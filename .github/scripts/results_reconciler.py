#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Axion Metrics — Results Reconciler  (AUTO layer)
================================================
Διασταυρώνει το Euronext Financial Calendar (ποιος δημοσίευσε αποτελέσματα
περιόδου) με τα δικά μας δεδομένα (data.js) → λίστα «δημοσίευσαν αλλά όχι live».
ΔΕΝ αλλάζει master/data.js.

ΔΥΟ ΠΗΓΕΣ (§96, 2026-09-21):
  1. **Οικονομικές εκθέσεις** του εκδότη στο Euronext Athens
     (/el/market-data/issuers/<cid>/financial-data). Δομημένος τίτλος
     «Οικονομική έκθεση <ΟΝΟΜΑ> (ΕΤΟΣ,Εξαμηνιαία|Ετήσιος Ισολογισμός,…)» + ημ/νία + PDF.
     Είναι ΤΟ ΙΔΙΟ το PDF που κατεβάζουμε → ΚΥΡΙΑ πηγή. Καλύπτει 136/137 (έλεγχος 21/09/2026).
  2. **Οικονομικό ημερολόγιο** (fin-cal-api). Δευτερεύουσα: για ~1/7 των εταιρειών δεν
     έχει ΚΑΜΙΑ εγγραφή (π.χ. 51 VIOHALCO), και κάποιες φορές κρατά ημερομηνίες που
     μετατέθηκαν. Εταιρεία που φαίνεται ΜΟΝΟ στο ημερολόγιο (χωρίς έκθεση) μπαίνει σε
     χωριστή ενότητα και ΔΕΝ μετράει ως εκκρεμότητα.

3ΜΗΝΑ / 9ΜΗΝΑ (§193, 2026-11-26): τρίτη πηγή οι ανακοινώσεις του εκδότη, αυξητικός έλεγχος με
μνήμη στο .github/monitor/reconciler_q_state.json — βλ. ενότητα «§193» πιο κάτω.

ΦΙΛΤΡΑ: εξαιρεί (α) frozen εταιρείες (UPDATED/CALCULATED=NO → `calculated=false`
στο data.js) και (β) μελλοντικές (προγραμματισμένες) ημ/νίες.
Σε ΚΑΘΕ report δείχνει ρητά το «Εκτός κάλυψης (frozen)» roster — ποιες αφήνουμε εκτός.
"""
import json, re, sys, os, argparse, datetime, urllib.request, html, time
from concurrent.futures import ThreadPoolExecutor

BASE = "https://athens.euronext.com/en/fin-cal-api"
ISSUER_URL = "https://athens.euronext.com/el/market-data/issuers/{cid}/financial-data"
UA = {"User-Agent": "AxionMetrics-Reconciler/1.0 (+https://axionmetrics.gr)"}

# Κλειδώνουμε στη ΔΗΜΟΣΙΕΥΣΗ ΤΗΣ ΕΚΘΕΣΗΣ (full report PDF) — αυτό κατεβάζουμε.
# Πολλές εταιρείες ανακοινώνουν πρώτα (press release) και δημοσιεύουν την έκθεση αργότερα
# (π.χ. ELVALHALCOR: ανακοίνωση 03.08 / δημοσίευση έκθεσης 04.09). Κρατάμε την πιο πρόσφατη.
INTERIM_TITLES = ("six months results announcement", "six months financial report publication",
                  "six months results publication", "six month results publication",
                  "half year financial report publication", "half-year financial report publication",
                  "interim financial report publication")
ANNUAL_TITLES  = ("annual results announcement", "twelve months results announcement",
                  "annual financial results announcement", "full year results announcement",
                  "annual financial report publication", "annual report publication",
                  "full year financial report publication")
# §69 — ΤΑΞΗ ΤΙΤΛΟΥ. Η «report publication» είναι η δημοσίευση της ΕΚΘΕΣΗΣ (το PDF που
# κατεβάζουμε)· η «results announcement» είναι το press release που προηγείται. Όταν μια
# εταιρεία έχει και τα δύο, μετράει ΜΟΝΟ η έκθεση.
REPORT_MARK = "report publication"
def title_rank(title):
    return 2 if REPORT_MARK in (title or "").lower() else 1

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

def fetch_month(ym, max_pages=80):
    """Σελιδοποίηση fin-cal (§32).

    Το API δεν επιστρέφει hasNextPage ΚΑΙ οι σελίδες επικαλύπτονται: υπάρχουν σελίδες
    εξ ολοκλήρου διπλές ενώ οι ΕΠΟΜΕΝΕΣ έχουν νέα δεδομένα. Το παλιό `if fresh==0: break`
    έσπαγε εκεί κι έχανε τον υπόλοιπο μήνα (Ιούλιος 2026: 15 από τα 125 events — γι' αυτό
    δεν καταγράφηκαν ποτέ οι δημοσιεύσεις 29–31/07 των μεγάλων κεφαλαιοποιήσεων).

    Πραγματικό τέλος: το API κλειδώνει στην τελευταία σελίδα και επιστρέφει για πάντα
    τα ίδια στοιχεία → σωστό κριτήριο = «η σελίδα είναι ίδια με την προηγούμενη».
    """
    seen, rows, prev = set(), [], None
    for p in range(max_pages):
        try: js = _get(f"{BASE}?date={ym}&page={p}")
        except Exception as e: sys.stderr.write(f"[warn] {ym} p{p}: {e}\n"); break
        items = parse_items(js.get("itemsHtml", ""))
        if not items: break
        cur = []
        for it in items:
            k = (it["cid"], it["date"], it["title"])
            cur.append(k)
            if k in seen: continue
            seen.add(k); rows.append(it)
        if prev is not None and cur == prev: break     # η σελίδα «κόλλησε» → τέλος μήνα
        prev = cur
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
def pick_publication(evs, cut):
    """Η ημ/νία δημοσίευσης ΜΙΑΣ εταιρείας, ανάμεσα σε πολλές εγγραφές ημερολογίου.

    ΔΥΟ ΑΞΟΝΕΣ, με αυτή τη σειρά:

    1) ΤΑΞΗ ΤΙΤΛΟΥ. Αν υπάρχει έστω μία «report publication», η «results announcement»
       αγνοείται εντελώς — περιμένουμε την έκθεση, αυτήν κατεβάζουμε.
       (26 ELVALHALCOR: ανακοίνωση 03.08 / δημοσίευση έκθεσης 04.09 → 04.09.)

    2) ΜΕΣΑ ΣΤΗΝ ΙΔΙΑ ΤΑΞΗ: η πιο πρόσφατη **ΠΕΡΑΣΜΕΝΗ** ημερομηνία. Μια μελλοντική
       εγγραφή ΔΕΝ σκεπάζει περασμένη του ίδιου τίτλου.

    Η διαφορά με τον παλιό κανόνα («κράτα πάντα την τελευταία, μετά πέτα τις μελλοντικές»):
    το Euronext γράφει καμιά φορά το ΙΔΙΟ γεγονός δύο φορές. Στην 39 PREMIA, 6μηνο 2026,
    υπήρχαν «Six Months Financial Report Publication» στις 15.09 ΚΑΙ στις 21.09. Ο παλιός
    κανόνας κρατούσε τη 21.09, το φίλτρο μελλοντικών την έκοβε, και η εταιρεία εξαφανιζόταν
    ενώ είχε ήδη δημοσιεύσει στις 15.09.

    Επιστρέφει None όταν η ανώτερη τάξη έχει ΜΟΝΟ μελλοντικές ημερομηνίες — η έκθεση δεν
    έχει βγει ακόμη. (14 CENERGY, 6μηνο 2026: ανακοίνωση 04.08, έκθεση 16.09· στις 15/09
    σωστά ΔΕΝ μετριέται, κι ας έχει περάσει η ανακοίνωση.)
    """
    top  = max(title_rank(e["title"]) for e in evs)
    same = [e for e in evs if title_rank(e["title"]) == top]
    past = [e for e in same if (not cut or date_key(e["date"]) <= cut)]
    if not past: return None
    return max(past, key=lambda e: date_key(e["date"]))

# ---------------------------------------------------------------- πηγή 1: οικονομικές εκθέσεις
FIN_URL = "https://athens.euronext.com/el/market-data/issuers/{cid}/financial-data"
FIN_TIT = re.compile(r'\((\d{4})\s*,\s*([^,()]+?)\s*,\s*([^,()]+?)\)')
FIN_KIND = {"interim": "εξαμην", "annual": "ετησ"}
# Η σελίδα εκθέσεων είναι πλήρης ΜΟΝΟ για τις εξαμηνιαίες: 136/137 έχουν «(2025,Εξαμηνιαία,…)»,
# ενώ «(2025,Ετήσιος Ισολογισμός,…)» έχουν μόνο 23 — οι ετήσιες από το 2022 και μετά
# (ESEF) λείπουν για τις περισσότερες. Άρα: εξάμηνο → η έκθεση είναι κυρίαρχη·
# έτος → κυρίαρχο μένει το ημερολόγιο και η έκθεση απλώς ΠΡΟΣΘΕΤΕΙ όσες λείπουν.
REPORTS_AUTHORITATIVE = {"interim": True, "annual": False}
# Η ίδια σελίδα φιλοξενεί και ΑΛΛΑ έγγραφα με τον ίδιο δομημένο τίτλο. Μετράει ΜΟΝΟ
# «Οικονομική έκθεση» / «Οικονομική κατάσταση». Εκτός: «Κατάσταση επενδύσεων» — η τρισέλιδη
# κατάσταση ακινήτων των ΑΕΕΑΠ στις 30/06, που ανεβαίνει ΠΡΙΝ από την έκθεση (48 TRASTOR:
# κατάσταση επενδύσεων 27/07/2026, έκθεση 25/09/2026) — και «Στοιχεία και Πληροφορίες» (παλιό).
FIN_DOC_OK = ("οικονομικη εκθεση", "οικονομικη κατασταση")

def _get_text(url, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            if k == tries - 1: raise
            time.sleep(2 + 3 * k)

def fetch_fin_reports(cid):
    """[{year, kind, scope, date(YYYYMMDD), title, pdf}] — πρώτη σελίδα (15 νεότερες εκθέσεις)."""
    t = _get_text(FIN_URL.format(cid=cid)); out = []
    for tr in re.findall(r'<tr[^>]*>([\s\S]*?)</tr>', t):
        cells = [re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', c))).strip()
                 for c in re.findall(r'<td[^>]*>([\s\S]*?)</td>', tr)]
        if len(cells) < 2: continue
        m = FIN_TIT.search(cells[0]); d = re.search(r'(\d{2})-(\d{2})-(\d{4})', cells[1])
        if not (m and d): continue
        pdf = re.search(r'href="([^"]+\.pdf[^"]*)"', tr)
        href = pdf.group(1) if pdf else None
        if href and href.startswith("/"): href = "https://athens.euronext.com" + href
        out.append({"year": int(m.group(1)), "kind": m.group(2), "scope": m.group(3),
                    "date": d.group(3) + d.group(2) + d.group(1), "title": cells[0], "pdf": href})
    return out

def _fold(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn").lower()

def reports_published(cid2row, basis, period, excluded_tks, asof, workers=4):
    """{code: row+date+pdf} από τις οικονομικές εκθέσεις. Κρατά έκθεση του σωστού ΕΙΔΟΥΣ και ΕΤΟΥΣ,
    δημοσιευμένη μέσα στο παράθυρο της περιόδου (ίδιοι μήνες με το ημερολόγιο) και όχι μετά το asof.
    Το παράθυρο κόβει τις μη ημερολογιακές χρήσεις (18 CPI, 131 NAKAS: «εξαμηνιαία 2026» τον Μάρτιο).
    Επιστρέφει και τα cid που απέτυχαν — γι' αυτά ισχύει μόνο το ημερολόγιο."""
    yr = int(period[:4]); want = FIN_KIND[basis]
    months = {tuple(int(x) for x in ym.split("-")) for ym in period_window(basis, period)}
    cut = asof.strftime("%Y%m%d") if asof else None
    rows = [r for r in cid2row.values() if r["tk"] not in excluded_tks]
    def one(r):
        try: return r, fetch_fin_reports(r["cid"]), None
        except Exception as e: return r, [], str(e)
    pub, failed = {}, []
    with ThreadPoolExecutor(workers) as ex:
        for r, reps, err in ex.map(one, rows):
            if err: failed.append(r["code"]); continue
            hits = [x for x in reps if x["year"] == yr and _fold(x["kind"]).startswith(want)
                    and _fold(x["title"]).startswith(FIN_DOC_OK)
                    and (int(x["date"][:4]), int(x["date"][4:6])) in months
                    and (not cut or x["date"] <= cut)]
            if hits:
                h = min(hits, key=lambda x: x["date"])          # η ΠΡΩΤΗ δημοσίευση της έκθεσης
                pub[r["code"]] = {**r, "date": f'{h["date"][6:]}.{h["date"][4:6]}.{h["date"][:4]}',
                                  "title": h["title"], "pdf": h["pdf"], "src": "έκθεση"}
    return pub, failed

def reconcile(events, cid2row, reported_tks, basis, period, excluded_tks=None, asof=None):
    excluded_tks = excluded_tks or set()
    cut = asof.strftime("%Y%m%d") if asof else None
    cand = {}
    for ev in events:
        if not ev["cid"] or not is_result(ev["title"], basis): continue
        if event_period(ev, basis) != period: continue
        row = cid2row.get(ev["cid"])
        if not row or row["tk"] in excluded_tks: continue
        cand.setdefault(row["code"], (row, []))[1].append(ev)
    published = {}
    for code, (row, evs) in cand.items():
        best = pick_publication(evs, cut)
        if best: published[code] = {**row, "date": best["date"], "title": best["title"]}
    pub = sorted(published.values(), key=lambda r: date_key(r["date"]))
    return {"published": pub, "new": [r for r in pub if r["tk"] not in reported_tks]}

# ---------------------------------------------------------------- §193 — 3ΜΗΝΑ / 9ΜΗΝΑ
# Οι τριμηνιαίες ΔΕΝ είναι υποχρεωτικές (Ν. 3556/2007 όπως ισχύει) → δεν υπάρχει πλήρης λίστα
# «ποιος πρέπει να δημοσιεύσει». Έλεγχος 26/11/2026 στις εταιρείες με δεδομένα 3Μ/9Μ 2026:
#   πηγή                        3Μ (43)   9Μ (40)
#   οικονομικό ημερολόγιο         26        32
#   σελίδα εκθέσεων εκδότη        14        13
#   ανακοινώσεις εκδότη           41        37 (+2 με γενικό τίτλο)
#   ανακοινώσεις + εκθέσεις       43        40
# → ΤΡΕΙΣ πηγές. Οι ανακοινώσεις είναι ΑΝΑ ΕΚΔΟΤΗ (καμία ενιαία λίστα στο Euronext Athens),
#   οπότε ο έλεγχος είναι ΑΥΞΗΤΙΚΟΣ (απαίτηση user): ψάχνει ΜΟΝΟ εταιρείες που (α) δεν είναι
#   live στο data.js και (β) δεν έχουν ήδη βρεθεί. Ό,τι βρεθεί, και ως ποια ημερομηνία έχουν
#   διαβαστεί οι ανακοινώσεις κάθε εκδότη, μένει στο Q_STATE· το επόμενο τρέξιμο διαβάζει
#   μόνο τις καινούργιες ανακοινώσεις (συνήθως μόνο την 1η σελίδα).
Q_BASES  = ("q1", "q3")
Q_WIN    = {"q1": (4, 5, 6, 7), "q3": (10, 11, 12)}          # μήνες δημοσίευσης
Q_CAL    = {"q1": ("three months results", "three month results"),
            "q3": ("nine months results", "nine month results")}
Q_REP    = {"q1": "τριμην", "q3": "εννιαμην"}                 # «Τριμηνιαία» / «Εννιαμηνιαία»
_AP = r"\s*['΄’`]?\s*"
Q_ANN = {
    "q1": re.compile(r"(α|a|1ου|πρωτου|πρωτο)" + _AP + r"τριμην|3μην|\b3μ\s*\d{4}|three.?month"
                     r"|\bq1\b|\b1q\b|first quarter"),
    "q3": re.compile(r"εννε?α?μην|εννιαμην|9μην|\b9μ\s*\d{4}|\b9m\b|nine.?month|(γ|3ου|τριτου|τριτο)"
                     + _AP + r"τριμην|\bq3\b|\b3q\b|third quarter"),
}
# ημερομηνία λήξης περιόδου στον τίτλο μετράει ΜΟΝΟ μαζί με λέξη αποτελεσμάτων
# (123 REVOIL «αποτελεσμάτων περιόδου 01.01 έως 30.09.2026» ναι · 57 ALUMIL «Midcap Event … 30.09.2026» όχι)
Q_ANN_DATE = {"q1": re.compile(r"31[./]0?3[./]\d{4}"), "q3": re.compile(r"30[./]0?9[./]\d{4}")}
Q_ANN_RES  = re.compile(r"αποτελεσματ|results|μεγεθ|περιοδου")
# εκτός: ανακοινώσεις ΗΜΕΡΟΜΗΝΙΑΣ αποτελεσμάτων, οικονομικό ημερολόγιο, άλλο τρίμηνο
# (60 ADMHE / 119 PLASTIKA THRAKIS: «Ημερομηνία δημοσίευσης αποτελεσμάτων εννεαμήνου» — προαναγγελία, όχι δημοσίευση·
#  29 JUMBO: «δυναμική των πωλήσεων στο εννεάμηνο» — ενημέρωση πωλήσεων, όχι αποτελέσματα)
Q_ANN_EXC = re.compile(r"ημερομηνι\w* (και ωρα )?(ανακοινωσ|δημοσιευσ)|οικονομικο(υ)? ημερολογιο"
                       r"|financial calendar|(β|2ου|δευτερου)" + _AP + r"τριμην|εξαμην|πωλησ|\bsales\b"
                       r"|subsidiary|θυγατρικ")      # 51 VIOHALCO: «subsidiary ElvalHalcor financial results Q1»
# γενικός τίτλος χωρίς περίοδο («Δελτία Τύπου Αποτελεσμάτων – Παρουσιάσεις»): μόνο ένδειξη
Q_ANN_GEN = re.compile(r"αποτελεσματ|results")
Q_ANN_GEN_EXC = re.compile(r"ψηφοφορι|συνελευσ|δημοπρασ|δημοσιας (προσφορας|προτασ)|ipo|χρησ|ετησ|ετους|31\.12")
# γενικός τίτλος μετράει ως ένδειξη ΜΟΝΟ σε μήνες χωρίς ετήσια/6μηνα: Απρίλιος = ετήσια, Ιούλιος = 6μηνα
Q_GEN_MONTHS = {"q1": (5, 6), "q3": (10, 11, 12)}
ANN_URL = "https://athens.euronext.com/el/market-data/issuers/{cid}/announcements?page={p}"
ANN_MAX_PAGES = 15

def q_label(basis, period): return ("3μηνο " if basis == "q1" else "9μηνο ") + period[:4]

def q_season(asof):
    """Ποια τριμηνιαία περίοδος ελέγχεται σήμερα (ή None): 3Μ Απρ–Αύγ, 9Μ Οκτ–Ιαν."""
    m = asof.month
    if 4 <= m <= 8:  return "q1", f"{asof.year}Q1"
    if m >= 10:      return "q3", f"{asof.year}Q3"
    if m == 1:       return "q3", f"{asof.year - 1}Q3"
    return None

def _ymd(d):  # '05-11-2026' ή '05.11.2026' → '20261105'
    p = re.split(r"[.-]", d or "")
    return f"{p[2]}{p[1].zfill(2)}{p[0].zfill(2)}" if len(p) == 3 else ""

def q_live(data_js, basis, yr):
    """tickers με δεδομένα αποτελεσμάτων 3Μ/9Μ στο data.js (ίδιος κανόνας με το site, §191:
    μόνο ισολογισμός ΔΕΝ μετράει ως live)."""
    pl = ("revenue", "ebitda", "ebitda_rep", "net_profit", "pat", "ppi")
    out = set()
    for c in _load_axion(data_js).get("companies", {}).get("annual", []):
        q = (c.get("quarters") or {}).get(basis)
        if q and q.get("y") == yr and any((q.get("m") or {}).get(k) is not None for k in pl):
            out.add(c["tk"])
    return out

def fetch_announcements(cid, stop_before):
    """Ανακοινώσεις εκδότη, νεότερες πρώτα, μέχρι να βρεθεί ημερομηνία < stop_before.
    → (rows[(yyyymmdd, title, href)], newest_seen)"""
    out, newest = [], ""
    for p in range(ANN_MAX_PAGES):
        t = _get_text(ANN_URL.format(cid=cid, p=p)); page = []
        for tr in re.findall(r'<tr[^>]*>([\s\S]*?)</tr>', t):
            cells = [re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', c))).strip()
                     for c in re.findall(r'<td[^>]*>([\s\S]*?)</td>', tr)]
            d = next((_ymd(m.group(0)) for c in cells for m in [re.search(r'\d{2}-\d{2}-\d{4}', c)] if m), "")
            if not (cells and d): continue
            a = re.search(r'href="([^"]+)"', tr)
            href = a.group(1) if a else ""
            if href.startswith("/"): href = "https://athens.euronext.com" + href
            page.append((d, cells[0], href))
        if not page: break
        out += page; newest = max(newest, max(x[0] for x in page))
        if min(x[0] for x in page) < stop_before: break
    return out, newest

def run_quarter(basis, period, cid2row, data_js, asof, state_path):
    yr = int(period[:4]); months = Q_WIN[basis]
    lo = f"{yr}{months[0]:02d}01"; cut = asof.strftime("%Y%m%d")
    live = q_live(data_js, basis, yr)
    ann_year = _load_axion(data_js)["rowsByPeriod"]["annual"]
    _last = max(ann_year) if ann_year else None
    excluded = load_calc_excluded_from_datajs(data_js, "annual", _last) if _last else set()
    names = load_display_names(data_js, "annual", _last) if _last else {}
    try: ST = json.load(open(state_path, encoding="utf-8"))
    except Exception: ST = {}
    S = ST.setdefault(period, {"found": {}, "scanned": {}})
    rows = [r for r in cid2row.values() if r["tk"] not in excluded]
    todo = [r for r in rows if r["tk"] not in live and r["tk"] not in S["found"]]

    # 1) οικονομικό ημερολόγιο (λίγες σελίδες για όλη την αγορά)
    cal_past, upcoming = {}, {}
    for m in months:
        for ev in fetch_month(f"{yr}-{m}"):
            t = (ev["title"] or "").lower()
            if not ev["cid"] or not any(x in t for x in Q_CAL[basis]): continue
            row = cid2row.get(ev["cid"])
            if not row or row["tk"] in excluded or row["tk"] in live: continue
            d = _ymd(ev["date"])
            tgt = cal_past if d <= cut else upcoming
            if d > tgt.get(row["tk"], ("",))[0]: tgt[row["tk"]] = (d, row)

    # 2) ανακοινώσεις + 3) εκθέσεις — ΜΟΝΟ για όσες λείπουν (αυξητικά)
    def one(r):
        cid = str(r["cid"]); seen = S["scanned"].get(cid, "")
        hit, weak, err = None, None, None
        try:
            ann, newest = fetch_announcements(cid, max(lo, seen))
            for d, ti, href in ann:
                if not (lo <= d <= cut) or (seen and d < seen): continue
                f = _fold(ti)
                if Q_ANN_EXC.search(f): continue
                if Q_ANN[basis].search(f) or (Q_ANN_DATE[basis].search(f) and Q_ANN_RES.search(f)):
                    if not hit or d < hit["d"]: hit = {"d": d, "title": ti, "url": href, "src": "ανακοίνωση"}
                elif (Q_ANN_GEN.search(f) and not Q_ANN_GEN_EXC.search(f) and str(yr - 1) not in f
                      and int(d[4:6]) in Q_GEN_MONTHS[basis] and not weak):
                    weak = {"d": d, "title": ti, "url": href, "src": "ανακοίνωση (γενικός τίτλος)", "weak": True}
            if not hit:
                for x in fetch_fin_reports(cid):
                    if (x["year"] == yr and _fold(x["kind"]).startswith(Q_REP[basis])
                            and _fold(x["title"]).startswith(FIN_DOC_OK) and lo <= x["date"] <= cut):
                        hit = {"d": x["date"], "title": x["title"], "url": x["pdf"], "src": "έκθεση"}; break
        except Exception as e:
            return r, None, None, None, str(e)
        return r, hit or weak, newest, None, err
    failed = []
    with ThreadPoolExecutor(4) as ex:
        for r, hit, newest, _, err in ex.map(one, todo):
            if err: failed.append(r["code"]); continue
            if newest: S["scanned"][str(r["cid"])] = newest
            if hit and not hit.get("weak"): S["found"][r["tk"]] = hit
            elif hit: S.setdefault("weak", {})[r["tk"]] = hit
    for tk in list(S.get("weak", {})):           # γενικός τίτλος που πλέον επιβεβαιώθηκε/έγινε live
        if tk in S["found"] or tk in live: S["weak"].pop(tk)

    def mk(row, d, src, title="", url=""):
        return {**row, "date": f"{d[6:]}.{d[4:6]}.{d[:4]}", "src": src, "title": title,
                "pdf": url, "disp": names.get(row["tk"]) or _short(row["name"])}
    by_tk = {r["tk"]: r for r in rows}
    new = {}
    for tk, h in S["found"].items():
        if tk in live or tk not in by_tk: continue
        new[tk] = mk(by_tk[tk], h["d"], h["src"], h.get("title", ""), h.get("url", ""))
    for tk, (d, row) in cal_past.items():
        if tk not in new: new[tk] = mk(row, d, "ημερολόγιο")
        elif "ημερολόγιο" not in new[tk]["src"]: new[tk]["src"] += " + ημερολόγιο"
    weak = [mk(by_tk[tk], h["d"], h["src"], h.get("title", ""), h.get("url", ""))
            for tk, h in S.get("weak", {}).items() if tk not in new and tk in by_tk]
    up = [mk(row, d, "ημερολόγιο") for tk, (d, row) in upcoming.items() if tk not in new]
    os.makedirs(os.path.dirname(os.path.abspath(state_path)), exist_ok=True)
    json.dump(ST, open(state_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    srt = lambda L: sorted(L, key=lambda r: date_key(r["date"]))
    return {"q": True, "published": srt(new.values()), "new": srt(new.values()), "weak": srt(weak),
            "upcoming": srt(up), "failed": failed, "n_live": len(live), "n_scan": len(todo)}

def _short(n): return n.split(" ", 1)[1] if " " in n else n
def label(basis, period):
    if basis in Q_BASES: return q_label(basis, period)
    return (f"6μηνο {period[:4]}" if basis == "interim" else f"έτος {period}")

# ---------------------------------------------------------------- report
def render_quarter(basis, period, res):
    """§193 — ενότητα 3Μ/9Μ. Μετράει ΜΟΝΟ το «εκκρεμούν»· γενικοί τίτλοι και προγραμματισμένες
    ημερομηνίες εμφανίζονται για ενημέρωση."""
    L = ["", f"## {label(basis, period)}",
         f"live στο site: **{res['n_live']}** · ελέγχθηκαν σε αυτό το τρέξιμο: {res['n_scan']} "
         f"(μόνο όσες λείπουν) · εκκρεμούν στο master: **{len(res['new'])}**", ""]
    if res.get("failed"):
        L += [f"⚠️ Δεν διαβάστηκαν οι σελίδες για κωδ. {', '.join(map(str, res['failed']))} — ξαναδοκιμάζονται στο επόμενο τρέξιμο.", ""]
    if not res["new"]:
        L.append("_Καμία εκκρεμότητα._")
    else:
        L += ["| Εταιρεία | Ticker | Δημοσίευση | Πηγή | Σύνδεσμος |", "|---|---|---|---|---|"]
        for r in res["new"]:
            link = f"[↗]({r['pdf']})" if r.get("pdf") else f"[issuer ↗]({ISSUER_URL.format(cid=r['cid'])})"
            L.append(f"| **{r['code']} · {r['disp']}** | {r['tk']} | {r['date']} | {r['src']} | {link} |")
    if res.get("weak"):
        L += ["", "**Ανακοίνωση αποτελεσμάτων χωρίς περίοδο στον τίτλο — να ελεγχθεί** (δεν μετράει):", ""]
        for r in res["weak"]:
            L.append(f"- {r['code']} · {r['disp']} — {r['date']} «{r['title']}» [↗]({r['pdf']})")
    if res.get("upcoming"):
        L += ["", "**Αναμένονται** (οικονομικό ημερολόγιο):", ""]
        for r in res["upcoming"]:
            L.append(f"- {r['code']} · {r['disp']} — {r['date']}")
    return L

def render_report(results, asof, roster):
    tot_new = sum(len(r["new"]) for _,_,r in results)
    L = [f"# 🎯 Results Reconciler — {asof}", ""]
    if tot_new == 0:
        L.append("Καμία νέα δημοσίευση εκτός site. ✅")
    for basis, period, res in results:
        if res.get("q"):
            L += render_quarter(basis, period, res); continue
        L += ["", f"## {label(basis, period)}",
              f"live στο site: **{res.get('n_live', 0)}** · δημοσίευσαν εκτός site: εκθέσεις {res.get('n_rep', 0)} "
              f"(ελέγχονται μόνο όσες λείπουν) · ημερολόγιο {res.get('n_cal', 0)}  ·  "
              f"εκκρεμούν στο master: **{len(res['new'])}**", ""]
        if res.get("failed"):
            L += [f"⚠️ Δεν διαβάστηκαν οι εκθέσεις για κωδ. {', '.join(map(str, res['failed']))} — "
                  f"για αυτές ισχύει μόνο το ημερολόγιο.", ""]
        if not res["new"]:
            L.append("_Όλες live._")
        else:
            L += ["| Εταιρεία | Ticker | Δημοσίευση | Πηγή | Έκθεση |", "|---|---|---|---|---|"]
            for r in res["new"]:
                disp = r.get("disp") or _short(r["name"])  # database name (master), fallback cid_map
                link = f"[PDF ↗]({r['pdf']})" if r.get("pdf") else f"[issuer ↗]({ISSUER_URL.format(cid=r['cid'])})"
                L.append(f"| **{r['code']} · {disp}** | {r['tk']} | {r['date']} | {r.get('src', '')} | {link} |")
        if res.get("cal_only"):
            L += ["", "**Μόνο στο ημερολόγιο — δεν έχει ανέβει έκθεση** (πιθανή μετάθεση· δεν μετράει):", ""]
            for r in res["cal_only"]:
                disp = r.get("disp") or _short(r["name"])
                L.append(f"- {r['code']} · {disp} — ημερολόγιο {r['date']}")
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
    cal = {r["code"]: {**r, "src": "ημερολόγιο"} for r in res["published"]}
    if os.environ.get("RECON_NO_REPORTS"):
        rep_pub, failed = {}, []
    else:
        # §193 — οι εκθέσεις διαβάζονται ΜΟΝΟ για όσες ΔΕΝ είναι ήδη live (δεν ξαναελέγχουμε
        # ό,τι έχουμε ήδη): ένα αίτημα ανά εταιρεία που λείπει, αντί για ~140 σε κάθε τρέξιμο.
        rep_pub, failed = reports_published(cid2row, basis, period, excluded | reported, asof)
    # Έκθεση = κυρίαρχη. Ημερολόγιο μόνο: (α) όπου απέτυχε η ανάγνωση εκθέσεων → μετράει κανονικά,
    # (β) αλλιώς → «μόνο ημερολόγιο» (πιθανώς μετατεθειμένη ημερομηνία), ΔΕΝ μετράει ως εκκρεμότητα.
    published = dict(rep_pub)
    cal_only = []
    for code, r in cal.items():
        if code in published: continue
        if code in failed or not REPORTS_AUTHORITATIVE[basis]: published[code] = r
        else: cal_only.append(r)
    pub = sorted(published.values(), key=lambda r: date_key(r["date"]))
    res = {"published": pub, "new": [r for r in pub if r["tk"] not in reported],
           "cal_only": sorted([r for r in cal_only if r["tk"] not in reported], key=lambda r: date_key(r["date"])),
           "failed": failed, "n_cal": len(cal), "n_rep": len(rep_pub), "n_live": len(reported)}
    # Εμπλουτισμός ΜΟΝΟ εμφάνισης: database name από το master· fallback στο cid_map name.
    # (res["new"] μοιράζεται τα ίδια dict-objects με res["published"], άρα καλύπτεται κι αυτό.)
    for r in res["published"] + res["cal_only"]:
        r["disp"] = names.get(r["tk"]) or _short(r["name"])
    return res

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cid-map", default=".github/scripts/euronext_cid_map.json")
    ap.add_argument("--data-js", default="assets/data.js")
    ap.add_argument("--basis", default="interim", choices=["interim", "annual", "q1", "q3"])
    ap.add_argument("--both", action="store_true")
    ap.add_argument("--all", action="store_true", help="ετήσια + 6μηνο + το τρέχον 3μηνο/9μηνο (§193)")
    ap.add_argument("--q-state", default=".github/monitor/reconciler_q_state.json")
    ap.add_argument("--period"); ap.add_argument("--asof"); ap.add_argument("--out")
    ap.add_argument("--events-json")
    args = ap.parse_args()

    asof = datetime.date.fromisoformat(args.asof) if args.asof else datetime.datetime.utcnow().date()
    auto_period = lambda b: (f"{asof.year}H1" if b == "interim" else str(asof.year - 1))
    cid2row, _ = load_cid_map(args.cid_map)
    bases = ["interim", "annual"] if (args.both or args.all) else [args.basis]
    if args.all and q_season(asof): bases.append(q_season(asof)[0])

    results, roster = [], []
    for b in bases:
        if b in Q_BASES:
            period = (args.period if (args.period and not (args.both or args.all))
                      else (q_season(asof) or (None, f"{asof.year}{b.upper()}"))[1])
            results.append((b, period, run_quarter(b, period, cid2row, args.data_js, asof, args.q_state)))
            continue
        period = args.period if (args.period and not (args.both or args.all)) else auto_period(b)
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
