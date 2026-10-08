#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Axion Metrics — ΑΝΟΙΧΤΕΣ ΠΩΛΗΣΕΙΣ (short θέσεις) από την Επιτροπή Κεφαλαιαγοράς.  §128

Παράγει το `assets/shorts.js` (window.AXION_SHORTS) — ΑΝΕΞΑΡΤΗΤΟ από το data.js και από το
master. Τρέχει σε GitHub Action. ΚΑΜΙΑ χειροκίνητη ενέργεια στον κανονικό κύκλο.

Πηγή   : http://www.hcmc.gr/el_GR/web/portal/shortselling1
         ο σύνδεσμος «ΣΗΜΑΝΤΙΚΕΣ ΚΑΘΑΡΕΣ ΑΡΝΗΤΙΚΕΣ ΘΕΣΕΙΣ…» δείχνει σε αρχείο .xls του οποίου
         το ΟΝΟΜΑ φέρει την ημερομηνία ενημέρωσης: «<YYYY_MM_DD> HCMC_disclosed_short_positions_gr.xls».
         Τρία φύλλα: «Τρέχουσες», «Ιστορικό», «Ημερομηνία Δημοσίευσης».
         Στήλες (κεφαλίδα γρ.7): POSITION HOLDER · NAME OF THE ISSUER · ISIN · NET SHORT POSITION % · POSITION DATE
robots : hcmc.gr → «User-Agent: * / Disallow:» (επιτρέπει τα πάντα, ελεγμένο 08/10/2026).

Αντιστοίχιση: ΜΕ ISIN, από τον χάρτη `meta.isin` του data.js (τρέχοντα + ΠΑΛΙΑ ISIN από το INDEX
του master). Χωρίς fuzzy ονόματα.

Έξοδος : assets/shorts.js   (το site)
         .github/shorts/<YYYY-MM-DD>.json  (αρχείο εκδόσεων — δικό μας ιστορικό)
         .github/shorts/_state.json        (τελευταία επεξεργασμένη έκδοση)
Σε αποτυχία ή αταίριαστο ISIN → GitHub Issue (ίδιο κανάλι με τον euronext-monitor).
"""
import json, os, re, sys, io, datetime, hashlib
import urllib.request, urllib.error, urllib.parse

PAGE   = 'http://www.hcmc.gr/el_GR/web/portal/shortselling1'
BASE   = 'http://www.hcmc.gr'
UA     = 'AxionMetricsBot/1.0 (+https://www.axionmetrics.gr)'
ROOT   = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # ρίζα repo
OUTJS  = os.path.join(ROOT, 'assets', 'shorts.js')
DATAJS = os.path.join(ROOT, 'assets', 'data.js')
ARCH   = os.path.join(ROOT, '.github', 'shorts')
ALIAS  = os.path.join(ROOT, '.github', 'data', 'fund_aliases.json')
THRESHOLD = 0.5          # όριο δημοσιοποίησης (Καν. ΕΕ 236/2012, άρ. 6)

def log(*a): print(*a, flush=True)

# ---------------------------------------------------------------- GitHub Issue
def issue(title, body):
    tok=os.environ.get('GITHUB_TOKEN'); repo=os.environ.get('GITHUB_REPOSITORY')
    if not tok or not repo:
        log('[issue παραλείπεται — χωρίς GITHUB_TOKEN]', title); return
    req=urllib.request.Request('https://api.github.com/repos/%s/issues'%repo,
        data=json.dumps({'title':title,'body':body,'labels':['shorts']}).encode('utf-8'),
        headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json',
                 'Content-Type':'application/json','User-Agent':UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r: log('issue:', r.status)
    except Exception as e: log('issue ΑΠΕΤΥΧΕ:', e)

def die(msg, detail=''):
    log('ΣΦΑΛΜΑ:', msg); issue('Short θέσεις: '+msg, detail or msg); sys.exit(1)

# ---------------------------------------------------------------- λήψη
def get(url, binary=False, timeout=60):
    req=urllib.request.Request(url, headers={'User-Agent':UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw=r.read()
    return raw if binary else raw.decode('utf-8','replace')

def find_link(html):
    """Το href του αρχείου .xls (ελληνική έκδοση) και η ημερομηνία από το όνομά του."""
    m=re.findall(r'href="([^"]*HCMC_disclosed_short_positions_gr\.xls)"', html, re.I)
    if not m: return None, None
    href=m[-1]
    url = href if href.startswith('http') else BASE + ('' if href.startswith('/') else '/') + href
    d=re.search(r'(\d{4})[_-](\d{2})[_-](\d{2})', href)
    return urllib.parse.quote(url, safe=':/?&=%'), ('%s-%s-%s'%d.groups() if d else None)

# ---------------------------------------------------------------- parsing .xls
def cell_str(v):
    if v is None: return ''
    if isinstance(v, float) and v == int(v): return str(int(v))
    return str(v).strip()

def to_pct(v):
    s=cell_str(v).replace('%','').replace(',','.')
    try: return float(s)
    except ValueError: return None

def to_date(v):
    s=cell_str(v)
    m=re.match(r'^(\d{4})[/\-.](\d{1,2})[/\-.](\d{1,2})$', s)
    if m: return '%04d-%02d-%02d'%tuple(int(x) for x in m.groups())
    m=re.match(r'^(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})$', s)
    if m:
        d,mo,y=(int(x) for x in m.groups()); return '%04d-%02d-%02d'%(y,mo,d)
    return None

def read_sheet(book, names, idx):
    import xlrd
    for n in names:
        for sn in book.sheet_names():
            if sn.strip().lower().startswith(n.lower()): return book.sheet_by_name(sn)
    if idx < book.nsheets: return book.sheet_by_index(idx)
    return None

def rows_of(sh):
    """Γραμμές δεδομένων: όσες έχουν έγκυρο ISIN στη 3η στήλη."""
    out=[]
    if sh is None: return out
    for r in range(sh.nrows):
        vals=[sh.cell_value(r,c) if c < sh.ncols else '' for c in range(5)]
        isin=cell_str(vals[2]).upper()
        if not re.match(r'^[A-Z]{2}[A-Z0-9]{9}\d$', isin): continue
        pct=to_pct(vals[3]); dt=to_date(vals[4])
        if pct is None or dt is None: continue
        out.append({'holder':cell_str(vals[0]),'issuer':cell_str(vals[1]),
                    'isin':isin,'pct':pct,'date':dt})
    return out

# ---------------------------------------------------------------- χάρτης ISIN
def isin_from_datajs(path):
    if not os.path.exists(path): die('λείπει το assets/data.js', path)
    s=io.open(path, encoding='utf-8').read()
    i=s.index('='); j=s.rindex('}')
    try: ax=json.loads(s[i+1:j+1])
    except Exception as e: die('δεν διαβάζεται το data.js', str(e))
    m=((ax.get('meta') or {}).get('isin')) or {}
    if not m: die('το data.js δεν έχει meta.isin — τρέξε τη γέφυρα με τη στήλη «ΠΑΛΙΑ ISIN» (§128)')
    return {k.upper(): v for k, v in m.items()}

# ---------------------------------------------------------------- κανονικοποίηση funds
def load_aliases():
    try: a=json.load(io.open(ALIAS, encoding='utf-8'))
    except Exception: a={}
    return {k:v for k,v in a.items() if not k.startswith('_')}

def norm_key(name):
    s=re.sub(r'[^A-Z0-9]+',' ', name.upper()).strip()
    s=re.sub(r'\b(LIMITED)\b','LTD',s)
    s=re.sub(r'\b(INCORPORATED)\b','INC',s)
    return re.sub(r'\s+',' ',s)

# ---------------------------------------------------------------- δόμηση
def build(cur_rows, hist_rows, pub, isin, aliases):
    unmatched={}; by={}
    seen_names={}
    def canon(h):
        h2=aliases.get(h, h)
        seen_names.setdefault(norm_key(h2), set()).add(h2)
        return h2
    allrows=[dict(r, cur=False) for r in hist_rows]+[dict(r, cur=True) for r in cur_rows]
    for r in allrows:
        tk=isin.get(r['isin'])
        if not tk:
            unmatched.setdefault(r['isin'], r['issuer']); continue
        r['holder']=canon(r['holder'])
        by.setdefault(tk, {}).setdefault(r['holder'], []).append(r)
    out={}
    for tk, funds in by.items():
        fl=[]
        for fund, rs in funds.items():
            rs.sort(key=lambda x: x['date'])
            prev=None; rows=[]
            for r in rs:
                p=round(r['pct'], 2)
                chg=None if prev is None else round(p-prev, 2)
                prev=p
                rows.append({'d':r['date'],'p':p,'c':chg,'x':(p < THRESHOLD)})
            last=rs[-1]
            fl.append({'f':fund,'open':bool(last.get('cur')),'n':len(rows),
                       'lp':round(last['pct'],2),'ld':last['date'],
                       'rows':list(reversed(rows))})
        fl.sort(key=lambda g:(0 if g['open'] else 1, -g['lp'] if g['open'] else 0,
                              '' if g['open'] else g['ld']), reverse=False)
        op=[g for g in fl if g['open']];  op.sort(key=lambda g:-g['lp'])
        cl=[g for g in fl if not g['open']]; cl.sort(key=lambda g:g['ld'], reverse=True)
        out[tk]={'funds':op+cl,
                 'nopen':len(op), 'tot':round(sum(g['lp'] for g in op), 2),
                 'n':sum(g['n'] for g in fl)}
    # ονόματα που διαφέρουν μόνο σε πεζά/κεφαλαία ή Ltd/Limited → πιθανό διπλό
    dups={k:sorted(v) for k,v in seen_names.items() if len(v) > 1}
    return out, unmatched, dups

# ---------------------------------------------------------------- main
def main():
    local=None
    if '--local' in sys.argv: local=sys.argv[sys.argv.index('--local')+1]
    os.makedirs(ARCH, exist_ok=True)
    state_p=os.path.join(ARCH, '_state.json')
    state=json.load(io.open(state_p, encoding='utf-8')) if os.path.exists(state_p) else {}

    if local:
        raw=open(local,'rb').read(); src_date=state.get('src') or 'local'; url=local
    else:
        try: html=get(PAGE)
        except Exception as e: die('δεν ανοίγει η σελίδα της Επιτροπής Κεφαλαιαγοράς', '%s\n%s'%(PAGE, e))
        url, src_date = find_link(html)
        if not url:
            die('δεν βρέθηκε ο σύνδεσμος του αρχείου στη σελίδα',
                'Η σελίδα %s δεν περιέχει πια href προς «…HCMC_disclosed_short_positions_gr.xls». '
                'Πιθανή αλλαγή δομής — χρειάζεται έλεγχος.'%PAGE)
        if src_date and state.get('src')==src_date:
            log('καμία αλλαγή (έκδοση %s) — τέλος.'%src_date); return 0
        log('νέα έκδοση:', src_date, url)
        try: raw=get(url, binary=True)
        except Exception as e: die('δεν κατεβαίνει το αρχείο', '%s\n%s'%(url, e))

    sha=hashlib.sha1(raw).hexdigest()[:12]
    try:
        import xlrd
        book=xlrd.open_workbook(file_contents=raw)
    except Exception as e:
        die('δεν διαβάζεται το .xls', str(e))

    sh_cur =read_sheet(book, ['Τρέχουσες','Current'], 0)
    sh_hist=read_sheet(book, ['Ιστορικό','Histor'], 1)
    sh_pub =read_sheet(book, ['Ημερομηνία','Publication'], 2)
    cur_rows, hist_rows = rows_of(sh_cur), rows_of(sh_hist)
    if not hist_rows and not cur_rows:
        die('το αρχείο δεν έδωσε καμία γραμμή', 'φύλλα: %s'%book.sheet_names())
    pub=None
    if sh_pub is not None:
        for r in range(sh_pub.nrows):
            for c in range(sh_pub.ncols):
                pub=to_date(sh_pub.cell_value(r,c)) or pub
    pub=pub or src_date

    isin=isin_from_datajs(DATAJS)
    by, unmatched, dups = build(cur_rows, hist_rows, pub, isin, load_aliases())

    payload={'pub':pub,'src':src_date,'sha':sha,
             'built':datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
             'threshold':THRESHOLD,'by':by}
    io.open(OUTJS,'w',encoding='utf-8').write(
        '/* Axion Metrics — short θέσεις (Επιτροπή Κεφαλαιαγοράς). ΠΑΡΑΓΕΤΑΙ ΑΥΤΟΜΑΤΑ από\n'
        '   .github/scripts/shorts.py · έκδοση πηγής %s · ΜΗΝ το επεξεργάζεσαι με το χέρι. */\n'
        'window.AXION_SHORTS = %s;\n'%(src_date, json.dumps(payload, ensure_ascii=False, separators=(',',':'))))
    io.open(os.path.join(ARCH,'%s.json'%src_date),'w',encoding='utf-8').write(
        json.dumps(payload, ensure_ascii=False, indent=1))
    # το state γράφεται ΜΕΤΑ τα issues ώστε να μη χαθεί ειδοποίηση αν σκάσει κάτι ενδιάμεσα

    log('εταιρείες: %d · με ανοιχτή θέση: %d · γραμμές: %d'%(
        len(by), sum(1 for v in by.values() if v['nopen']), sum(v['n'] for v in by.values())))
    known_un=set(state.get('unmatched') or [])
    new_un={k:v for k,v in unmatched.items() if k not in known_un}
    known_dp=set(state.get('dups') or [])
    new_dp={k:v for k,v in dups.items() if k not in known_dp}
    if unmatched: log('ΑΤΑΙΡΙΑΣΤΑ ISIN:', unmatched, '(νέα: %d)'%len(new_un))
    if new_un:
        unmatched=new_un
        issue('Short θέσεις: %d ISIN χωρίς αντιστοίχιση'%len(unmatched),
              'Οι παρακάτω εκδότες υπάρχουν στο αρχείο της Επιτροπής αλλά το ISIN τους δεν βρέθηκε '
              'στο INDEX ΕΠΙΧΕΙΡΗΣΕΩΝ του master (στήλες «ISIN» / «ΠΑΛΙΑ ISIN»):\n\n'
              + '\n'.join('- `%s` — %s'%(k,v) for k,v in sorted(unmatched.items()))
              + '\n\nΑν η εταιρεία είναι εντός κάλυψης, συμπλήρωσε το ISIN στο master και τρέξε τη γέφυρα. '
                'Αν είναι εκτός κάλυψης (π.χ. διαγραμμένη), δεν χρειάζεται ενέργεια.')
    if new_dp:
        dups=new_dp
        issue('Short θέσεις: πιθανά διπλά ονόματα fund',
              'Τα παρακάτω ονόματα μοιάζουν ίδια μετά την κανονικοποίηση αλλά γράφονται διαφορετικά:\n\n'
              + '\n'.join('- %s'%(' · '.join('`%s`'%x for x in v)) for v in dups.values())
              + '\n\nΑν πρόκειται για την ΙΔΙΑ νομική οντότητα, πρόσθεσέ τα στο '
                '`.github/data/fund_aliases.json`. Αν είναι διαφορετικοί υπόχρεοι, άφησέ τα ως έχουν.')
    json.dump({'src':src_date,'sha':sha,'pub':pub,
               'unmatched':sorted(set(list(known_un)+list(unmatched))),
               'dups':sorted(set(list(known_dp)+list(dups)))},
              io.open(state_p,'w',encoding='utf-8'), ensure_ascii=False)
    return 0

if __name__ == '__main__':
    sys.exit(main())
