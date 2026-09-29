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
import re
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
SNAP_PATH  = os.path.join(MON_DIR, "snapshot.json")
REPORT_MD  = os.path.join(MON_DIR, "last_report.md")
QUEUE_PATH = os.path.join(MON_DIR, "events_queue.csv")
 
# Στήλες ουράς — ό,τι χρειάζεται το apply_events.py για να χτίσει τη γραμμή
# ΕΤΑΙΡΙΚΑ ΓΕΓΟΝΟΤΑ (η ανάλυση symbol->όνομα master γίνεται στο apply, από το INDEX).
QUEUE_COLS = ["detected_on", "euronext_symbol", "euronext_company", "date",
              "family", "category", "type", "description", "amount_eur",
              "fiscal_year", "source_title", "needs_detail", "event_key"]
 
# family -> Κατηγορία (ακριβώς όπως στο master)
CATEGORY = {
    "div":     "Μέρισμα / Διανομή",
    "capital": "Κεφαλαιακή πράξη",
    "crit":    "Διαπραγμάτευση / Εταιρικό",
    "listing": "Εισαγωγή / Κατηγορία",
}
 
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
        stq = (e.get("Trading Status") or "").split("|")
        st_change = stq[1][:10] if len(stq) > 1 else ""
        out[sym] = {
            "segment":  (e.get("Market Segment") or "").strip(),
            "status":   status,
            "st_change_date": st_change,
            "isin":     (e.get("ISIN") or "").strip(),
            "ca_type":  (e.get("Type of Last Corporate Action") or "").strip(),
            "ca_date":  _ca_date(e.get("Date of Last Corporate Action")),
            "mcap":     (e.get("Market Capitalisation") or "").strip(),
            "company":  (e.get("Symbol") or sym).strip(),
            "name_full": (e.get("_productId") or sym),
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
DIST_MEMORY = 600   # πόσα κλειδιά διανομών κρατά η μνήμη του snapshot


def build_snapshot(stocks, dists, prev=None):
    """Μόνο το ουσιώδες state — χωρίς volatile timestamps ώστε το git diff
    να δείχνει αλλαγή ΜΟΝΟ όταν αλλάζει πραγματικά κάτι.

    §123 — ΟΙ ΔΙΑΝΟΜΕΣ ΕΙΝΑΙ ΕΝΩΣΗ, ΟΧΙ ΣΤΙΓΜΙΟΤΥΠΟ.
    Η σελίδα διανομών δίνει σταθερά CASH_PAGES*10 = 20 γραμμές, ταξινομημένες
    φθίνουσα κατά αποκοπή. Όταν πολλές εταιρείες έχουν ΤΗΝ ΙΔΙΑ ημερομηνία
    αποκοπής στο κάτω όριο του παραθύρου (π.χ. έξι στις 20/07/2026), το ποιες
    δύο από αυτές χωράνε στις τελευταίες θέσεις ΔΕΝ είναι σταθερό — δεν υπάρχει
    δευτερεύον κριτήριο ταξινόμησης. Έτσι σε κάθε τρέξιμο έμπαινε στο παράθυρο
    άλλο υποσύνολο, και το προηγούμενο snapshot (που κρατούσε ΜΟΝΟ τις 20 της
    στιγμής) το έβλεπε ως «νέα διανομή» — δίμηνα παλιά γεγονότα εμφανίζονταν
    στάγδην ως νέα. Κρατώντας ένωση, ό,τι έχει ξαναδεί ο monitor μένει «γνωστό».
    """
    keep = sorted(set(r["key"] for r in dists) |
                  set((prev or {}).get("distributions", [])))[-DIST_MEMORY:]
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
        "distributions": keep,
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
# Κανονικοποίηση αλλαγών -> γραμμές ουράς (schema ΕΤΑΙΡΙΚΑ ΓΕΓΟΝΟΤΑ)
# ----------------------------------------------------------------------------
def _strip_tonos(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")
 
 
def _iso(dmy):
    """'17/08/2026' -> '2026-08-17'· ό,τι άλλο επιστρέφεται ως έχει."""
    dmy = (dmy or "").strip()
    parts = dmy.split("/")
    if len(parts) == 3 and all(parts):
        d, m, y = parts
        return "%s-%s-%s" % (y, m.zfill(2), d.zfill(2))
    return dmy
 
 
def _src_date(iso):
    """'2026-08-17' -> '17 - 08 - 2026' (μορφή τίτλου πηγής του master)."""
    p = (iso or "").split("-")
    if len(p) == 3:
        return "%s - %s - %s" % (p[2], p[1], p[0])
    return iso or ""
 
 
def _ev(sym, comp, date_iso, fam, typ, desc, src, detected_on, needs=False,
        amount="", fiscal=""):
    key = "%s|%s|%s" % (sym, date_iso, typ)
    return {
        "detected_on": detected_on,
        "euronext_symbol": sym,
        "euronext_company": comp or sym,
        "date": date_iso,
        "family": fam,
        "category": CATEGORY.get(fam, ""),
        "type": typ,
        "description": desc,
        # amount_eur -> στήλη M «Ποσό €/μτχ» του master· fiscal_year -> στήλη N «Χρήση».
        # Μόνο για διανομές (div/capital)· τα άλλα events μένουν κενά.
        "amount_eur": amount,
        "fiscal_year": fiscal,
        "source_title": src,
        "needs_detail": "1" if needs else "",
        "event_key": key,
    }
 
 
def build_events(ch, stocks, detected_on):
    """Μετατρέπει το diff σε λίστα γεγονότων έτοιμων για το master."""
    ev = []
 
    # Διανομές (ακριβή)
    for r in ch["new_dists"]:
        sym = r["symbol"]
        diso = _iso(r["ex"])
        t = _strip_tonos((r["type"] or "").upper())
        price = r["price"]
        if "ΜΕΡΙΣΜ" in t:
            fam, typ = "div", "dividend"
            desc = "Διανομή €%s/μετοχή" % price if price else "Διανομή μερίσματος"
        elif "ΚΕΦΑΛΑ" in t:   # «ΕΠΙΣΤΡΟΦΗ ΚΕΦΑΛΑΙΟΥ» (τονο-ανεξάρτητο)
            fam, typ = "capital", "capital_return"
            desc = "Επιστροφή κεφαλαίου €%s/μετοχή" % price if price else "Επιστροφή κεφαλαίου"
        else:
            fam, typ = "div", "dividend"
            desc = "%s €%s/μετοχή" % (r["type"], price) if price else r["type"]
        src = "%s ΧΡΗΜΑΤΙΚΗ ΔΙΑΝΟΜΗ %s" % (r["company"], _src_date(diso))
        # amount σε καθαρό αριθμό (τελεία δεκαδικό)· fiscal = χρήση όπως τη δίνει το Euronext
        _p = (price or "").strip()
        if "," in _p and "." in _p: amount = _p.replace(".", "").replace(",", ".")
        elif "," in _p:             amount = _p.replace(",", ".")
        else:                       amount = _p
        fiscal = (r.get("fiscal") or "").strip()
        ev.append(_ev(sym, r["company"], diso, fam, typ, desc, src, detected_on,
                      amount=amount, fiscal=fiscal))
 
    # Αναστολή / επαναφορά διαπραγμάτευσης
    for sym, o, n in ch["status_changes"]:
        d = stocks.get(sym, {}).get("st_change_date") or detected_on
        if n == "0":
            ev.append(_ev(sym, sym, d, "crit", "suspension",
                          "Αναστολή διαπραγμάτευσης", "Euronext — αλλαγή κατάστασης",
                          detected_on))
        elif n == "1":
            ev.append(_ev(sym, sym, d, "crit", "resume",
                          "Επαναφορά σε διαπραγμάτευση", "Euronext — αλλαγή κατάστασης",
                          detected_on))
 
    # Διαγραφές
    for sym in ch["gone_syms"]:
        ev.append(_ev(sym, sym, detected_on, "crit", "delisting",
                      "Διαγραφή από το Euronext (επιβεβαίωση: Διεγραμμένες Εταιρείες)",
                      "Euronext — εξαφάνιση συμβόλου", detected_on, needs=True))
 
    # Νέες εισαγωγές
    for sym in ch["new_syms"]:
        seg = stocks.get(sym, {}).get("segment", "")
        ev.append(_ev(sym, sym, detected_on, "listing", "market_change",
                      "Νέα εισαγωγή προς διαπραγμάτευση%s" % ((" — %s" % seg) if seg else ""),
                      "Euronext — νέο σύμβολο", detected_on, needs=True))
 
    # Αλλαγές segment (μεταφορά κατηγορίας)
    for sym, o, n in ch["seg_changes"]:
        ev.append(_ev(sym, sym, detected_on, "listing", "market_change",
                      "Μεταφορά κατηγορίας: %s → %s" % (o or "—", n or "—"),
                      "Euronext — αλλαγή κατηγορίας αγοράς", detected_on))
 
    # Σκανδάλη ΑΜΚ (χρειάζεται λεπτομέρεια από ανακοίνωση)
    for sym, t, d in ch["ca_changes"]:
        ev.append(_ev(sym, sym, d or detected_on, "capital", "amk",
                      "Μεταβολή μετοχικού κεφαλαίου — έλεγξε ανακοίνωση (υποείδος/ποσό)",
                      "Euronext — %s" % t, detected_on, needs=True))
 
    return ev
 
 
# ----------------------------------------------------------------------------
# §123 — ΔΙΧΤΥ ΑΣΦΑΛΕΙΑΣ: ήδη καταχωρημένα & πολύ παλιά
# ----------------------------------------------------------------------------
DATA_JS   = os.path.normpath(os.path.join(HERE, "..", "..", "assets", "data.js"))
STALE_DAYS = 30   # πέρα από τόσες ημέρες, το γεγονός θεωρείται «παλιό»


def _known_from_data_js():
    """Κλειδιά «ημερομηνία|ποσό» των ΗΔΗ καταχωρημένων χρηματικών διανομών.

    Το data.js είναι το παραγόμενο του master — ό,τι υπάρχει εκεί έχει ήδη
    περάσει στα ΕΤΑΙΡΙΚΑ ΓΕΓΟΝΟΤΑ. Δεν αντιστοιχίζουμε με σύμβολο Euronext
    (τα σύμβολα διαφέρουν από τα ονόματα του master· η αντιστοίχιση γίνεται
    στο apply_events.py από το INDEX), αλλά με ΗΜΕΡΟΜΗΝΙΑ + ΠΟΣΟ, που είναι
    αρκετά διακριτικό ζεύγος για διανομή.
    """
    if not os.path.exists(DATA_JS):
        return set()
    try:
        with open(DATA_JS, encoding="utf-8") as f:
            txt = f.read()
        i = txt.index('"marketEvents"')
        j = txt.index("[", i)
        depth = 0
        for k in range(j, len(txt)):
            if txt[k] == "[":
                depth += 1
            elif txt[k] == "]":
                depth -= 1
                if depth == 0:
                    break
        out = set()
        for e in json.loads(txt[j:k + 1]):
            if e.get("t") not in ("div", "capital"):
                continue
            m = re.search(r"€\s*([0-9][0-9.,]*)", e.get("x", "") or "")
            if m:
                a = _amt(m.group(1))
                if a:
                    out.add("%s|%s" % (e.get("d", ""), a))
        return out
    except Exception as exc:                      # ποτέ δεν ρίχνει το job
        print("[monitor] ΠΡΟΣΟΧΗ: αδύνατη η ανάγνωση data.js (%s)" % exc,
              file=sys.stderr)
        return set()


def _amt(v):
    """Κανονικοποίηση ποσού σε «0.6000».

    ΠΡΟΣΟΧΗ στις δύο μορφές: η ουρά γράφει «0.6000» (τελεία = δεκαδικό, μορφή
    CSV), το data.js «0,6000» (κόμμα = δεκαδικό, ελληνική μορφή). Τυφλή αφαίρεση
    των τελειών μετατρέπει το «0.0606» σε 606 — γι' αυτό η μορφή κρίνεται από
    το αν υπάρχει κόμμα.
    """
    t = str(v or "").strip()
    if not t:
        return ""
    if "," in t:
        t = t.replace(".", "").replace(",", ".")   # ελληνική: τελεία = χιλιάδες
    try:
        return "%.4f" % float(t)
    except Exception:
        return ""


def _age_days(date_iso, detected_on):
    try:
        a = datetime.date.fromisoformat(date_iso)
        b = datetime.date.fromisoformat(detected_on)
        return (b - a).days
    except Exception:
        return 0


def annotate(events, detected_on):
    """Χωρίζει σε (νέα, ήδη γνωστά, παλιά). ΤΙΠΟΤΑ δεν πετιέται σιωπηλά."""
    known = _known_from_data_js()
    fresh, dup, stale = [], [], []
    for e in events:
        amt = _amt(e.get("amount_eur"))
        if amt and ("%s|%s" % (e["date"], amt)) in known:
            dup.append(e)
        elif _age_days(e["date"], detected_on) > STALE_DAYS:
            stale.append(e)
        else:
            fresh.append(e)
    return fresh, dup, stale


def _read_queue_keys():
    keys = set()
    if os.path.exists(QUEUE_PATH):
        import csv
        with open(QUEUE_PATH, encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                if row.get("event_key"):
                    keys.add(row["event_key"])
    return keys
 
 
def write_queue(events):
    """Append-only ουρά, με dedup στο event_key. Επιστρέφει πλήθος νέων."""
    import csv
    existing = _read_queue_keys()
    fresh = [e for e in events if e["event_key"] not in existing]
    if not fresh:
        return 0
    new_file = not os.path.exists(QUEUE_PATH)
    with open(QUEUE_PATH, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=QUEUE_COLS)
        if new_file:
            w.writeheader()
        for e in fresh:
            w.writerow(e)
    return len(fresh)
 
 
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
 
    # Ουρά γεγονότων για το master (μόνο εκτός baseline).
    queued = 0
    if changed:
        events = build_events(ch, stocks, gen_dt[:10])
        # §123 — τριχοτόμηση πριν την ουρά: νέα / ήδη στο data.js / παλιά.
        # Στην ουρά μπαίνουν ΜΟΝΟ τα νέα· τα άλλα δύο αναφέρονται ώστε να
        # φαίνονται, αλλά δεν λερώνουν το apply.
        fresh, dup, stale = annotate(events, gen_dt[:10])
        queued = write_queue(fresh)
        if queued:
            report += ("\n\n> 📥 %d νέα γεγονότα προστέθηκαν στην ουρά "
                       "`events_queue.csv` — θα περάσουν στο master με το "
                       "επόμενο apply." % queued)
        if dup:
            report += ("\n\n> ♻️ %d γεγονότα **παραλείφθηκαν** — υπάρχουν ήδη "
                       "στο `assets/data.js` (ίδια ημερομηνία & ποσό): %s"
                       % (len(dup), ", ".join("%s %s" % (e["euronext_symbol"],
                                                         e["date"]) for e in dup)))
        if stale:
            report += ("\n\n> 🕰️ %d γεγονότα **παλαιότερα των %d ημερών** — δεν "
                       "μπήκαν στην ουρά, έλεγξέ τα χειροκίνητα: %s"
                       % (len(stale), STALE_DAYS,
                          ", ".join("%s %s (%d ημ.)" % (e["euronext_symbol"], e["date"],
                                                        _age_days(e["date"], gen_dt[:10]))
                                    for e in stale)))
 
    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write(report + "\n")
 
    # Γράφουμε το snapshot ΠΑΝΤΑ (η επιτροπή γίνεται μόνο αν άλλαξε ουσιαστικά).
    snap = build_snapshot(stocks, dists, prev)
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
 
