#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Axion Metrics — Results Reconciler  (AUTO layer)
================================================
Διασταυρώνει το Euronext Financial Calendar (ποιος δημοσίευσε αποτελέσματα
περιόδου) με τα δικά μας δεδομένα (data.js) → λίστα «δημοσίευσαν αλλά όχι live».
ΔΕΝ αλλάζει master/data.js.

ΦΙΛΤΡΑ: εξαιρεί (α) frozen εταιρείες (UPDATED/CALCULATED=NO → `calculated=false`
στο data.js) και (β) μελλοντικές (προγραμματισμένες) ημ/νίες.
Σε ΚΑΘΕ report δείχνει ρητά το «Εκτός κάλυψης (frozen)» roster — ποιες αφήνουμε εκτός.
"""
import json, re, sys, os, argparse, datetime, urllib.request

BASE = "https://athens.euronext.com/en/fin-cal-api"
ISSUER_URL = "https://athens.euronext.com/en/issuers/{cid}"
UA = {"User-Agent": "AxionMetrics-Reconciler/1.0 (+https://axionmetrics.gr)"}

# Κλειδώνουμε στη ΔΗΜΟΣΙΕΥΣΗ ΤΗΣ ΕΚΘΕΣΗΣ (full report PDF) — αυτό κατεβάζουμε.
# Πολλές εταιρείες ανακοινώνουν πρώτα (press release) και δημοσιεύουν την έκθεση αργότερα
# (π.χ. ELVALHALCOR: ανακοίνωση 03.08 / δημοσίευση έκθεσης 04.09). Κρατάμε την πιο πρόσφατη.
INTERIM_TITLES = ("six months results announcement", "six months financial report publication",
                  "half year financial report publication", "half-year financial report publication",
                  "interim financial report publication")
ANNUAL_TITLES  = ("annual results announcement", "twelve months results announcement",
                  "annual financial results announcement", "full year results announcement",
                  "annual financial report publication", "annual report publication",
                  "full year financial report publication")
INTERIM_MONTHS = (7, 8, 9, 10, 11)
ANNUAL_MONTHS  = (2, 3, 4, 5, 6)

# ---------------------------------------------------------------- fetch/parse
def _get(url, timeout=45):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))

CAT_RE   = re.compile(r'category-calendar">([^<]+)<')
DATE_RE  = re.compile(r'class="date">\s*([0-9.]+)\s*<')
CID_RE   = re.compile(r'/issuers/(\d+)')
NAME_RE  = re.compile(r'/issuers/\d+"\s*>\s*([^<]+?)\s*</a>')
TITLE_RE = re.compile(r'title-calendar">([^<]+)<')

def parse_items(items_html):
    """itemsHtml -> [{cat,date,cid,name,title}] · split στο '<div class="item">'."""
    out = []
    for blk in (items_html or "").split('<div class="item">')[1:]:
        cid = CID_RE.search(blk); cat = CAT_RE.search(blk); dt = DATE_RE.search(blk)
        nm = NAME_RE.search(blk); ti = TITLE_RE.search(blk)
        out.append({"cat": cat.group(1).strip() if cat else "",
                    "date": dt.group(1).strip() if dt else "",
                    "cid": cid.group(1) if cid else None,
                    "name": nm.group(1).strip() if nm else "",
                    "title": ti.group(1).strip() if ti else ""})
    return out

def fetch_month(ym, max_pages=25):
    seen, rows = set(), []
    for p in range(max_pages):
        try: js = _get(f"{BASE}?date={ym}&page={p}")
        except Exception as e: sys.stderr.write(f"[warn] {ym} p{p}: {e}\n"); break
        items = parse_items(js.get("itemsHtml", ""))
        if not items: break
        fresh = 0
        for it in items:
            k = (it["cid"], it["date"], it["title"])
            if k in seen: continue
            seen.add(k); rows.append(it); fresh += 1
        if fresh == 0: break
    return rows

# ---------------------------------------------------------------- helpers
def period_window(basis, period):
    if basis == "interim":
        yr = int(period[:4]); return [f"{yr}-{m}" for m in INTERIM_MONTHS]
    yr = int(period) + 1;    return [f"{yr}-{m}" for m in ANNUAL_MONTHS]

def is_result(title, basis):
    t = (title or "").lower()
    return any(x in t for x in (INTERIM_TITLES if basis == "interim" else ANNUAL_TITLES))

def event_period(ev, basis):
    yr = int(ev["date"].split(".")[-1])
    return f"{yr}H1" if basis == "interim" else str(yr - 1)

def date_key(d):
    p = (d or "").split(".")
    if len(p) != 3: return ""
    dd, mm, yy = p
    return f"{yy}{mm.zfill(2)}{dd.zfill(2)}"

def load_cid_map(path):
    m = json.load(open(path, encoding="utf-8"))
    return {str(r["cid"]): r for r in m["rows"]}, {str(r["code"]): r for r in m["rows"]}

def _load_axion(path):
    txt = open(path, encoding="utf-8").read()
    mm = re.search(r'window\.AXION\s*=\s*(\{.*\})\s*;', txt, re.S)
    return json.loads(mm.group(1))

def _rows(path, basis, period):
    return _load_axion(path)["rowsByPeriod"][basis].get(period, [])

def load_reported_from_datajs(path, basis, period):
    return {r["tk"] for r in _rows(path, basis, period) if r.get("reported") is True}

def load_calc_excluded_from_datajs(path, basis, period):
    return {r["tk"] for r in _rows(path, basis, period) if r.get("calculated") is False}

def load_frozen_roster(path, basis, period):
    """[names] των frozen (calculated=false) — για το «Εκτός κάλυψης» roster."""
    return sorted({(r.get("t") or r.get("tk")) for r in _rows(path, basis, period)
                   if r.get("calculated") is False})

def load_display_names(path, basis, period):
    """{ticker -> ΟΝΟΜΑ ΣΤΗ ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ} από data.js — ΜΟΝΟ για εμφάνιση.
    Δεν συμμετέχει στην αντιστοίχιση (που μένει στο cid) — χρησιμεύει ώστε τα reports
    να δείχνουν το database name του master, όχι τη συντομευμένη Euronext-εκδοχή του cid_map."""
    return {r["tk"]: r.get("t") for r in _rows(path, basis, period) if r.get("t")}

# ---------------------------------------------------------------- reconcile
def reconcile(events, cid2row, reported_tks, basis, period, excluded_tks=None, asof=None):
    excluded_tks = excluded_tks or set(); published = {}
    for ev in events:
        if not ev["cid"] or not is_result(ev["title"], basis): continue
        if event_period(ev, basis) != period: continue
        row = cid2row.get(ev["cid"])
        if not row or row["tk"] in excluded_tks: continue
        cur = published.get(row["code"])
        # Κρατάμε την ΠΙΟ ΠΡΟΣΦΑΤΗ ημ/νία: η δημοσίευση της έκθεσης (full report)
        # υπερισχύει της απλής ανακοίνωσης αποτελεσμάτων (press release).
        if not cur or date_key(ev["date"]) > date_key(cur["date"]):
            published[row["code"]] = {**row, "date": ev["date"], "title": ev["title"]}
    # asof ΜΕΤΑ την επιλογή: αν η (τελική) ημ/νία δημοσίευσης της έκθεσης είναι μελλοντική,
    # η εταιρεία εξαιρείται — ακόμη κι αν η προγενέστερη ανακοίνωση έχει ήδη περάσει.
    if asof:
        cut = asof.strftime("%Y%m%d")
        published = {k: v for k, v in published.items() if date_key(v["date"]) <= cut}
    pub = sorted(published.values(), key=lambda r: date_key(r["date"]))
    return {"published": pub, "new": [r for r in pub if r["tk"] not in reported_tks]}

def _short(n): return n.split(" ", 1)[1] if " " in n else n
def label(basis, period): return (f"6μηνο {period[:4]}" if basis == "interim" else f"έτος {period}")

# ---------------------------------------------------------------- report
def render_report(results, asof, roster):
    tot_new = sum(len(r["new"]) for _,_,r in results)
    L = [f"# 🎯 Results Reconciler — {asof}", ""]
    if tot_new == 0:
        L.append("Καμία νέα δημοσίευση εκτός site. ✅")
    for basis, period, res in results:
        L += ["", f"## {label(basis, period)}",
              f"δημοσίευσαν (Euronext, στις 133 μας): **{len(res['published'])}**  ·  "
              f"εκκρεμούν στο master: **{len(res['new'])}**", ""]
        if not res["new"]:
            L.append("_Όλες live._"); continue
        L += ["| Εταιρεία | Ticker | Δημοσίευση (Euronext) | Euronext |", "|---|---|---|---|"]
        for r in res["new"]:
            disp = r.get("disp") or _short(r["name"])  # database name (master), fallback cid_map
            L.append(f"| **{r['code']} · {disp}** | {r['tk']} | {r['date']} | "
                     f"[issuer ↗]({ISSUER_URL.format(cid=r['cid'])}) |")
    # frozen roster — ΠΑΝΤΑ, για να βλέπουμε ποιες αφήνουμε εκτός
    L += ["", f"## ⏸️ Εκτός κάλυψης (frozen) — δεν παρακολουθούνται · {len(roster)}", ""]
    if roster:
        for nm in roster: L.append(f"- {nm}")
        L.append("")
        L.append("_Εξαιρούνται από τη λίστα δημοσιεύσεων (UPDATED=NO). Επανεισαγωγή/άρση αναστολής "
                 "τις ξανα-ενεργοποιεί αυτόματα μέσω του μηχανισμού Monitor→TRADING._")
    else:
        L.append("_Καμία._")
    L += ["", "---", "_Δεν γράφει τίποτα. Εξαιρεί frozen + μελλοντικές ημ/νίες._"]
    return "\n".join(L)

# ---------------------------------------------------------------- GH plumbing
def gh_output(k, v):
    p = os.environ.get("GITHUB_OUTPUT")
    if p: open(p, "a", encoding="utf-8").write(f"{k}={v}\n")
def step_summary(md):
    p = os.environ.get("GITHUB_STEP_SUMMARY")
    if p: open(p, "a", encoding="utf-8").write(md + "\n")

# ---------------------------------------------------------------- main
def run_basis(basis, period, cid2row, data_js, asof, events_json=None):
    reported = load_reported_from_datajs(data_js, basis, period)
    excluded = load_calc_excluded_from_datajs(data_js, basis, period)
    names    = load_display_names(data_js, basis, period)   # {tk -> database name}, μόνο για εμφάνιση
    if events_json:
        events = json.load(open(events_json, encoding="utf-8"))
    else:
        events = []
        for ym in period_window(basis, period): events += fetch_month(ym)
    res = reconcile(events, cid2row, reported, basis, period, excluded_tks=excluded, asof=asof)
    # Εμπλουτισμός ΜΟΝΟ εμφάνισης: database name από το master· fallback στο cid_map name.
    # (res["new"] μοιράζεται τα ίδια dict-objects με res["published"], άρα καλύπτεται κι αυτό.)
    for r in res["published"]:
        r["disp"] = names.get(r["tk"]) or _short(r["name"])
    return res

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cid-map", default=".github/scripts/euronext_cid_map.json")
    ap.add_argument("--data-js", default="assets/data.js")
    ap.add_argument("--basis", default="interim", choices=["interim", "annual"])
    ap.add_argument("--both", action="store_true")
    ap.add_argument("--period"); ap.add_argument("--asof"); ap.add_argument("--out")
    ap.add_argument("--events-json")
    args = ap.parse_args()

    asof = datetime.date.fromisoformat(args.asof) if args.asof else datetime.datetime.utcnow().date()
    auto_period = lambda b: (f"{asof.year}H1" if b == "interim" else str(asof.year - 1))
    cid2row, _ = load_cid_map(args.cid_map)
    bases = ["interim", "annual"] if args.both else [args.basis]

    results, roster = [], []
    for b in bases:
        period = args.period if (args.period and not args.both) else auto_period(b)
        results.append((b, period, run_basis(b, period, cid2row, args.data_js, asof, args.events_json)))
        if not roster:
            roster = load_frozen_roster(args.data_js, b, period)

    report = render_report(results, asof, roster)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        open(args.out, "w", encoding="utf-8").write(report + "\n")
    tot_new = sum(len(r["new"]) for _,_,r in results)
    step_summary(report); gh_output("has_new", "true" if tot_new else "false")
    gh_output("new_count", str(tot_new))
    print(report)
    return results

if __name__ == "__main__":
    main()
