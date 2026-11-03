#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ξένοι επενδυτές — Axion Metrics
================================
Μηνιαία σειρά συμμετοχής ξένων επενδυτών στο Euronext Athens, από το
«Securities Market Monthly Statistical Bulletin (AXIA NUMBERS)».

ΠΗΓΗ — γιατί ΑΥΤΗ και όχι το Mid-Month Report:
  Το Mid-Month Report δίνει ένα στιγμιότυπο ανά έκδοση, ΑΛΛΑΖΕΙ ορισμό στο
  μερίδιο συναλλαγών (οι εκδόσεις 2025 δίνουν σωρευτικό YtD, του 2026
  δεκαπενθημέρου) και δεν έχει σελίδα αρχείου. Το AXIA NUMBERS Securities
  δίνει ΜΗΝΙΑΙΑ στοιχεία με σταθερές ενότητες και έχει αρχείο ως το 2007.
  ΜΗΝ τα ανακατεύεις: για το 2019 το AXIA δίνει 64,18% συμμετοχή (με ΤΧΣ)
  ενώ το Mid-Month 66,4%. Διαφορετικό σύνολο αναφοράς.

ΤΙ ΒΓΑΖΕΙ (ανά μήνα):
  - συμμετοχή ξένων στην κεφαλαιοποίηση   (ενότητα 3.1.1)
  - αγορές / πωλήσεις ξένων του μήνα       (ενότητα 2.3.1)
  - καθαρή ροή του μήνα                    (= αγορές - πωλήσεις)
  - γεωγραφική κατανομή                    (ενότητα 2.3.11, προαιρετικά)

ΤΡΟΠΟΣ ΧΡΗΣΗΣ:
  python xenoi_ependites.py --inventory     # μόνο ο κατάλογος τευχών (χωρίς λήψη)
  python xenoi_ependites.py --fetch         # λήψη + αποθήκευση PDF στο cache
  python xenoi_ependites.py                 # πλήρες: λήψη, εξαγωγή, JSON

ΠΡΟΣΟΧΗ (§ΝΕΟ):
  1) Από το Issue 190 (Ιούλιος 2019) και μετά τα τεύχη είναι **ZIP**. Οι
     διευθύνσεις /en/documents/... ΔΕΝ έχουν κατάληξη — ο τύπος αναγνωρίζεται
     από τα πρώτα bytes, ΟΧΙ από το URL.
  2) Υπάρχουν ΚΕΝΑ στη σειρά τευχών (π.χ. λείπει το 047). Μη θεωρείς ότι ο
     αριθμός τεύχους αντιστοιχεί γραμμικά σε μήνα.
  3) Το δελτίο καθυστερεί 1-2 μήνες. Ο τελευταίος διαθέσιμος μήνας ΔΕΝ είναι
     ο προηγούμενος.
  4) Η διάταξη των ενοτήτων είναι επαληθευμένη στο τεύχος 187 (Απρ 2019).
     Για 2020+ ΔΕΝ έχει επαληθευτεί — γι' αυτό η parse_pdf() ΣΠΑΕΙ θορυβωδώς
     αν δεν βρει ό,τι περιμένει, αντί να γράψει σιωπηλά λάθος νούμερα.
"""

import argparse, io, json, os, re, sys, zipfile
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
            mon = MONTHS.get(m.group(2))
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


NUM = r"([\d.,]+)"

def parse_pdf(text, period):
    """Εξαγωγή των τριών μεγεθών. ΣΠΑΕΙ αν δεν βρει — δεν μαντεύει.

    ΕΠΑΛΗΘΕΥΜΕΝΟ στο Issue 187 (Απρ 2019):
      3.1.1 «Total Listed Equities and Main Categories» -> II. Foreign Investors
      2.3.1 «Analysis of the Monthly Trading Activity ... per Investor Category»
    Αν η διάταξη άλλαξε στα νεότερα τεύχη, ΕΔΩ είναι το σημείο που διορθώνεις —
    και ΠΑΝΤΑ με δείγμα μπροστά σου, όχι με εικασία."""
    res = {"period": period}
    flat = re.sub(r"[ \t]+", " ", text)

    m = re.search(r"Foreign\s+Investors.{0,200}?" + NUM + r"\s*%", flat, re.S | re.I)
    if not m:
        raise ValueError("%s: δεν βρέθηκε ποσοστό συμμετοχής (3.1.1)" % period)
    res["cap_pct"] = float(m.group(1).replace(".", "").replace(",", "."))

    # ΤΟ ΣΗΜΕΙΟ ΠΟΥ ΘΕΛΕΙ ΔΕΙΓΜΑ: αγορές/πωλήσεις ξένων του μήνα (2.3.1).
    # Μένει ασυμπλήρωτο επίτηδες ώσπου να δούμε πραγματικό τεύχος 2020+.
    res["buys_pct"] = res["sells_pct"] = None
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory", action="store_true", help="μόνο κατάλογος τευχών")
    ap.add_argument("--fetch", action="store_true", help="λήψη + αποθήκευση PDF")
    ap.add_argument("--from", dest="frm", default=FROM_PERIOD)
    a = ap.parse_args()

    inv = [r for r in inventory() if r["period"] >= a.frm]
    print("τεύχη από %s: %d  (%s -> %s)" % (
        a.frm, len(inv), inv[-1]["period"] if inv else "—",
        inv[0]["period"] if inv else "—"))

    # έλεγχος κενών: ποιοι μήνες λείπουν από το εύρος
    have = {r["period"] for r in inv}
    if inv:
        y0, m0 = map(int, inv[-1]["period"].split("-"))
        y1, m1 = map(int, inv[0]["period"].split("-"))
        gaps = ["%04d-%02d" % (y, m)
                for y in range(y0, y1 + 1) for m in range(1, 13)
                if (y, m) >= (y0, m0) and (y, m) <= (y1, m1)
                and "%04d-%02d" % (y, m) not in have]
        print("κενά: %s" % (", ".join(gaps) if gaps else "κανένα"))

    if a.inventory:
        for r in inv:
            print("  %s  Issue %-4d %s" % (r["period"], r["issue"], r["url"]))
        return

    os.makedirs(CACHE, exist_ok=True)
    rows, failed = [], []
    for r in inv:
        dst = os.path.join(CACHE, "%s_issue%d.pdf" % (r["period"], r["issue"]))
        try:
            if not os.path.exists(dst):
                data, inner = pdf_bytes(fetch(r["url"]))
                with open(dst, "wb") as f:
                    f.write(data)
                print("  %s  %s" % (r["period"], inner))
            if a.fetch:
                continue
            import pdfplumber                      # μόνο όταν χρειάζεται
            with pdfplumber.open(dst) as pdf:
                text = "\n".join((p.extract_text() or "") for p in pdf.pages)
            rows.append(parse_pdf(text, r["period"]))
        except Exception as ex:
            failed.append((r["period"], str(ex)[:120]))
            print("  ΑΠΟΤΥΧΙΑ %s: %s" % (r["period"], ex), file=sys.stderr)

    if failed:
        print("\nαπέτυχαν %d από %d τεύχη" % (len(failed), len(inv)), file=sys.stderr)
    if a.fetch:
        print("\nτα PDF αποθηκεύτηκαν στο %s" % CACHE)
        return

    rows.sort(key=lambda r: r["period"])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({"source": "AXIA NUMBERS Securities (Euronext Athens)",
               "category_param": CATEGORY_AXIA_SECURITIES,
               "rows": rows, "failed": failed},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("γράφτηκε %s — %d μήνες" % (OUT, len(rows)))


if __name__ == "__main__":
    main()
