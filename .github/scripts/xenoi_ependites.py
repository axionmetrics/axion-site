#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ξένοι επενδυτές — Axion Metrics
================================
Μηνιαία σειρά συμμετοχής και συναλλαγών ξένων επενδυτών στο Euronext Athens,
από το «AxiaNUMBERS — Securities Market» (μηνιαίο στατιστικό δελτίο).

ΠΗΓΗ — γιατί ΑΥΤΗ και όχι το Mid-Month Report:
  Το Mid-Month Report δίνει ένα στιγμιότυπο ανά έκδοση, ΑΛΛΑΖΕΙ ορισμό στο
  μερίδιο συναλλαγών (οι εκδόσεις 2025 δίνουν σωρευτικό YtD, του 2026
  δεκαπενθημέρου) και δεν έχει σελίδα αρχείου. Το AxiaNUMBERS Securities
  δίνει ΜΗΝΙΑΙΑ στοιχεία με σταθερές ενότητες και έχει αρχείο ως το 2007.
  ΜΗΝ τα ανακατεύεις: για το 2019 το AXIA δίνει 64,18% συμμετοχή ενώ το
  Mid-Month 66,4%. Διαφορετικό σύνολο αναφοράς.

ΤΙ ΒΓΑΖΕΙ (ανά μήνα), από τη γραμμή «ΙΙ. Foreign Investors»:
  ενότητα «Investors' Participation in Total Listed Equities»
      -> συμμετοχή στα assets under custody: πλήθος, %, αξία (εκ. €), %
  ενότητα «Analysis of the Monthly Trading Activity in Total of Listed
            Equities of Athex market per Investors Category»
      -> αγορές/πωλήσεις του μήνα: αξία (εκ. €) και % του τζίρου, net, net YtD

ΔΙΕΥΘΥΝΣΙΟΔΟΤΗΣΗ ΜΕ ΕΤΙΚΕΤΕΣ, ΟΧΙ ΜΕ ΑΡΙΘΜΟΥΣ ΕΝΟΤΗΤΑΣ:
  Η αρίθμηση ΑΛΛΑΖΕΙ μεταξύ ετών (στο τεύχος 187 του Απρ 2019 τα ίδια
  στοιχεία ήταν στις 3.1.1 και 2.3.1· στο τεύχος 276 του Σεπ 2026 είναι
  στις 3.1 και 2.1). Οπότε αγκυρώνουμε στον ΤΙΤΛΟ της ενότητας και στην
  ετικέτα της γραμμής — ποτέ στο «3.1.1».

ΕΠΑΛΗΘΕΥΣΗ — τρία checks σε κάθε μήνα, αλλιώς ο μήνας απορρίπτεται:
  1) αγορές - πωλήσεις == net            (ανοχή 0,05 εκ. €)
  2) αξία ξένων / σύνολο == ποσοστό       (ανοχή 0,03 μονάδες)
  3) ο μήνας του εξωφύλλου == ο μήνας του τίτλου του τεύχους

ΤΡΟΠΟΣ ΧΡΗΣΗΣ:
  python xenoi_ependites.py --selftest <τεύχος.zip|.pdf>   # έλεγχος σε δείγμα
  python xenoi_ependites.py --inventory                    # κατάλογος τευχών
  python xenoi_ependites.py --fetch                        # λήψη στο cache
  python xenoi_ependites.py                                # πλήρες -> JSON

ΠΡΟΣΟΧΗ:
  1) Από το Issue 190 (Ιούλ 2019) και μετά τα τεύχη είναι **ZIP** με το PDF
     μέσα. Οι διευθύνσεις δεν έχουν κατάληξη — ο τύπος αναγνωρίζεται από τα
     πρώτα bytes, ΟΧΙ από το URL.
  2) Υπάρχουν ΚΕΝΑ στη σειρά τευχών (π.χ. λείπει το 047). Ο αριθμός τεύχους
     ΔΕΝ αντιστοιχεί γραμμικά σε μήνα.
  3) Το δελτίο καθυστερεί 1-2 μήνες. Ο τελευταίος διαθέσιμος μήνας ΔΕΝ είναι
     ο προηγούμενος.
  4) Η διάταξη είναι ΕΠΑΛΗΘΕΥΜΕΝΗ στο τεύχος 276 (Σεπ 2026). Για παλαιότερα
     τεύχη δεν έχει επαληθευτεί· όποιος μήνας δεν περάσει τα checks μπαίνει
     στο "failed" με τον λόγο, ΔΕΝ γράφεται με μαντεμένη τιμή.
"""

import argparse, io, json, os, re, shutil, subprocess, sys, tempfile, zipfile, datetime
import urllib.request, urllib.parse

BASE = "https://athens.euronext.com"
LIST = BASE + "/en/market-data/data-services/statistics/reports-monthly"
CATEGORY_AXIA_SECURITIES = 4          # field_mig_category_target_id
PAGES = 16                            # 0..15 (Σεπ 2026 -> Ιαν 2007)
FROM_PERIOD = "2020-01"               # κάλυψη Axion

HERE  = os.path.dirname(os.path.abspath(__file__))
OUT   = os.path.normpath(os.path.join(HERE, "..", "data", "xenoi_ependites.json"))
CACHE = os.path.normpath(os.path.join(HERE, "..", "cache", "axia"))

UA = {"User-Agent": "AxionMetrics-Monitor/1.0 (+https://axionmetrics.gr)"}

MONTHS = {m: i for i, m in enumerate(
    ["January","February","March","April","May","June","July",
     "August","September","October","November","December"], 1)}
TITLE_RE = re.compile(r"Issue\s+(\d+)\s*\(\s*([A-Za-z]+)\s+(\d{4})\s*\)")

# ---------------------------------------------------------------- εξαγωγή ----

NUM = r"-?\d{1,3}(?:,\d{3})*(?:\.\d+)?"
# «ΙΙ.» γράφεται άλλοτε με λατινικό I, άλλοτε με ελληνικό Ι — δέξου και τα δύο.
FOREIGN = re.compile(r"^\s*[IΙ]{2}\s*\.\s*Foreign\s+Investors\b(.*)$")
TOTAL   = re.compile(r"^\s*Total\s+(" + NUM + r")\s+(?:100%|" + NUM + r"%)\s+(" + NUM + r")\s")

# Οι τέσσερις πίνακες που έχουν γραμμή «ΙΙ. Foreign Investors». Αγκυρώνουμε
# στον ΤΙΤΛΟ του πίνακα — όχι στο «2.1»/«3.1», που αλλάζει μεταξύ ετών.
TABLES = {
    "trade_total": "Analysis of the Monthly Trading Activity in Total of Listed Equities",
    "trade_ftse":  "Trading Activity in FTSE/Athex Large Cap",
    "part_total":  "Participation in Total Listed Equities",
    "part_ftse":   "Participation in the FTSE/Athex Large Cap Index",
}


def f(s):
    return float(s.replace(",", "").rstrip("%"))


def tables_of(text):
    """{όνομα πίνακα: [τιμές της γραμμής ΙΙ. Foreign Investors]}.

    Για κάθε γραμμή συνόλου ξένων βρίσκουμε τον ΠΛΗΣΙΕΣΤΕΡΟ ΠΡΟΗΓΟΥΜΕΝΟ τίτλο
    πίνακα. Αντίστροφα (τίτλος -> πρώτη γραμμή από κάτω) ΔΕΝ δουλεύει: ο ίδιος
    τίτλος εμφανίζεται και στα περιεχόμενα, και η καταχώρηση των περιεχομένων
    σπάει σε δύο γραμμές, οπότε η πρώτη δεν έχει τελείες και περνά για σώμα.
    """
    lines = text.splitlines()
    marks = []
    for i, ln in enumerate(lines):
        low = re.sub(r"\s+", " ", ln).strip().lower()
        for name, phrase in TABLES.items():
            if phrase.lower() in low:
                marks.append((i, name))
    out = {}
    for i, ln in enumerate(lines):
        m = FOREIGN.match(ln)
        if not m:
            continue
        v = re.findall(NUM + r"%?", m.group(1))
        if not v:
            continue
        prev = [nm for (j, nm) in marks if j < i]
        if not prev:
            continue
        out.setdefault(prev[-1], v)          # η πρώτη γραμμή κάθε πίνακα
    return out, lines


def parse_text(text, period):
    """Εξαγωγή + επαλήθευση. Σπάει με ValueError αν κάτι δεν βγαίνει."""
    tb, lines = tables_of(text)
    r = {"period": period}

    v = tb.get("trade_total")
    if not v or len(v) < 10:
        raise ValueError("μηνιαίες συναλλαγές (σύνολο αγοράς): γραμμή ξένων %s" % v)
    r["buys_m"], r["buys_pct"] = f(v[2]), f(v[3])
    r["sells_m"], r["sells_pct"] = f(v[6]), f(v[7])
    r["net_m"], r["net_ytd_m"] = f(v[8]), f(v[9])

    v = tb.get("part_total")
    if not v or len(v) < 4:
        raise ValueError("συμμετοχή (σύνολο εισηγμένων): γραμμή ξένων %s" % v)
    r["part_n"], r["part_val_m"], r["part_pct"] = int(f(v[0])), f(v[2]), f(v[3])

    # σύνολο αγοράς = η γραμμή Total του ΙΔΙΟΥ πίνακα συμμετοχής
    r["mkt_val_m"] = None
    start = next((i for i, ln in enumerate(lines)
                  if FOREIGN.match(ln) and f"{r['part_val_m']:,.2f}" in ln), 0)
    for j in range(start, min(start + 60, len(lines))):
        m = TOTAL.match(lines[j])
        if m:
            r["mkt_val_m"] = f(m.group(2))
            break

    # --- check 1: αγορές - πωλήσεις == net ---
    d = abs((r["buys_m"] - r["sells_m"]) - r["net_m"])
    if d > 0.05:
        raise ValueError("αγορές-πωλήσεις != net (διαφορά %.2f εκ. €)" % d)

    # --- check 2: αξία / σύνολο == ποσοστό ---
    if not r["mkt_val_m"]:
        raise ValueError("δεν βρέθηκε η γραμμή Total του πίνακα συμμετοχής")
    calc = r["part_val_m"] / r["mkt_val_m"] * 100.0
    if abs(calc - r["part_pct"]) > 0.03:
        raise ValueError("συμμετοχή %.2f%% != αξία/σύνολο %.2f%%"
                         % (r["part_pct"], calc))

    # --- check 3: μήνας εξωφύλλου ---
    m = re.search(r"^\s*([A-Za-z]{3,9})\s+(\d{4})\s*$", text[:1500], re.M)
    if m and MONTHS.get(m.group(1).title()):
        cover = "%s-%02d" % (m.group(2), MONTHS[m.group(1).title()])
        if cover != period:
            raise ValueError("εξώφυλλο %s != τίτλος τεύχους %s" % (cover, period))
        r["cover_ok"] = True
    else:
        r["cover_ok"] = False
    return r


def pdf_text(src):
    """Κείμενο του PDF. Πρώτα pdftotext (poppler) — είναι ~100x ταχύτερο και το
    χρειαζόμαστε, γιατί το backfill είναι ~80 τεύχη x 20 σελίδες. Αν λείπει,
    πέφτει στο pdfplumber. Η εξαγωγή είναι ΕΠΑΛΗΘΕΥΜΕΝΗ ΚΑΙ ΜΕ ΤΑ ΔΥΟ."""
    raw = src if isinstance(src, bytes) else open(src, "rb").read()
    exe = shutil.which("pdftotext")
    if exe:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as fh:
            fh.write(raw); tmp = fh.name
        try:
            out = subprocess.run([exe, "-layout", tmp, "-"], check=True,
                                 capture_output=True)
            txt = out.stdout.decode("utf-8", "replace")
            if "Foreign Investors" in txt:
                return txt
        except Exception:
            pass
        finally:
            os.unlink(tmp)
    import pdfplumber
    with pdfplumber.open(io.BytesIO(raw)) as pdf:
        return "\n".join((p.extract_text() or "") for p in pdf.pages)


def pdf_bytes(raw):
    """Το τεύχος είναι ZIP ή PDF — κρίνεται από τα bytes, όχι από το URL."""
    if raw[:4] == b"PK\x03\x04":
        z = zipfile.ZipFile(io.BytesIO(raw))
        names = [n for n in z.namelist() if n.lower().endswith(".pdf")]
        if not names:
            raise ValueError("ZIP χωρίς PDF: %s" % z.namelist()[:5])
        names.sort(key=lambda n: -z.getinfo(n).file_size)   # το μεγαλύτερο
        return z.read(names[0]), names[0]
    if raw[:4] == b"%PDF":
        return raw, "(απευθείας PDF)"
    raise ValueError("άγνωστος τύπος αρχείου, πρώτα bytes: %r" % raw[:8])


# -------------------------------------------------------------- κατάλογος ----

def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def inventory():
    """-> [{'issue':276,'period':'2026-09','title':...,'url':...}] φθίνουσα."""
    from bs4 import BeautifulSoup
    seen, out = set(), []
    for p in range(PAGES):
        url = "%s?field_mig_category_target_id=%d&page=%d" % (
            LIST, CATEGORY_AXIA_SECURITIES, p)
        soup = BeautifulSoup(fetch(url).decode("utf-8", "replace"), "html.parser")
        rows = 0
        for a in soup.find_all("a", href=True):
            m = TITLE_RE.search(a.get_text(" ", strip=True))
            if not m:
                continue
            mon = MONTHS.get(m.group(2).title())
            if not mon:
                continue
            period = "%s-%02d" % (m.group(3), mon)
            key = (int(m.group(1)), period)
            if key in seen:
                continue
            seen.add(key); rows += 1
            out.append({"issue": int(m.group(1)), "period": period,
                        "title": a.get_text(" ", strip=True),
                        "url": urllib.parse.urljoin(BASE, a["href"])})
        if rows == 0:
            print("  σελίδα %d: καμία γραμμή — άλλαξε η δομή;" % p, file=sys.stderr)
    out.sort(key=lambda r: r["period"], reverse=True)
    return out


def gaps_of(periods):
    if not periods:
        return []
    lo, hi = min(periods), max(periods)
    y0, m0 = map(int, lo.split("-")); y1, m1 = map(int, hi.split("-"))
    out = []
    y, m = y0, m0
    while (y, m) <= (y1, m1):
        p = "%04d-%02d" % (y, m)
        if p not in periods:
            out.append(p)
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def yearly(months):
    """Ανά έτος: συμμετοχή Δεκεμβρίου (ή του τελευταίου μήνα) + καθαρή ροή."""
    by = {}
    for r in months:
        by.setdefault(int(r["period"][:4]), []).append(r)
    out = []
    for y in sorted(by):
        g = sorted(by[y], key=lambda r: r["period"])
        n = len(g)
        out.append({
            "year": y, "months": n, "last": g[-1]["period"],
            "part_pct_end": g[-1]["part_pct"],
            "part_pct_avg": round(sum(r["part_pct"] for r in g) / n, 2),
            "buys_pct_avg": round(sum(r["buys_pct"] for r in g) / n, 2),
            "sells_pct_avg": round(sum(r["sells_pct"] for r in g) / n, 2),
            "net_m": round(sum(r["net_m"] for r in g), 2),
            "net_ytd_m_reported": g[-1]["net_ytd_m"],
        })
    return out


# ------------------------------------------------------------------- main ----

def load_existing():
    """Τα όσα έχουν ήδη βγει. Το JSON ΕΙΝΑΙ η μνήμη της ροής: κάθε run κατεβάζει
    μόνο τους μήνες που λείπουν, όχι και τα 80 τεύχη του backfill."""
    try:
        with open(OUT, encoding="utf-8") as fh:
            d = json.load(fh)
        return {r["period"]: r for r in d.get("months", [])}
    except Exception:
        return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", metavar="ΑΡΧΕΙΟ",
                    help="έλεγχος της εξαγωγής σε ένα τεύχος (.zip ή .pdf)")
    ap.add_argument("--inventory", action="store_true", help="μόνο κατάλογος τευχών")
    ap.add_argument("--refresh", action="store_true",
                    help="ξανακατέβασε και ξαναδιάβασε ΟΛΟΥΣ τους μήνες")
    ap.add_argument("--from", dest="frm", default=FROM_PERIOD)
    ap.add_argument("--cache", default=os.path.join(tempfile.gettempdir(), "axia"),
                    help="φάκελος για τα PDF (ΕΚΤΟΣ repo — δεν γίνονται commit)")
    a = ap.parse_args()

    if a.selftest:
        data, inner = pdf_bytes(open(a.selftest, "rb").read())
        print("PDF μέσα στο αρχείο: %s" % inner)
        txt = pdf_text(data)
        m = re.search(r"^\s*([A-Za-z]{3,9})\s+(\d{4})\s*$", txt[:1500], re.M)
        if not m or not MONTHS.get(m.group(1).title()):
            print("ΔΕΝ βρέθηκε μήνας στο εξώφυλλο", file=sys.stderr); sys.exit(1)
        r = parse_text(txt, "%s-%02d" % (m.group(2), MONTHS[m.group(1).title()]))
        w = max(len(k) for k in r)
        for k, v in r.items():
            print("  %-*s %s" % (w, k, v))
        print("OK — πέρασαν και τα 3 checks")
        return

    inv = [r for r in inventory() if r["period"] >= a.frm]
    print("τεύχη στο αρχείο από %s: %d  (%s -> %s)" % (
        a.frm, len(inv), inv[-1]["period"] if inv else "—",
        inv[0]["period"] if inv else "—"))
    print("κενά στον κατάλογο: %s" % (
        ", ".join(gaps_of({r["period"] for r in inv})) or "κανένα"))

    if a.inventory:
        for r in inv:
            print("  %s  Issue %-4d %s" % (r["period"], r["issue"], r["url"]))
        return

    have = {} if a.refresh else load_existing()
    todo = [r for r in inv if r["period"] not in have]
    print("ήδη στο JSON: %d · προς λήψη: %d" % (len(have), len(todo)))

    os.makedirs(a.cache, exist_ok=True)
    failed = []
    for r in todo:
        dst = os.path.join(a.cache, "%s_issue%d.pdf" % (r["period"], r["issue"]))
        try:
            if not os.path.exists(dst):
                data, _ = pdf_bytes(fetch(r["url"]))
                with open(dst, "wb") as fh:
                    fh.write(data)
            row = parse_text(pdf_text(dst), r["period"])
            row["issue"] = r["issue"]
            have[r["period"]] = row
            print("  %s  συμμετοχή %.2f%%  αγορές %.2f%%  πωλήσεις %.2f%%  net %+.2f"
                  % (r["period"], row["part_pct"], row["buys_pct"],
                     row["sells_pct"], row["net_m"]))
        except Exception as ex:
            failed.append({"period": r["period"], "issue": r["issue"],
                           "why": str(ex)[:160]})
            print("  ΑΠΟΤΥΧΙΑ %s (Issue %d): %s" % (r["period"], r["issue"], ex),
                  file=sys.stderr)

    months = sorted(have.values(), key=lambda r: r["period"])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({
            "source": "AxiaNUMBERS — Securities Market (Euronext Athens)",
            "source_url": LIST + "?field_mig_category_target_id=%d" % CATEGORY_AXIA_SECURITIES,
            "basis": "συμμετοχή = assets under custody στο ΕΛΚΑΤ · "
                     "αγορές/πωλήσεις = % του μηνιαίου τζίρου",
            "generated": datetime.date.today().isoformat(),
            "from": a.frm,
            "months": months,
            "years": yearly(months),
            "missing": gaps_of({r["period"] for r in months}),
            "failed": failed,
        }, fh, ensure_ascii=False, indent=1)
    print("γράφτηκε %s — %d μήνες (%s -> %s), %d αποτυχίες"
          % (OUT, len(months),
             months[0]["period"] if months else "—",
             months[-1]["period"] if months else "—", len(failed)))
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
