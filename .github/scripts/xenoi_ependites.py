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
  4) ΔΥΟ ΕΠΟΧΕΣ ΔΙΑΤΑΞΗΣ, και οι δύο ΕΠΑΛΗΘΕΥΜΕΝΕΣ σε πραγματικό τεύχος:
     τεύχος 196 (Ιαν 2020, παλιά) και τεύχος 276 (Σεπ 2026, νέα). Αλλάζουν
     τίτλοι ενοτήτων, πλήθος στηλών, γραφή αριθμού (ευρωπαϊκή/αμερικανική),
     ετικέτα γραμμής συνόλου και ο τρόπος που γράφεται η περίοδος. Όποιος
     μήνας δεν περάσει τους checks μπαίνει στο "failed" με τον λόγο — ΔΕΝ
     γράφεται ποτέ μαντεμένη τιμή.
  5) ΣΤΗΝ ΠΑΛΙΑ ΔΙΑΤΑΞΗ ο πίνακας συμμετοχής δίνει κεφαλαιοποίηση ΜΕ και ΧΩΡΙΣ
     ΤΧΣ (HFSF). Κρατάμε το ΜΕ ΤΧΣ ως part_pct, γιατί ο παρονομαστής του είναι
     όλη η αγορά — ίδιος ορισμός με το μοναδικό σύνολο της νέας διάταξης. Το
     ΧΩΡΙΣ μπαίνει δίπλα ως part_pct_exhfsf, ώστε η επιλογή να μπορεί να
     ξανακριθεί από τη σειρά και όχι από υπόθεση.
"""

import argparse, collections, io, json, os, re, shutil, subprocess, sys, tempfile, zipfile, datetime
import urllib.request, urllib.parse

# Η έκδοση τυπώνεται σε κάθε τρέξιμο, ώστε το log του Action να λέει ΜΟΝΟ του
# ποια εκδοχή έτρεξε. (03/11/2026: έτρεξαν κατά λάθος δύο παλιότερες.)
VERSION = "2026-11-03d"

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

# ΔΥΟ ΕΠΟΧΕΣ ΔΙΑΤΑΞΗΣ, ΔΥΟ ΜΟΡΦΕΣ ΑΡΙΘΜΟΥ (διαπιστώθηκε 03/11/2026):
#   ΠΑΛΙΑ (ως Μαρ 2021): ευρωπαϊκή γραφή «33.082,95», χωρίς σύμβολο %, γραμμή
#       συνόλου «TOTALS», πίνακας συμμετοχής με τίτλο «Total Listed Equities and
#       Main Categories» και ΕΞΙ ζεύγη στηλών (incl/excl ΤΧΣ × Σύνολο/Κύρια).
#   ΝΕΑ (από Απρ 2021): αμερικανική γραφή «115,821.90», με %, «Total», τίτλος
#       «Investors' Participation in Total Listed Equities», ΕΝΑ ζεύγος.
# Επιπλέον το παλιό PDF έχει ΠΑΡΑΣΙΤΙΚΑ ΚΕΝΑ μέσα στις λέξεις («Inv estors»,
# «Dom estic», «Gov ernment»), οπότε όλες οι αντιστοιχίσεις ετικετών γίνονται
# ΑΓΝΟΩΝΤΑΣ τα κενά.
# ⚠ Η παλιά μορφή αριθμού είναι ο σοβαρός κίνδυνος: με αμερικανικό regex το
# «3,01» έδινε «3» και «01» — ΣΚΟΥΠΙΔΙΑ ΠΟΥ ΠΕΡΝΟΥΣΑΝ τον έλεγχο πλήθους.

NUM_US = r"-?\d{1,3}(?:,\d{3})*(?:\.\d+)?"
NUM_EU = r"-?\d{1,3}(?:\.\d{3})*(?:,\d+)?"


def euro_format(text):
    """ΕΥΡΩΠΑΪΚΗ ή ΑΜΕΡΙΚΑΝΙΚΗ γραφή; Κρίνεται από το πλήθος δεκαδικών δύο
    ψηφίων: στην αμερικανική τα κόμματα χωρίζουν ΠΑΝΤΑ τριάδες, άρα «,05» δεν
    υπάρχει· στην ευρωπαϊκή δεν υπάρχει «.05»."""
    eu = len(re.findall(r"\d,\d{2}(?!\d)", text))
    us = len(re.findall(r"\d\.\d{2}(?!\d)", text))
    return eu > us


def spacey(word):
    """Regex που δέχεται παράσιτα κενά ΜΕΣΑ στη λέξη («Inv estors»)."""
    return r"\s*".join(re.escape(c) for c in word if not c.isspace())


FOREIGN = re.compile(r"^\s*[I\u0399]\s*[I\u0399]\s*\.\s*"
                     + spacey("ForeignInvestors") + r"\b(.*)$", re.I)
TOTALROW = re.compile(r"^\s*" + spacey("TOTAL") + r"S?\b(.*)$", re.I)

# Οι πίνακες που έχουν γραμμή «ΙΙ. Foreign Investors» και μας ενδιαφέρουν.
# Αγκυρώνουμε στον ΤΙΤΛΟ — ποτέ στο «3.1», που αλλάζει μεταξύ ετών.
TABLES = {
    "trade_total": ["Analysis of the Monthly Trading Activity in Total of Listed Equities"],
    "trade_ftse":  ["Trading Activity in FTSE / Athex Large Cap",
                    "Trading Activity in FTSE/Athex Large Cap"],
    "part_total":  ["Investors' Participation in Total Listed Equities",
                    "Participation in Total Listed Equities",
                    "Total Listed Equities and Main Categories"],
    "part_ftse":   ["Participation in the FTSE/Athex Large Cap Index",
                    "FTSE / Athex Large Cap & Average Number of Investors"],
}
_TAB = [(name, re.sub(r"\s+", "", ph).lower())
        for name, phrases in TABLES.items() for ph in phrases]


def tables_of(text, eu):
    """{όνομα πίνακα: (τιμές της γραμμής ΙΙ. Foreign Investors, τιμές TOTAL)}.

    Για κάθε γραμμή συνόλου ξένων βρίσκουμε τον ΠΛΗΣΙΕΣΤΕΡΟ ΠΡΟΗΓΟΥΜΕΝΟ τίτλο
    πίνακα. Αντίστροφα (τίτλος -> πρώτη γραμμή από κάτω) ΔΕΝ δουλεύει: ο ίδιος
    τίτλος εμφανίζεται και στα περιεχόμενα, και η καταχώρηση των περιεχομένων
    σπάει σε δύο γραμμές, οπότε η πρώτη δεν έχει τελείες και περνά για σώμα.
    Κρατάμε ΤΗΝ ΠΡΩΤΗ γραμμή κάθε πίνακα (setdefault): έτσι οι ενδιάμεσοι
    πίνακες που ΔΕΝ μας ενδιαφέρουν δεν μπορούν να την αντικαταστήσουν.
    Μαζί κρατάμε και τη γραμμή TOTAL του ΙΔΙΟΥ πίνακα, για τον παρονομαστή."""
    pat = re.compile((NUM_EU if eu else NUM_US) + r"%?")
    lines = text.splitlines()
    marks, out = [], {}
    for i, ln in enumerate(lines):
        flat = re.sub(r"\s+", "", ln).lower()
        for name, key in _TAB:
            if key in flat:
                marks.append((i, name))
                break
    for i, ln in enumerate(lines):
        m = FOREIGN.match(ln)
        if not m:
            continue
        vals = pat.findall(m.group(1))
        if not vals:
            continue
        prev = [nm for (j, nm) in marks if j < i]
        if not prev:
            continue
        tot = None
        for j in range(i, min(i + 70, len(lines))):
            t = TOTALROW.match(lines[j])
            if t:
                tv = pat.findall(t.group(1))
                if len(tv) >= len(vals):
                    tot = tv
                break
        out.setdefault(prev[-1], (vals, tot))
    return out


def period_of(text, eu):
    """Μήνας/έτος ΑΠΟ ΜΕΣΑ ΑΠΟ ΤΟ PDF, σε τρία επίπεδα — οι δύο εποχές γράφουν
    την περίοδο αλλιώς:
      1) ημερομηνία ηη/μμ/εεεε στους πίνακες   (παλιά: «31/01/2020»)
      2) «AxiaNumbers, January 2020» στο disclaimer (παλιά)
      3) σκέτη γραμμή «SEPTEMBER 2026» στο εξώφυλλο  (νέα)
    Το παλιό εξώφυλλο γράφει ΜΟΝΟ «January», χωρίς έτος — γι' αυτό το (3) δεν
    αρκεί από μόνο του."""
    d = re.findall(r"\b[0-3]\d/([0-1]\d)/(20\d{2})\b", text)
    if d:
        mo, yr = collections.Counter(d).most_common(1)[0][0]
        return "%s-%s" % (yr, mo)
    m = re.search(r"Axia\s?Numbers?,?\s+([A-Za-z]{3,9})\s+(20\d{2})", text, re.I)
    if not m:
        m = re.search(r"^\s*([A-Za-z]{3,9})\s+(20\d{2})\s*$", text[:1500], re.M)
    if m and MONTHS.get(m.group(1).title()):
        return "%s-%02d" % (m.group(2), MONTHS[m.group(1).title()])
    return None


def parse_text(text, period):
    """Εξαγωγή + επαλήθευση. Σπάει με ValueError αν κάτι δεν βγαίνει."""
    eu = euro_format(text)

    def f(x):
        x = x.rstrip("%")
        return float(x.replace(".", "").replace(",", ".")) if eu \
            else float(x.replace(",", ""))

    tb = tables_of(text, eu)
    r = {"period": period, "eu_format": eu}

    v, _ = tb.get("trade_total", (None, None))
    if not v or len(v) < 10:
        raise ValueError("μηνιαίες συναλλαγές (σύνολο αγοράς): γραμμή ξένων %s" % v)
    r["buys_m"], r["buys_pct"] = f(v[2]), f(v[3])
    r["sells_m"], r["sells_pct"] = f(v[6]), f(v[7])
    r["net_m"], r["net_ytd_m"] = f(v[8]), f(v[9])

    v, tot = tb.get("part_total", (None, None))
    if not v:
        raise ValueError("συμμετοχή (σύνολο εισηγμένων): γραμμή ξένων δεν βρέθηκε")
    # ΠΛΗΘΟΣ ΣΤΗΛΩΝ = ΕΠΟΧΗ. 4 -> νέα διάταξη. 12 -> παλιά με ΤΧΣ (incl στις
    # θέσεις 2/3, excl στις 4/5, Κύρια Αγορά από τη 6). 8 -> παλιά χωρίς ΤΧΣ.
    # ΚΡΑΤΑΜΕ ΤΟ incl ΤΧΣ: ο παρονομαστής του είναι ΟΛΗ η αγορά, που είναι ο
    # ίδιος ορισμός με το μοναδικό σύνολο της νέας διάταξης. Το excl μπαίνει
    # δίπλα ως part_pct_exhfsf — ΔΕΝ χάνεται, ώστε να κριθεί από τη σειρά.
    if len(v) == 4:
        idx = 2
    elif len(v) in (8, 12):
        idx = 2
        if len(v) == 12:
            r["part_val_exhfsf_m"], r["part_pct_exhfsf"] = f(v[4]), f(v[5])
    else:
        raise ValueError("συμμετοχή: ασυνήθιστο πλήθος στηλών (%d): %s" % (len(v), v))
    r["part_n"], r["part_val_m"], r["part_pct"] = int(f(v[0])), f(v[idx]), f(v[idx + 1])

    # Παρονομαστής = το κελί της γραμμής TOTAL στην ΙΔΙΑ ΣΤΗΛΗ. Δουλεύει και
    # στις δύο εποχές χωρίς να ξέρουμε πόσες στήλες έχει ο πίνακας.
    if not tot or len(tot) <= idx:
        raise ValueError("συμμετοχή: δεν βρέθηκε η γραμμή TOTAL του πίνακα")
    r["mkt_val_m"] = f(tot[idx])

    # --- check 1: αγορές - πωλήσεις == net ---
    d = abs((r["buys_m"] - r["sells_m"]) - r["net_m"])
    if d > 0.05:
        raise ValueError("αγορές-πωλήσεις != net (διαφορά %.2f εκ. €)" % d)

    # --- check 2: αξία / σύνολο == ποσοστό ---
    calc = r["part_val_m"] / r["mkt_val_m"] * 100.0
    if abs(calc - r["part_pct"]) > 0.03:
        raise ValueError("συμμετοχή %.2f%% != αξία/σύνολο %.2f%%"
                         % (r["part_pct"], calc))

    # --- check 3: περίοδος μέσα από το PDF — ΚΑΤΑΓΡΑΦΕΤΑΙ, ΔΕΝ ΑΠΟΡΡΙΠΤΕΙ ---
    # Αρχικά απέρριπτε. Το τεύχος 237 («June 2023») έχει εξώφυλλο «July 2023»
    # και χανόταν ολόκληρος μήνας για ένα τυπογραφικό του δελτίου. Τον πραγματικό
    # κίνδυνο (λάθος ή διπλό αρχείο) τον πιάνει ο check 4, που ελέγχει τη
    # ΣΥΝΕΧΕΙΑ του net YtD μέσα στη σειρά.
    inside = period_of(text, eu)
    r["cover_ok"] = (inside == period)
    if inside and not r["cover_ok"]:
        r["cover"] = inside
    return r


def check_series(months):
    """CHECK 4 — ΣΥΝΕΧΕΙΑ ΤΟΥ net YtD ΜΕΣΑ ΣΤΗ ΣΕΙΡΑ.

    Σε κάθε μήνα πλην Ιανουαρίου: net_ytd(τρέχοντος) - net_ytd(προηγούμενου)
    πρέπει να ισούται με net(τρέχοντος). Τον Ιανουάριο: net_ytd == net.
    Αυτό πιάνει αυτό που ο έλεγχος εξωφύλλου δεν πιάνει αξιόπιστα — λάθος ή
    διπλό αρχείο — γιατί τότε η διαφορά βγαίνει εκατοντάδες εκατομμύρια, όχι
    δεκάδες λεπτά. Ανοχή 1,0 εκ. €: το net_ytd του δελτίου είναι ανεξάρτητη
    στρογγυλοποίηση αθροίσματος (μετρημένη απόκλιση ως 0,09 εκ. €).
    Επιστρέφει λίστα προβλημάτων — ΔΕΝ πετάει μήνες."""
    by = {r["period"]: r for r in months}
    out = []
    for r in months:
        y, mo = map(int, r["period"].split("-"))
        if mo == 1:
            d, ref = abs(r["net_ytd_m"] - r["net_m"]), "net"
        else:
            prev = by.get("%04d-%02d" % (y, mo - 1))
            if not prev:
                continue
            d = abs((r["net_ytd_m"] - prev["net_ytd_m"]) - r["net_m"])
            ref = "net_ytd(%s)" % prev["period"]
        if d > 1.0:
            out.append({"period": r["period"],
                        "why": "ασυνέχεια net YtD ως προς %s: %.2f εκ. €" % (ref, d)})
    return out


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


FILE_PREFIX = "/sites/default/files/"


def inventory():
    """-> [{'issue':276,'period':'2026-09','title':...,'url':...}] φθίνουσα.

    ΔΥΟ ΜΟΡΦΕΣ ΓΡΑΜΜΗΣ ΣΤΟ ΙΔΙΟ ΑΡΧΕΙΟ (διαπιστώθηκε 03/11/2026, το σημείο
    αλλαγής είναι μεταξύ Οκτ και Νοε 2024):
      ΠΑΛΙΑ:  ο τίτλος δείχνει ΚΑΤΕΥΘΕΙΑΝ στο έγγραφο, /en/documents/10180/...
      ΝΕΑ:    ο τίτλος δείχνει σε ΣΕΛΙΔΑ ανακοίνωσης, /en/more-options/
              announcements/issue-276-september-2026, και το αρχείο κρέμεται
              χωριστά στο /sites/default/files/2026-10/Issue 276 (...).zip
    Γι' αυτό προτιμάμε ΠΑΝΤΑ τον σύνδεσμο αρχείου όταν υπάρχει: το ΟΝΟΜΑ του
    αρχείου κουβαλά μόνο του τεύχος και μήνα, άρα δεν χρειάζεται αντιστοίχιση
    με τη γραμμή. Αν λείπει, πέφτουμε στον τίτλο — και τότε αναλαμβάνει η
    follow_html() στον βρόχο λήψης."""
    from bs4 import BeautifulSoup
    best, out = {}, []
    for p in range(PAGES):
        url = "%s?field_mig_category_target_id=%d&page=%d" % (
            LIST, CATEGORY_AXIA_SECURITIES, p)
        soup = BeautifulSoup(fetch(url).decode("utf-8", "replace"), "html.parser")
        found = 0
        for a in soup.find_all("a", href=True):
            href = urllib.parse.urljoin(BASE, a["href"])
            # (1) σύνδεσμος αρχείου — ο τίτλος είναι μέσα στο ΟΝΟΜΑ του
            txt = urllib.parse.unquote(href.rsplit("/", 1)[-1]) \
                  if FILE_PREFIX in href else a.get_text(" ", strip=True)
            m = TITLE_RE.search(txt)
            if not m:
                continue
            mon = MONTHS.get(m.group(2).title())
            if not mon:
                continue
            key = (int(m.group(1)), "%s-%02d" % (m.group(3), mon))
            direct = FILE_PREFIX in href or "/documents/" in href
            # προτεραιότητα: σύνδεσμος αρχείου > /documents/ > σελίδα ανακοίνωσης
            rank = 2 if FILE_PREFIX in href else (1 if direct else 0)
            if key not in best or rank > best[key][0]:
                best[key] = (rank, href, a.get_text(" ", strip=True) or txt)
                found += 1
        if found == 0:
            print("  σελίδα %d: καμία γραμμή — άλλαξε η δομή;" % p, file=sys.stderr)
    for (issue, period), (rank, href, title) in best.items():
        out.append({"issue": issue, "period": period, "title": title,
                    "url": href, "direct": rank > 0})
    out.sort(key=lambda r: r["period"], reverse=True)
    return out


def follow_html(raw, url):
    """Αν αντί για αρχείο ήρθε σελίδα HTML, βρες μέσα της τον σύνδεσμο λήψης.

    Δεύτερη ζώνη ασφαλείας: κρατά τη ροή ζωντανή και στην επόμενη μετακόμιση
    του site, χωρίς να χρειάζεται να ξέρουμε εκ των προτέρων τη νέα δομή."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(raw.decode("utf-8", "replace"), "html.parser")
    for a in soup.find_all("a", href=True):
        h = urllib.parse.urljoin(url, a["href"])
        if FILE_PREFIX in h or h.lower().endswith((".zip", ".pdf")):
            return h
    raise ValueError("ήρθε HTML και δεν βρέθηκε σύνδεσμος λήψης μέσα της")


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
    except Exception:
        return {}
    if "months" not in d and "rows" in d:
        # Αρχείο από την ΠΡΩΤΗ εκδοχή του script (κλειδί "rows", χαλαρό regex
        # που έδινε cap_pct ~16-20% αντί ~60-70%). Δεν κληρονομείται τίποτε.
        print("ΠΡΟΣΟΧΗ: βρέθηκε JSON παλιάς μορφής (%d γραμμές στο \"rows\") — "
              "ΑΓΝΟΕΙΤΑΙ και ξαναχτίζεται από την αρχή."
              % len(d.get("rows") or []), file=sys.stderr)
        return {}
    return {r["period"]: r for r in d.get("months", [])}


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
    print("xenoi_ependites.py έκδοση %s" % VERSION)

    if a.selftest:
        data, inner = pdf_bytes(open(a.selftest, "rb").read())
        print("PDF μέσα στο αρχείο: %s" % inner)
        txt = pdf_text(data)
        eu = euro_format(txt)
        per = period_of(txt, eu)
        print("γραφή αριθμών: %s · περίοδος μέσα από το PDF: %s"
              % ("ευρωπαϊκή" if eu else "αμερικανική", per))
        if not per:
            print("ΔΕΝ βρέθηκε περίοδος μέσα στο PDF", file=sys.stderr); sys.exit(1)
        r = parse_text(txt, per)
        w = max(len(k) for k in r)
        for k, v in r.items():
            print("  %-*s %s" % (w, k, v))
        print("OK — πέρασαν οι checks 1-3 (ο 4 είναι σειριακός)")
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
                raw = fetch(r["url"])
                if raw[:1] == b"<":                 # σελίδα, όχι αρχείο
                    raw = fetch(follow_html(raw, r["url"]))
                data, _ = pdf_bytes(raw)
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
    breaks = check_series(months)
    covers = [r["period"] for r in months if not r.get("cover_ok")]
    for b in breaks:
        print("  ΑΣΥΝΕΧΕΙΑ %s: %s" % (b["period"], b["why"]), file=sys.stderr)
    if covers:
        print("  εξώφυλλο != τίτλος σε: %s (κρατήθηκαν· βλ. check 3)"
              % ", ".join(covers), file=sys.stderr)
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
            "ytd_breaks": breaks,
            "cover_mismatch": covers,
        }, fh, ensure_ascii=False, indent=1)
    print("γράφτηκε %s — %d μήνες (%s -> %s), %d αποτυχίες, "
          "%d ασυνέχειες net YtD, %d με εξώφυλλο != τίτλο"
          % (OUT, len(months),
             months[0]["period"] if months else "—",
             months[-1]["period"] if months else "—",
             len(failed), len(breaks), len(covers)))
    if failed or breaks:
        sys.exit(1)


if __name__ == "__main__":
    main()
