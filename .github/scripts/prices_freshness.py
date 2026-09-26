#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prices_freshness.py — Axion Metrics
===================================
Ελέγχει αν το `assets/current.js` κουβαλά την ΤΕΛΕΥΤΑΙΑ ΚΛΕΙΣΜΕΝΗ συνεδρίαση.

ΓΙΑΤΙ ΥΠΑΡΧΕΙ (§111): η αλυσίδα των ημερήσιων τιμών αποτυγχάνει **σιωπηλά**. Ο
Cloudflare Worker γράφει τον κωδικό απόκρισης του GitHub σε `console.log` που δεν τον
βλέπει κανείς· αν λήξει το `GH_TOKEN` (24/09/2027), σβήσει ο Worker, αλλάξει το feed του
Euronext ή σπάσει το `daily_prices.py`, το μόνο ορατό σύμπτωμα είναι ότι το site δείχνει
παλιές τιμές. Ένα δεύτερο cron καλύπτει αποτυχία της *σκανδάλης*, όχι της *δουλειάς*.
Αυτός ο έλεγχος καλύπτει και τα δύο.

ΠΩΣ ΑΠΟΦΕΥΓΕΙ ΤΙΣ ΨΕΥΔΕΙΣ ΕΙΔΟΠΟΙΗΣΕΙΣ: δεν μετρά ημέρες. Ρωτά το **ίδιο το feed** ποια
ήταν η τελευταία συνεδρίαση, μέσω της `session_date()` του `daily_prices.py` — της ίδιας
συνάρτησης που σφραγίζει την ημερομηνία μέσα στο `current.js`. Έτσι αργίες του Χ.Α.
(Πάσχα, Καθαρά Δευτέρα, 15Αυγ) δεν παράγουν συναγερμό: το feed δεν προχωρά ούτε αυτό.
ΚΑΝΕΝΑ ημερολόγιο αργιών δεν συντηρείται πουθενά.

Έξοδος: `stale=true|false` + `GITHUB_OUTPUT`, αναφορά σε $RUNNER_TEMP/freshness.md
(εκτός αποθετηρίου — δεν αφήνει αδέσποτα αρχεία). Πρόβλημα ΔΙΚΤΥΟΥ/feed -> ΟΧΙ συναγερμός
(παροδικό), μόνο προειδοποίηση.
"""
import json, os, re, sys, datetime, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daily_prices as dp          # μία πηγή αλήθειας για URL + session_date + CURRENT

def out(k, v):
    f = os.environ.get('GITHUB_OUTPUT')
    if f:
        with open(f, 'a', encoding='utf-8') as fh: fh.write('%s=%s\n' % (k, v))

def current_dates(path):
    """Όλες οι διακριτές ημερομηνίες μέσα στο current.js, με το πλήθος μετοχών καθεμιάς."""
    s = open(path, encoding='utf-8').read()
    d = json.loads(s[s.index('{'):].rstrip().rstrip(';'))
    c = {}
    for tk, rec in d.items():
        if isinstance(rec, dict) and rec.get('date'):
            c[rec['date']] = c.get(rec['date'], 0) + 1
    return c, len(d)

def main():
    # ── 1) τι λέει το feed
    try:
        req = urllib.request.Request(dp.URL, headers={'User-Agent': dp.UA})
        with urllib.request.urlopen(req, timeout=90) as r:
            raw = json.loads(r.read().decode('utf-8', 'replace'))
    except Exception as e:
        print('::warning::Το feed του Euronext δεν απαντά (%s) — παροδικό, χωρίς συναγερμό.' % e)
        out('stale', 'false'); out('feed_ok', 'false')
        return 0
    expected = dp.session_date(raw)

    # ── 2) τι λέει το αρχείο
    if not os.path.exists(dp.CURRENT):
        report(expected, None, {}, 0, 'ΛΕΙΠΕΙ ΤΟ ΑΡΧΕΙΟ %s' % dp.CURRENT)
        out('stale', 'true'); out('feed_ok', 'true'); return 0
    counts, total = current_dates(dp.CURRENT)
    if not counts:
        report(expected, None, counts, total, 'Το %s δεν περιέχει καμία ημερομηνία.' % dp.CURRENT)
        out('stale', 'true'); out('feed_ok', 'true'); return 0

    newest = max(counts)
    lag = (datetime.date.fromisoformat(expected) - datetime.date.fromisoformat(newest)).days
    stale = newest < expected
    print('feed: τελευταία συνεδρίαση %s · current.js: %s (%d μετοχές) · υστέρηση %d ημ.'
          % (expected, newest, counts[newest], lag))
    if stale:
        report(expected, newest, counts, total,
               'Το current.js είναι %d ημέρες πίσω από τη συνεδρίαση που δίνει το feed.' % lag)
    else:
        summary('✅ Οι τιμές είναι ενήμερες', expected, newest, counts, total)
    out('stale', 'true' if stale else 'false'); out('feed_ok', 'true')
    return 0

def _table(expected, newest, counts, total):
    L = ['| | |', '|---|---|',
         '| τελευταία συνεδρίαση κατά το feed | **%s** |' % expected,
         '| νεότερη ημερομηνία στο `current.js` | **%s** |' % (newest or '—'),
         '| μετοχές στο αρχείο | %d |' % total]
    if len(counts) > 1:
        L.append('| ⚠ ημερομηνίες στο ίδιο αρχείο | %s |'
                 % ' · '.join('%s (%d)' % (d, n) for d, n in sorted(counts.items(), reverse=True)))
    return L

def summary(title, expected, newest, counts, total):
    f = os.environ.get('GITHUB_STEP_SUMMARY')
    if not f: return
    with open(f, 'a', encoding='utf-8') as fh:
        fh.write('### %s\n\n' % title); fh.write('\n'.join(_table(expected, newest, counts, total)) + '\n')

def report(expected, newest, counts, total, why):
    body = ['**%s**' % why, '', *_table(expected, newest, counts, total), '',
            'Τι να ελέγξεις, με αυτή τη σειρά:', '',
            '1. **Actions → `daily-prices`** — έτρεξε; Αν όχι, δεν ήρθε η σκανδάλη.',
            '2. **Cloudflare → `axion-eod-trigger` → Logs** — ο κωδικός απόκρισης του GitHub. '
            '`401` σημαίνει ότι έληξε ή ανακλήθηκε το `GH_TOKEN` (προγραμματισμένη λήξη 24/09/2027).',
            '3. Αν η ροή έτρεξε αλλά δεν έγραψε, το πρόβλημα είναι στο `daily_prices.py` ή στο feed '
            'του Euronext — δες το job summary της εκτέλεσης.', '',
            '_Η ροή `daily-prices` έχει και δικό της cron στις 19:35 UTC (Δευ–Παρ) ως δικτυωτό· '
            'αν ούτε αυτό έγραψε, το σπασμένο κομμάτι είναι η δουλειά, όχι η σκανδάλη._']
    txt = '\n'.join(body) + '\n'
    p = os.path.join(os.environ.get('RUNNER_TEMP', '.'), 'freshness.md')
    open(p, 'w', encoding='utf-8').write(txt)
    print('αναφορά:', p)
    summary('⚠️ ΠΑΛΙΕΣ ΤΙΜΕΣ', expected, newest, counts, total)

if __name__ == '__main__':
    sys.exit(main())
