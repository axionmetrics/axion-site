# -*- coding: utf-8 -*-
"""AXION — ισοτιμίες ΕΚΤ (§103 + §160).

ΔΥΟ ΧΡΗΣΕΙΣ, ΕΝΑ ΑΡΧΕΙΟ:

1) ΧΕΙΡΟΚΙΝΗΤΑ — όταν καταχωρούμε μεγέθη εταιρείας που δημοσιεύει σε άλλο νόμισμα:
     python3 fx_rates.py 2026H1 [USD]    -> κλείσιμο + μέση περιόδου + γραμμή για το φύλλο
     python3 fx_rates.py 2025   [USD]
     python3 fx_rates.py latest [USD]    -> τελευταία διαθέσιμη ημερήσια παρατήρηση
   Κανόνας (§103): ισολογισμός με την ισοτιμία ΚΛΕΙΣΙΜΑΤΟΣ της περιόδου, αποτελέσματα και
   ταμειακές ροές με τη ΜΕΣΗ της περιόδου.

2) ΩΣ JOB (§160) — `python3 .github/scripts/fx_rates.py --job` από το fx-rates.yml:
   γράφει ΔΥΟ αρχεία, ώστε να αντλεί η κάθε εργασία την ισοτιμία όποτε τη θέλει:
     .github/fx/rates.json   μηχαναγνώσιμο — latest + ιστορικό (για python jobs/γέφυρα)
     assets/fx.js            window.AXION_FX — για τις σελίδες (ίδιο μοτίβο με current.js)

⚠ ΦΟΡΑ ΜΕΤΑΤΡΟΠΗΣ — ΤΟ ΛΑΘΟΣ ΠΟΥ ΕΓΙΝΕ ΗΔΗ ΜΙΑ ΦΟΡΑ (BUG 13):
   Η ΕΚΤ δίνει «**ξένο νόμισμα ανά 1 ευρώ**».
       ευρώ      = ξένο_ποσό / ισοτιμία
       ξένο_ποσό = ευρώ      * ισοτιμία
   Έλεγχος λογικής: ασθενέστερο ευρώ (μικρότερη ισοτιμία) → ΠΕΡΙΣΣΟΤΕΡΑ ευρώ για το ίδιο
   δολάριο. Χρησιμοποίησε τις βοηθητικές `to_eur()` / `to_ccy()` αντί για σκέτο */.

⚠ Η ΕΚΤ ΔΗΜΟΣΙΕΥΕΙ ΜΟΝΟ ΕΡΓΑΣΙΜΕΣ, και η τιμή της ημέρας βγαίνει ~16:00 CET. Το job
   κρατά ΠΑΝΤΑ την τελευταία διαθέσιμη παρατήρηση μαζί με την ΗΜΕΡΟΜΗΝΙΑ της και το
   `stale_days`· καμία εργασία δεν πρέπει να υποθέτει ότι η τιμή είναι της σήμερον.
"""
import sys, csv, io, json, os, urllib.request, statistics, datetime

BASE   = 'https://data-api.ecb.europa.eu/service/data/EXR/%s?startPeriod=%s&endPeriod=%s&format=csvdata'
SOURCE = 'ECB reference rates (EXR D.<CUR>.EUR.SP00.A)'
RULE   = 'ξένο νόμισμα ανά 1 ευρώ → ευρώ = ξένο / ισοτιμία'

# Νομίσματα που αντλεί το job. Πρόσθεσε κωδικό ISO εδώ όταν μπει εταιρεία που
# δημοσιεύει σε άλλο νόμισμα (η 141 CMF δημοσιεύει σε USD).
CURRENCIES = ['USD']
KEEP_DAYS  = 800          # πόσο ιστορικό κρατά το rates.json (~3 έτη εργάσιμων)
JSON_OUT   = '.github/fx/rates.json'
JS_OUT     = 'assets/fx.js'


# ── άντληση ────────────────────────────────────────────────────────────────────────
def series(key, s, e):
    with urllib.request.urlopen(BASE % (key, s, e), timeout=60) as r:
        rd = csv.DictReader(io.StringIO(r.read().decode()))
        return [(x['TIME_PERIOD'], float(x['OBS_VALUE'])) for x in rd if x.get('OBS_VALUE')]

def daily(cur, days=30):
    """Τελευταίες ημερήσιες παρατηρήσεις. Το παράθυρο καλύπτει αργίες/Πάσχα."""
    e = datetime.date.today()
    s = e - datetime.timedelta(days=days)
    return series('D.%s.EUR.SP00.A' % cur.upper(), s.isoformat(), e.isoformat())

def period(p):
    if p.endswith('H1'): y = int(p[:4]); return '%d-01-01' % y, '%d-06-30' % y
    if p.endswith('H2'): y = int(p[:4]); return '%d-07-01' % y, '%d-12-31' % y
    y = int(p); return '%d-01-01' % y, '%d-12-31' % y


# ── μετατροπές: ΧΡΗΣΙΜΟΠΟΙΗΣΕ ΑΥΤΕΣ, ΟΧΙ ΣΚΕΤΟ */ ─────────────────────────────────
def to_eur(amount, rate):
    """ξένο ποσό → ευρώ."""
    return amount / rate

def to_ccy(amount_eur, rate):
    """ευρώ → ξένο ποσό."""
    return amount_eur * rate


# ── για άλλα jobs/τη γέφυρα ────────────────────────────────────────────────────────
def load_rate(cur='USD', path=JSON_OUT):
    """Διαβάζει την αποθηκευμένη ισοτιμία. Επιστρέφει (ισοτιμία, ημερομηνία, stale_days)
    ή (None, None, None) αν λείπει. ΠΟΤΕ δεν χτυπά δίκτυο — το job έχει ήδη τρέξει.

        r, d, stale = load_rate('USD')
        eur = to_eur(dollars, r)        # ΟΧΙ dollars * r
    """
    try:
        with open(path, encoding='utf8') as f:
            d = json.load(f)
        e = d['latest'][cur.upper()]
        stale = (datetime.date.today() - datetime.date.fromisoformat(e['date'])).days
        return e['rate'], e['date'], stale
    except Exception:
        return None, None, None


# ── job ────────────────────────────────────────────────────────────────────────────
def run_job():
    today = datetime.date.today()
    old = {}
    if os.path.exists(JSON_OUT):
        try:
            with open(JSON_OUT, encoding='utf8') as f: old = json.load(f)
        except Exception: old = {}
    hist = old.get('history', {})
    latest, report = {}, []

    for cur in CURRENCIES:
        h = dict(hist.get(cur, {}))
        # ΠΡΩΤΗ ΕΚΤΕΛΕΣΗ (άδειο ιστορικό): τράβα ολόκληρο το παράθυρο, ώστε οι εργασίες
        # να μπορούν να βγάλουν μέσους όρους από την πρώτη μέρα. Μετά, 30 ημέρες αρκούν
        # και καλύπτουν αργίες/διακοπές του job.
        win = 30 if h else KEEP_DAYS
        try:
            obs = daily(cur, win)
        except Exception as ex:
            obs = []
            report.append('%s: ΑΠΟΤΥΧΙΑ άντλησης (%s)' % (cur, type(ex).__name__))
        added = 0
        for d, v in obs:
            if h.get(d) != v: added += 1
            h[d] = v
        # κράτα παράθυρο
        cut = (today - datetime.timedelta(days=KEEP_DAYS)).isoformat()
        h = {d: v for d, v in h.items() if d >= cut}
        if not h:
            report.append('%s: ΚΑΜΙΑ τιμή — ούτε νέα ούτε αποθηκευμένη' % cur); continue
        last = max(h)
        stale = (today - datetime.date.fromisoformat(last)).days
        hist[cur] = dict(sorted(h.items()))
        # ΣΚΟΠΙΜΑ ΔΕΝ αποθηκεύεται `stale_days`: θα άλλαζε κάθε μέρα και το job θα
        # έκανε commit χωρίς νέο δεδομένο. Το υπολογίζει ο καταναλωτής από το `date`.
        latest[cur] = {'rate': h[last], 'date': last}
        report.append('%s: %.4f (%s) · νέες/αλλαγμένες %d · ιστορικό %d ημέρες%s'
                      % (cur, h[last], last, added, len(h),
                         '  ⚠ ΠΑΛΙΑ ΤΙΜΗ' if stale > 4 else ''))

    if not latest:
        print('\n'.join(report)); raise SystemExit('fx: καμία ισοτιμία — το αρχείο δεν πειράχτηκε')

    # ΧΩΡΙΣ ΝΕΟ ΔΕΔΟΜΕΝΟ ΔΕΝ ΑΓΓΙΖΟΥΜΕ ΤΑ ΑΡΧΕΙΑ — αλλιώς το `updated` θα άλλαζε σε κάθε
    # εκτέλεση και το βήμα commit θα έσπρωχνε θόρυβο πέντε φορές τη μέρα.
    if old.get('latest') == latest and old.get('history') == hist and os.path.exists(JS_OUT):
        print('== fx_rates (job) ==')
        for r in report: print('  ' + r)
        print('  καμία αλλαγή — τα αρχεία δεν πειράχτηκαν.')
        return
    out = {'updated': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
           'source': SOURCE, 'rule': RULE, 'latest': latest, 'history': hist}
    os.makedirs(os.path.dirname(JSON_OUT), exist_ok=True)
    with open(JSON_OUT, 'w', encoding='utf8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=False)
    os.makedirs(os.path.dirname(JS_OUT), exist_ok=True)
    with open(JS_OUT, 'w', encoding='utf8') as f:
        f.write('/* Axion Metrics — ισοτιμίες ΕΚΤ (§160). Παράγεται ΑΥΤΟΜΑΤΑ από το\n'
                '   .github/scripts/fx_rates.py. ΜΗΝ το επεξεργάζεσαι με το χέρι.\n'
                '   ΦΟΡΑ: %s */\n' % RULE)
        f.write('window.AXION_FX = ' + json.dumps(
            {'updated': out['updated'], 'source': SOURCE, 'rule': RULE, 'latest': latest},
            ensure_ascii=False, separators=(',', ':')) + ';\n')
    print('== fx_rates (job) ==')
    for r in report: print('  ' + r)
    print('  γράφτηκαν: %s · %s' % (JSON_OUT, JS_OUT))


# ── χειροκίνητα ────────────────────────────────────────────────────────────────────
def show_latest(cur):
    d = daily(cur)
    if not d: raise SystemExit('δεν βρέθηκε ημερήσια ισοτιμία για %s' % cur)
    day, v = d[-1]
    stale = (datetime.date.today() - datetime.date.fromisoformat(day)).days
    print('ΝΟΜΙΣΜΑ       : %s ανά 1 EUR' % cur)
    print('ΤΕΛΕΥΤΑΙΑ     : %.4f  (%s%s)' % (v, day, ', πριν %d ημέρες' % stale if stale else ', σήμερα'))
    print('ΦΟΡΑ          : %s' % RULE)
    print('ΠΗΓΗ          : %s' % SOURCE)

def show_period(per, cur):
    s, e = period(per)
    d = series('D.%s.EUR.SP00.A' % cur, s, e)
    if not d: raise SystemExit('δεν βρέθηκαν ημερήσιες ισοτιμίες για %s %s' % (cur, per))
    close_day, close = d[-1]
    avg = statistics.mean(v for _, v in d)
    note = 'μέσος όρος %d ημερήσιων παρατηρήσεων' % len(d)
    if not per.endswith(('H1', 'H2')):
        a = series('A.%s.EUR.SP00.A' % cur, per, per)
        if a: avg = a[0][1]; note = 'ετήσια μέση ΕΚΤ'
    print('ΠΕΡΙΟΔΟΣ      : %s' % per)
    print('ΝΟΜΙΣΜΑ       : %s ανά 1 EUR' % cur)
    print('ΚΛΕΙΣΙΜΑΤΟΣ   : %.4f  (%s)' % (close, close_day))
    print('ΜΕΣΗ          : %.4f  (%s)' % (avg, note))
    print('ΦΟΡΑ          : %s' % RULE)
    print('ΠΗΓΗ          : %s' % SOURCE)
    print('ΑΝΤΛΗΘΗΚΕ     : %s' % datetime.date.today().isoformat())
    print('\nΓΡΑΜΜΗ ΓΙΑ ΤΟ ΦΥΛΛΟ ΙΣΟΤΙΜΙΕΣ:')
    print('%s | %s | %.4f | %.4f | %s | %s' % (per, cur, close, avg, close_day, note))

def main():
    a = sys.argv[1:]
    if a and a[0] == '--job': return run_job()
    if not a: raise SystemExit(__doc__)
    cur = (a[1] if len(a) > 1 else 'USD').upper()
    return show_latest(cur) if a[0] == 'latest' else show_period(a[0], cur)

if __name__ == '__main__': main()
