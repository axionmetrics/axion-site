
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Euronext Monitor — Axion Metrics
=================================
Εβδομαδιαίος έλεγχος εταιρικών γεγονότων από το Euronext Athens.
 
ΔΕΝ μεταλλάσσει το master ούτε το data.js. Απλώς ΑΝΙΧΝΕΥΕΙ αλλαγές
συγκρίνοντας με ένα αποθηκευμένο snapshot και ΑΝΑΦΕΡΕΙ (report + Issue).
Το master (ΑΡΙΘΜΟΔΕΙΚΤΕΣ.xlsx) παραμένει η πηγή αλήθειας.
 
Πηγές:
  1) stocks_details_el.json  -> Market Segment, Trading Status (1=ενεργό/0=αναστολή),
                                Type/Date of Last Corporate Action (σκανδάλη ΑΜΚ),
                                ISIN, Market Capitalisation.
  2) cash-distribution (HTML) -> δομημένες χρηματικές διανομές
                                (σύμβολο, ποσό, τύπος, αποκοπή, πληρωμή, χρήση).
 
Κατηγορίες που καλύπτει:
  - Trading status (αναστολή/επαναφορά)                [πλήρως, από JSON]
  - Market segment (Κύρια/ΕΝ.Α/Επιτήρηση/Αναστολή)     [πλήρως, από JSON]
  - Εισαγωγές/Διαγραφές (νέο/χαμένο σύμβολο)           [πλήρως, από JSON]
  - Χρηματικές διανομές (μερίσματα/επιστροφές κεφ.)     [πλήρως, από cash-distribution]
  - Μεταβολές μετοχικού κεφαλαίου (ΑΜΚ κ.λπ.)          [σκανδάλη, από JSON "last corp. action"]
Εκτός εμβέλειας (χειροκίνητα): αλλαγές δεικτών (αναθεωρήσεις ΧΑ).
"""
 
import json
import os
import sys
import datetime
import urllib.request
 
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Λείπει το beautifulsoup4 (pip install beautifulsoup4).", file=sys.stderr)
    raise
 
# ----------------------------------------------------------------------------
BASE = "https://athens.euronext.com"
STOCKS_JSON = BASE + "/sites/default/files/json_data_files/stocks_details_el.json"
CASH_URL    = BASE + "/el/market-data/cash-distribution"
CASH_PAGES  = 2   # πόσες σελίδες διανομών να τραβάμε (10 γραμμές/σελίδα, φθίνουσα αποκοπή)
 
HERE      = os.path.dirname(os.path.abspath(__file__))
MON_DIR   = os.path.normpath(os.path.join(HERE, "..", "monitor"))
SNAP_PATH = os.path.join(MON_DIR, "snapshot.json")
REPORT_MD = os.path.join(MON_DIR, "last_report.md")
 
STATUS_LABEL = {"1": "Ενεργή διαπραγμάτευση", "0": "Σε αναστολή"}
 
UA = {"User-Agent": "AxionMetrics-Monitor/1.0 (+https://axionmetrics.gr)"}
 
 
def fetch(url, as_json=False, timeout=45):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
    if as_json:
        return json.loads(raw.decode("utf-8"))
    return raw.decode("utf-8", "replace")
 
 
# ----------------------------------------------------------------------------
def _ca_date(v):
    """Το 'Date of Last Corporate Action' είναι είτε dict {date:...} είτε None."""
    if isinstance(v, dict):
        return (v.get("date") or "")[:10]
    if isinstance(v, str):
        return v[:10]
    return ""
 
 
def load_stocks():
    """-> dict Symbol -> {segment,status,isin,ca_type,ca_date,mcap,company}"""
    j = fetch(STOCKS_JSON, as_json=True)
    out = {}
    for e in j.get("data", []):
        sym = (e.get("Symbol") or "").strip()
        if not sym:
            continue
        status = (e.get("Trading Status") or "").split("|")[0].strip()
        out[sym] = {
            "segment":  (e.get("Market Segment") or "").strip(),
            "status":   status,
            "isin":     (e.get("ISIN") or "").strip(),
            "ca_type":  (e.get("Type of Last Corporate Action") or "").strip(),
            "ca_date":  _ca_date(e.get("Date of Last Corporate Action")),
            "mcap":     (e.get("Market Capitalisation") or "").strip(),
            "company":  (e.get("_productId") or sym),  # φιλικό ref
        }
    return out, j.get("lastUpdated")
 
 
def _cell(tr, cls):
    td = tr.find("td", class_=cls)
    return td.get_text(strip=True) if td else ""
 
 
def load_distributions():
    """-> list of dicts + key. Τραβάει CASH_PAGES σελίδες."""
    rows = []
    seen_keys = set()
    for p in range(CASH_PAGES):
        url = CASH_URL + (("?page=%d" % p) if p else "")
        try:
            html = fetch(url)
        except Exception as ex:
            print("Προσοχή: αποτυχία σελίδας διανομών %s (%s)" % (url, ex), file=sys.stderr)
            break
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", class_="view-table")
        if not table:
            break
        body = table.find("tbody") or table
        page_rows = body.find_all("tr")
        if not page_rows:
            break
        for tr in page_rows:
            sym = _cell(tr, "field--symbol")
            if not sym:
                continue
            rec = {
                "company": _cell(tr, "field--company-name"),
                "symbol":  sym,
                "price":   _cell(tr, "field--price-in-€"),  # field--price-in-€
                "type":    _cell(tr, "field--type"),
                "ex":      _cell(tr, "field--ex-date"),
                "pay":     _cell(tr, "field--start-payment-date"),
                "fiscal":  _cell(tr, "field--fiscal-year"),
            }
            key = "%s|%s|%s|%s" % (rec["symbol"], rec["ex"], rec["type"], rec["price"])
            if key in seen_keys:
                continue
            seen_keys.add(key)
            rec["key"] = key
            rows.append(rec)
    return rows
 
 
# ----------------------------------------------------------------------------
def build_snapshot(stocks, dists):
    """Μόνο το ουσιώδες state — χωρίς volatile timestamps ώστε το git diff
    να δείχνει αλλαγή ΜΟΝΟ όταν αλλάζει πραγματικά κάτι."""
    return {
        "stocks": {
            s: {
                "segment": v["segment"],
                "status":  v["status"],
                "isin":    v["isin"],
                "ca_type": v["ca_type"],
                "ca_date": v["ca_date"],
            } for s, v in stocks.items()
        },
        "distributions": sorted(r["key"] for r in dists),
    }
 
 
def load_prev_snapshot():
    if not os.path.exists(SNAP_PATH):
        return None
    try:
        with open(SNAP_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None
 
 
def diff(prev, stocks, dists):
    """Επιστρέφει dict με τις κατηγορίες αλλαγών."""
    old = (prev or {}).get("stocks", {})
    old_dist = set((prev or {}).get("distributions", []))
 
    new_syms = [s for s in stocks if s not in old]
    gone_syms = [s for s in old if s not in stocks]
 
    seg_changes, status_changes, ca_changes = [], [], []
    for s, v in stocks.items():
        o = old.get(s)
        if not o:
            continue
        if o.get("segment") != v["segment"]:
            seg_changes.append((s, o.get("segment", ""), v["segment"]))
        if o.get("status") != v["status"]:
            status_changes.append((s, o.get("status", ""), v["status"]))
        # Σκανδάλη μεταβολής κεφαλαίου: νέα ΑΜΚ (αγνοούμε τα ΜΕΡΙΣΜΑ εδώ,
        # καλύπτονται δομημένα από τις διανομές).
        if (o.get("ca_type"), o.get("ca_date")) != (v["ca_type"], v["ca_date"]) \
           and v["ca_type"] and "ΚΕΦΑΛΑΙΟ" in v["ca_type"].upper():
            ca_changes.append((s, v["ca_type"], v["ca_date"]))
 
    new_dists = [r for r in dists if r["key"] not in old_dist]
 
    return {
        "new_syms": new_syms,
        "gone_syms": gone_syms,
        "seg_changes": seg_changes,
        "status_changes": status_changes,
        "ca_changes": ca_changes,
        "new_dists": new_dists,
    }
 
 
def has_any(ch):
    return any(ch[k] for k in
               ("new_syms", "gone_syms", "seg_changes",
                "status_changes", "ca_changes", "new_dists"))
 
 
# ----------------------------------------------------------------------------
def render_report(ch, stocks, first_run, gen_dt):
    L = []
    L.append("# 🛰️ Euronext Monitor — %s" % gen_dt)
    L.append("")
    if first_run:
        L.append("**Baseline.** Πρώτη εκτέλεση — αποθηκεύτηκε το αρχικό snapshot "
                 "(%d εταιρείες). Καμία σύγκριση. Οι επόμενες εκτελέσεις θα "
                 "αναφέρουν μόνο αλλαγές." % len(stocks))
        return "\n".join(L)
 
    if not has_any(ch):
        L.append("Καμία αλλαγή από την προηγούμενη εκτέλεση. ✅")
        return "\n".join(L)
 
    def name(sym):
        return sym
 
    if ch["status_changes"]:
        L.append("## ⏸️ Αλλαγές κατάστασης διαπραγμάτευσης")
        L.append("")
        for s, o, n in ch["status_changes"]:
            L.append("- **%s**: %s → **%s**" %
                     (name(s), STATUS_LABEL.get(o, o or "—"),
                      STATUS_LABEL.get(n, n or "—")))
        L.append("")
 
    if ch["seg_changes"]:
        L.append("## 🔁 Αλλαγές κατηγορίας αγοράς (segment)")
        L.append("")
        for s, o, n in ch["seg_changes"]:
            L.append("- **%s**: %s → **%s**" % (name(s), o or "—", n or "—"))
        L.append("")
 
    if ch["gone_syms"]:
        L.append("## ❌ Πιθανές διαγραφές (εξαφανίστηκαν από το Euronext)")
        L.append("")
        for s in ch["gone_syms"]:
            L.append("- **%s** — επιβεβαίωσε στη σελίδα «Διεγραμμένες Εταιρείες»." % name(s))
        L.append("")
 
    if ch["new_syms"]:
        L.append("## 🆕 Νέες εισαγωγές (νέα σύμβολα)")
        L.append("")
        for s in ch["new_syms"]:
            v = stocks[s]
            L.append("- **%s** — %s%s" %
                     (name(s), v["segment"] or "—",
                      (", ISIN %s" % v["isin"]) if v["isin"] else ""))
        L.append("")
 
    if ch["new_dists"]:
        L.append("## 💰 Νέες χρηματικές διανομές")
        L.append("")
        L.append("| Εταιρεία | Σύμβολο | Ποσό € | Τύπος | Αποκοπή | Πληρωμή | Χρήση |")
        L.append("|---|---|---|---|---|---|---|")
        for r in ch["new_dists"]:
            L.append("| %s | %s | %s | %s | %s | %s | %s |" %
                     (r["company"], r["symbol"], r["price"], r["type"],
                      r["ex"] or "—", r["pay"] or "—", r["fiscal"] or "—"))
        L.append("")
 
    if ch["ca_changes"]:
        L.append("## 💠 Σκανδάλη μεταβολής μετοχικού κεφαλαίου")
        L.append("")
        L.append("_Το Euronext δηλώνει νέα «τελευταία εταιρική πράξη» τύπου "
                 "κεφαλαίου. Δες την ανακοίνωση για λεπτομέρειες (ΑΜΚ, split κ.λπ.)._")
        L.append("")
        for s, t, d in ch["ca_changes"]:
            L.append("- **%s**: %s (%s)" % (name(s), t, d or "—"))
        L.append("")
 
    L.append("---")
    L.append("_Υπενθύμιση: ο monitor δεν αλλάζει το master ούτε το site. "
             "Καταχώρησε ό,τι ισχύει στο ΑΡΙΘΜΟΔΕΙΚΤΕΣ.xlsx._")
    return "\n".join(L)
 
 
# ----------------------------------------------------------------------------
def gh_output(key, val):
    p = os.environ.get("GITHUB_OUTPUT")
    if p:
        with open(p, "a", encoding="utf-8") as f:
            f.write("%s=%s\n" % (key, val))
 
 
def step_summary(md):
    p = os.environ.get("GITHUB_STEP_SUMMARY")
    if p:
        with open(p, "a", encoding="utf-8") as f:
            f.write(md + "\n")
 
 
def main():
    gen_dt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    prev = load_prev_snapshot()
    first_run = prev is None
 
    stocks, _ = load_stocks()
    dists = load_distributions()
    if not stocks:
        print("Σφάλμα: άδειο stocks_details.", file=sys.stderr)
        sys.exit(1)
 
    ch = diff(prev, stocks, dists)
    changed = (not first_run) and has_any(ch)
 
    report = render_report(ch, stocks, first_run, gen_dt)
 
    os.makedirs(MON_DIR, exist_ok=True)
    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write(report + "\n")
 
    # Γράφουμε το snapshot ΠΑΝΤΑ (η επιτροπή γίνεται μόνο αν άλλαξε ουσιαστικά).
    snap = build_snapshot(stocks, dists)
    with open(SNAP_PATH, "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=1, sort_keys=True)
 
    step_summary(report)
    gh_output("has_changes", "true" if changed else "false")
    gh_output("first_run", "true" if first_run else "false")
 
    print(report)
    print("\n[monitor] stocks=%d distributions=%d changed=%s first_run=%s"
          % (len(stocks), len(dists), changed, first_run))
 
 
if __name__ == "__main__":
    main()
 
