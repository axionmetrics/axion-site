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
         ΑΚΡΙΒΕΙΑ: η στήλη του ποσοστού ΔΕΝ είναι 2 δεκαδικών. Ο Καν. (ΕΕ) 826/2012 (Παράρτ. Ι,
         πίν. 1, πεδίο 13) απαιτεί «rounded to 2 decimal places» ως ΕΛΑΧΙΣΤΟ, αλλά η Επιτροπή
         δημοσιεύει ό,τι της δηλώνεται: στην έκδοση 09/10/2026, 101 από τις 415 γραμμές έχουν
         4–5 δεκαδικά (π.χ. 1.05351, 0.79475). Κρατάμε την ΠΗΓΑΙΑ ακρίβεια (5 δεκαδικά· η
         στρογγυλοποίηση υπάρχει μόνο για να μη μπαίνει θόρυβος float) και αφήνουμε την
         εμφάνιση να αποφασίσει πόσα δεκαδικά δείχνει. Με 2 δεκαδικά χάνονταν 101 τιμές και
         94 διακριτές θέσεις ισοπεδώνονταν σε κοινές.
robots : hcmc.gr → «User-Agent: * / Disallow:» (επιτρέπει τα πάντα, ελεγμένο 08/10/2026).

Αντιστοίχιση: ΜΕ ISIN, από τον χάρτη `meta.isin` του data.js (τρέχοντα + ΠΑΛΙΑ ISIN από το INDEX
του master). Χωρίς fuzzy ονόματα.

Έξοδος : assets/shorts.js   (το site)
         .github/shorts/<YYYY-MM-DD>.json  (αρχείο εκδόσεων — δικό μας ιστορικό)
         .github/shorts/_state.json        (τελευταία επεξεργασμένη έκδοση)
         .github/shorts/fca_history.json   (§143 — ΣΥΣΣΩΡΕΥΤΙΚΟ ιστορικό FCA: ANSP + ονομαστικό ≤10/07/2026)
Δεύτερη πηγή (§140): FCA — https://www.fca.org.uk/publication/documents/aggregated-current-net-short-positions.csv
         Στήλες: Name of Company · ISIN · Aggregated net short position (%) · Position date (dd/mm/yyyy).
         Αφορά μετοχές εισηγμένες σε βρετανικό τόπο διαπραγμάτευσης. Από τις δικές μας, ΔΥΟ
         (ελεγμένο 21/10/2026): 34 METLEN ENERGY & METALS (GB00BTQGS779) και
         11 COCA-COLA HBC (CH0198251305). Κανένα ΕΛΛΗΝΙΚΟ ISIN (GRS…) δεν υπάρχει εκεί.
Τρίτη πηγή (§142.2): ESMA — κατάλογος ΕΞΑΙΡΟΥΜΕΝΩΝ μετοχών, άρθρο 16 Καν. (ΕΕ) 236/2012.
         Όταν η ΚΥΡΙΑ αγορά διαπραγμάτευσης μιας μετοχής εισηγμένης στην ΕΕ βρίσκεται σε
         τρίτη χώρα, τα άρθρα 5 (γνωστοποίηση) και 6 (δημοσιοποίηση) ΔΕΝ εφαρμόζονται: η
         Επιτροπή Κεφαλαιαγοράς δεν λαμβάνει και δεν δημοσιεύει ΤΙΠΟΤΑ για τη μετοχή, σε
         κανένα μέγεθος. Αυτό ΔΕΝ είναι το ίδιο με «καμία θέση δεν έφτασε το 0,5%» και
         πρέπει να φαίνεται ρητά στη σελίδα — αλλιώς η άδεια στήλη διαβάζεται ως απουσία
         θέσεων. Σήμερα αφορά ΜΟΝΟ την 11 COCA-COLA HBC (κύρια αγορά: LSE από το Brexit·
         εξαίρεση από 16/03/2021). Η ESMA επαναπροσδιορίζει την κύρια αγορά τουλάχιστον
         ΚΑΘΕ ΔΙΕΤΙΑ, γι' αυτό ο κατάλογος διαβάζεται σε κάθε εκτέλεση και κάθε μεταβολή
         ανοίγει Issue.

ΑΔΕΙΑ ΧΡΗΣΗΣ FCA — ΑΝΟΙΧΤΟ: οι όροι (fca.org.uk/legal) δίνουν Open Government Licence για
         «charts, tables and numerical datasets» της ενότητας Data, αλλά γενικά απαιτούν γραπτή
         άδεια για αναπαραγωγή σε άλλον ιστότοπο και ζητούν αναφορά πηγής. Τα αρχεία ANSP
         βρίσκονται σε /publication/documents/, όχι /publication/data/ — δεν είναι σαφές ποια
         ρήτρα ισχύει. Μέχρι να απαντήσει η FCA, ο διακόπτης FCA_ON ελέγχει τη δημοσίευση.

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

# ── §140 — ΔΕΥΤΕΡΗ ΠΗΓΗ: FCA (Ηνωμένο Βασίλειο) ──────────────────────────────
# Η 34 METLEN ENERGY & METALS είναι από 04/08/2025 εισηγμένη στο LSE ως βρετανική plc
# με ISIN GB00BTQGS779 (υπάρχει ήδη στον χάρτη meta.isin του master). Οι θέσεις της
# δηλώνονται και στην FCA, με ΑΛΛΟ καθεστώς:
#   • Επιτροπή Κεφαλαιαγοράς: ΟΝΟΜΑΣΤΙΚΕΣ θέσεις ≥0,5% (Καν. ΕΕ 236/2012)
#   • FCA από 13/07/2026    : ΑΝΩΝΥΜΟ ΑΘΡΟΙΣΜΑ όλων των θέσεων από 0,2% (ANSP),
#                             δημοσίευση κάθε εργάσιμη από 12:00 Λονδίνου, βάση T+2
# Δεν είναι αντίφαση όταν διαφέρουν — μετρούν διαφορετικό πράγμα. Γι' αυτό μπαίνουν
# ΔΙΠΛΑ, σε ξεχωριστό κλειδί `fca`, και ΠΟΤΕ δεν αθροίζονται με τα ελληνικά.
# Αποτυχία της FCA ΔΕΝ ρίχνει τη ροή: η ελληνική πηγή είναι η κύρια.
FCA_ON   = True          # διακόπτης δημοσίευσης (βλ. ΑΔΕΙΑ ΧΡΗΣΗΣ στο docstring)
FCA_CSV  = 'https://www.fca.org.uk/publication/documents/aggregated-current-net-short-positions.csv'
FCA_THR  = 0.2           # κατώφλι αναφοράς του βρετανικού καθεστώτος
FCA_ATTR = '© The Financial Conduct Authority'
# ── §143 — ΙΣΤΟΡΙΚΟ FCA (δικό μας αρχείο, ΣΥΣΣΩΡΕΥΤΙΚΟ) ──────────────────────
# Η FCA δημοσιεύει, εκτός από το τρέχον ANSP, και πίνακα ΙΣΤΟΡΙΚΩΝ ANSP (κάθε τιμή που
# αντικαταστάθηκε, με την ημερομηνία που έγινε ιστορική). Δεν τον εμπιστευόμαστε ως
# μοναδικό αρχείο: στις πρώτες εκδόσεις του νέου καθεστώτος χάθηκαν/διπλασιάστηκαν
# γραμμές, και ο Handbook (SSR 6.3) επιτρέπει στην FCA να ΑΝΑΘΕΩΡΕΙ δημοσιευμένα ANSP.
# Γι' αυτό κρατάμε ΔΙΚΟ μας αρχείο `.github/shorts/fca_history.json`:
#   • κάθε εκτέλεση ενώνει (upsert) το τρέχον + το ιστορικό CSV, ΜΟΝΟ για ISIN της κάλυψής μας
#   • ΠΟΤΕ δεν σβήνεται γραμμή επειδή εξαφανίστηκε από την FCA
#   • αν η FCA αλλάξει τιμή για ημερομηνία που ήδη έχουμε, η παλιά κρατιέται στο `rev`
# Το ΠΑΛΙΟ καθεστώς (ονομαστικές θέσεις ≥0,5%, έως 10/07/2026) είναι ΠΑΓΩΜΕΝΟ: φορτώθηκε
# μία φορά από το short-positions-daily-update.xlsx στο κλειδί `legacy` και δεν ξαναγγίζεται.
FCA_HIST_CSV = 'https://www.fca.org.uk/publication/documents/aggregated-historic-net-short-positions.csv'
FCA_LEGACY_XLSX = 'https://www.fca.org.uk/publication/data/short-positions-daily-update.xlsx'
FCA_LEGACY_END = '2026-07-10'   # τελευταία έκδοση του ονομαστικού καθεστώτος
FCA_ARCH = os.path.join(ARCH, 'fca_history.json')
FCA_CUR_RAW = None
# ── §142.2 — ΤΡΙΤΗ ΠΗΓΗ: ESMA, κατάλογος εξαιρούμενων μετοχών (άρθρο 16) ─────
# Δημόσιο Solr του μητρώου της ESMA. Ζητάμε ΜΟΝΟ τις εγγραφές με αρμόδια αρχή την
# Επιτροπή Κεφαλαιαγοράς (countryCode=GR) — για μετοχή εισηγμένη στο ΧΑ αυτή είναι η
# αρμόδια αρχή του ενωσιακού τόπου διαπραγμάτευσης. Κάθε ISIN εμφανίζεται πολλαπλά
# (status NEW / Unchanged / Updated / Not effective yet)· κρατάμε μία εγγραφή ανά ISIN.
# Λήξη «31/12/9999» = σε ισχύ χωρίς ημερομηνία λήξης.
ESMA_ON  = True
ESMA_URL = 'https://registers.esma.europa.eu/solr/esma_registers_mifid_shsexs/select'
DEC       = 5            # δεκαδικά που κρατάμε από την πηγή (βλ. ΑΚΡΙΒΕΙΑ στο docstring)
FMT       = 5            # έκδοση μορφής εξόδου. ΑΥΞΗΣΕ ΤΟ όταν αλλάζει ο τρόπος που γράφονται
                         # τα δεδομένα: αναγκάζει πλήρη ανακατασκευή ακόμη κι αν η πηγή είναι ίδια.

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

# ---------------------------------------------------------------- FCA (§140)
def fca_fetch(isin_map):
    """Επιστρέφει (block, sha) ή (None, None). ΔΕΝ πετάει ποτέ — η FCA είναι δευτερεύουσα."""
    if not FCA_ON:
        log('FCA: απενεργοποιημένη (FCA_ON=False)'); return None, None
    try:
        raw=get(FCA_CSV, binary=True, timeout=45)
    except Exception as e:
        log('FCA: δεν κατεβαίνει το CSV —', e); return None, None
    sha=hashlib.sha1(raw).hexdigest()[:12]
    global FCA_CUR_RAW; FCA_CUR_RAW=raw      # §143 — το ίδιο αρχείο τροφοδοτεί και το ιστορικό
    try:
        import csv
        txt=raw.decode('utf-8-sig','replace')
        rd=list(csv.reader(io.StringIO(txt)))
    except Exception as e:
        log('FCA: δεν διαβάζεται το CSV —', e); return None, None
    if not rd or len(rd) < 2:
        log('FCA: κενό CSV'); return None, None
    # Εντοπισμός στηλών από την κεφαλίδα· αν αλλάξει η σειρά, δεν σπάει.
    hdr=[c.strip().lower() for c in rd[0]]
    def col(*keys, default=None):
        for i,h in enumerate(hdr):
            if any(k in h for k in keys): return i
        return default
    i_name=col('name of company','company','issuer', default=0)
    i_isin=col('isin', default=1)
    i_pct =col('net short position','position (%)','%', default=2)
    i_date=col('position date','date', default=3)
    by={}; latest=None; n=0
    for r in rd[1:]:
        if len(r) <= max(i_name,i_isin,i_pct,i_date): continue
        code=(r[i_isin] or '').strip().upper()
        if not re.match(r'^[A-Z]{2}[A-Z0-9]{9}\d$', code): continue
        n+=1
        tk=isin_map.get(code)
        if not tk: continue
        try: pct=float((r[i_pct] or '').strip().replace(',','.'))
        except ValueError: continue
        d=to_date((r[i_date] or '').strip())
        if d is None: continue
        prev=by.get(tk)
        if prev is None or d >= prev['d']:
            by[tk]={'p':round(pct,2),'d':d,'co':(r[i_name] or '').strip()}
        latest=d if (latest is None or d > latest) else latest
    log('FCA: %d γραμμές στο αρχείο · %d αντιστοιχίστηκαν (%s)'%(n, len(by), ', '.join(sorted(by)) or '—'))
    if not by:
        # Δεν είναι σφάλμα από μόνο του: αν η METLEN βγει από τη λίστα, απλώς δεν υπάρχει θέση.
        return {'rows':{}, 'pub':latest, 'n':n, 'threshold':FCA_THR, 'attr':FCA_ATTR}, sha
    return {'rows':by, 'pub':latest, 'n':n, 'threshold':FCA_THR, 'attr':FCA_ATTR}, sha

# ------------------------------------------------- §143 ιστορικό FCA
def _csv_rows(raw):
    import csv
    rd=list(csv.reader(io.StringIO(raw.decode('utf-8-sig','replace'))))
    if not rd: return [], []
    return [c.strip().lower() for c in rd[0]], rd[1:]

def _col(hdr, *keys, default=None):
    for i,h in enumerate(hdr):
        if any(k in h for k in keys): return i
    return default

def fca_ansp_rows(raw, isin_set, historic):
    """Γραμμές (isin, co, d, p, h) από CSV της FCA — μόνο για ISIN της κάλυψής μας."""
    hdr, body = _csv_rows(raw)
    i_name=_col(hdr,'name of company','company', default=0)
    i_isin=_col(hdr,'isin', default=1)
    i_pct =_col(hdr,'net short position','%', default=2)
    i_date=_col(hdr,'position date', default=3)
    i_hist=_col(hdr,'became histor', default=4) if historic else None
    out=[]
    for r in body:
        need=max(x for x in (i_name,i_isin,i_pct,i_date,i_hist) if x is not None)
        if len(r) <= need: continue
        code=(r[i_isin] or '').strip().upper()
        if code not in isin_set: continue
        try: p=round(float((r[i_pct] or '').strip().replace(',','.')),2)
        except ValueError: continue
        d=to_date((r[i_date] or '').strip())
        if not d: continue
        h=to_date((r[i_hist] or '').strip()) if i_hist is not None else None
        out.append((code,(r[i_name] or '').strip(),d,p,h))
    return out

def fca_legacy(isin_set):
    """ΜΙΑ φορά: ονομαστικές θέσεις του παλιού καθεστώτος (≤10/07/2026) για τα ISIN μας."""
    try: import openpyxl
    except ImportError:
        log('FCA legacy: λείπει το openpyxl — παραλείπεται (το αρχείο σπέρνεται χειροκίνητα)'); return None
    try: raw=get(FCA_LEGACY_XLSX, binary=True, timeout=120)
    except Exception as e:
        log('FCA legacy: δεν κατεβαίνει —', e); return None
    wb=openpyxl.load_workbook(io.BytesIO(raw), read_only=True, data_only=True)
    out={}
    for ws in wb.worksheets:
        for r in ws.iter_rows(values_only=True):
            if not r or len(r) < 5: continue
            code=(str(r[2] or '')).strip().upper()
            if code not in isin_set: continue
            d=r[4]
            d=d.strftime('%Y-%m-%d') if hasattr(d,'strftime') else to_date(str(d))
            try: p=round(float(r[3]),5)
            except (TypeError, ValueError): continue
            if not d: continue
            e=out.setdefault(code, {'co':str(r[1] or '').strip(), 'rows':[]})
            row={'f':str(r[0] or '').strip(),'d':d,'p':p}
            if row not in e['rows']: e['rows'].append(row)
    for e in out.values(): e['rows'].sort(key=lambda x:(x['f'],x['d']))
    log('FCA legacy: %d ISIN · %d γραμμές'%(len(out), sum(len(e['rows']) for e in out.values())))
    return out

def fca_history(isin_map, cur_raw):
    """Ενημερώνει το .github/shorts/fca_history.json και επιστρέφει (arch, sha).
    ΔΕΝ πετάει ποτέ — σε αποτυχία κρατά ό,τι υπάρχει ήδη."""
    isin_set=set(isin_map)
    try: arch=json.load(io.open(FCA_ARCH, encoding='utf-8'))
    except Exception: arch={}
    arch.setdefault('ansp', {})
    today=datetime.date.today().isoformat()
    if 'legacy' not in arch:
        lg=fca_legacy(isin_set)
        if lg is not None: arch['legacy']=lg; arch['legacy_end']=FCA_LEGACY_END
    rows=[]
    try:
        rows+=fca_ansp_rows(get(FCA_HIST_CSV, binary=True, timeout=60), isin_set, True)
    except Exception as e:
        log('FCA ιστορικό: δεν κατεβαίνει —', e)
    if cur_raw:
        try: rows+=fca_ansp_rows(cur_raw, isin_set, False)
        except Exception as e: log('FCA τρέχον: δεν διαβάζεται για το ιστορικό —', e)
    # Κλειδί μιας δημοσίευσης = (ημερομηνία θέσης, ημερομηνία που έγινε ιστορική). Η ΙΔΙΑ
    # ημερομηνία θέσης μπορεί να δημοσιευτεί δύο φορές με άλλο ποσοστό (π.χ. 34 METLEN,
    # θέση 15/10/2026: 6,76% → ιστορική 19/10, και 6,47% στο τρέχον) — αυτό ΔΕΝ είναι
    # αναθεώρηση, είναι δύο διαδοχικά ANSP. Αναθεώρηση = ίδιο (d,h), άλλο ποσοστό.
    added=revised=0
    for code,co,d,p,h in rows:
        e=arch['ansp'].setdefault(code, {'co':co, 'rows':[]})
        L=e['rows']
        if h:
            x=next((r for r in L if r['d']==d and r.get('h')==h), None)
            if x is not None:
                if x['p']!=p:
                    x.setdefault('rev', []).append({'p':x['p'],'at':today}); x['p']=p; revised+=1
                continue
            x=next((r for r in L if r['d']==d and not r.get('h') and r['p']==p), None)
            if x is not None: x['h']=h; continue      # το τρέχον έγινε ιστορικό
        else:
            if any(r['d']==d and r['p']==p for r in L): continue
        L.append({'d':d,'p':p,'h':h,'seen':today}); added+=1
    # ⚠ ΑΝΑΛΛΟΙΩΤΟ: το ΤΡΕΧΟΝ αρχείο ANSP έχει ΑΚΡΙΒΩΣ ΜΙΑ ανοιχτή θέση ανά ISIN, άρα μέσα
    # σε κάθε ISIN επιτρέπεται ΜΙΑ μόνο γραμμή χωρίς `h`. Παλιότερες «τρέχουσες» που δεν
    # εμφανίστηκαν ποτέ στο ιστορικό CSV (η FCA δεν δημοσιεύει κάθε ενδιάμεσο βήμα) έμεναν
    # ΓΙΑ ΠΑΝΤΑ σημειωμένες ως τρέχουσες — 34 METLEN, θέση 15/10/2026 με 6,24% και 6,47%
    # δίπλα στο 6,76% που είχε κανονικά κλείσει στις 19/10.
    # Κλείνουν με `sup` = η ΔΙΚΗ ΜΑΣ ημερομηνία παρατήρησης. Το `h` μένει ΑΠΟΚΛΕΙΣΤΙΚΑ για
    # την ημερομηνία που δηλώνει η ίδια η FCA — τα δύο δεν ανακατεύονται.
    # ΑΣΦΑΛΕΙΑ: αν το τρέχον αρχείο δεν διαβάστηκε για κάποιο ISIN, ΔΕΝ κλείνει τίποτε.
    cur_key={}
    for code,co,d,p,h in rows:
        if not h: cur_key[code]=(d,p)
    closed=0
    for code,e in arch['ansp'].items():
        k=cur_key.get(code)
        if k is None: continue
        for r in e['rows']:
            if r.get('h') or r.get('sup'): continue
            if (r['d'],r['p'])!=k: r['sup']=today; closed+=1
    for e in arch['ansp'].values():
        e['rows'].sort(key=lambda r:(r['d'], r.get('h') or '9999-99-99'))
    blob=json.dumps(arch, ensure_ascii=False, sort_keys=True)
    sha=hashlib.sha1(blob.encode('utf-8')).hexdigest()[:12]
    log('FCA ιστορικό: %d ISIN · %d θέσεις · νέες %d · αναθεωρήσεις %d · έκλεισαν %d'
        %(len(arch['ansp']), sum(len(e['rows']) for e in arch['ansp'].values()), added, revised, closed))
    return arch, sha, revised

def fca_hist_payload(arch, isin_map):
    """Για το site: ANSP σειρά ανά ticker (νεότερη πρώτη) + ονομαστικό ιστορικό (legacy)."""
    hist={}; leg={}
    for code,e in (arch.get('ansp') or {}).items():
        tk=isin_map.get(code)
        if not tk: continue
        # [ημ. θέσης, %, ημ. που έγινε ιστορική ή null = τρέχον] — νεότερη πρώτη
        hist[tk]=[[r['d'],r['p'],r.get('h')] for r in reversed(e['rows'])]
    for code,e in (arch.get('legacy') or {}).items():
        tk=isin_map.get(code)
        if not tk: continue
        funds={}
        for r in e['rows']: funds.setdefault(r['f'], []).append(r)
        fl=[]
        for f,rs in funds.items():
            rs.sort(key=lambda x:x['d']); prev=None; out=[]
            for r in rs:
                c=None if prev is None else round(r['p']-prev, DEC); prev=r['p']
                out.append({'d':r['d'],'p':r['p'],'c':c,'x':(r['p'] < THRESHOLD)})
            last=rs[-1]
            # «open» = ήταν ακόμη ≥0,5% όταν έπαψε το ονομαστικό καθεστώς (όχι «ανοιχτή σήμερα»)
            fl.append({'f':f,'open':last['p'] >= THRESHOLD,'n':len(out),
                       'lp':last['p'],'ld':last['d'],'rows':list(reversed(out))})
        op=sorted([g for g in fl if g['open']], key=lambda g:-g['lp'])
        cl=sorted([g for g in fl if not g['open']], key=lambda g:g['ld'], reverse=True)
        leg[tk]={'end':arch.get('legacy_end', FCA_LEGACY_END),'funds':op+cl,
                 'nopen':len(op),'n':sum(g['n'] for g in fl)}
    return hist, leg

# ------------------------------------------------- §142.2 ESMA: εξαιρούμενες
def esma_exempt(isin_map):
    """Ποιες ΔΙΚΕΣ ΜΑΣ μετοχές εξαιρούνται από τα άρθρα 5 & 6 (άρθρο 16 Καν. 236/2012).

    Επιστρέφει (dict ticker→{'isin':…,'since':'YYYY-MM-DD'}, sha) ή (None, None).
    ΔΕΝ πετάει ποτέ: η εξαίρεση είναι συμπληρωματική πληροφορία, δεν ρίχνει τη ροή.
    """
    if not ESMA_ON:
        log('ESMA: απενεργοποιημένη (ESMA_ON=False)'); return None, None
    q=urllib.parse.urlencode({'q':'shs_countryCode:GR','rows':'500','wt':'json',
                              'fl':'shs_isin,shs_name,shs_exemptionStartDateStr,shs_exemptionEndDateStr'})
    try:
        raw=get(ESMA_URL+'?'+q, binary=True, timeout=45)
        docs=json.loads(raw.decode('utf-8','replace'))['response']['docs']
    except Exception as e:
        log('ESMA: δεν διαβάζεται ο κατάλογος —', e); return None, None
    def iso(d):
        m=re.match(r'^(\d{2})/(\d{2})/(\d{4})$', (d or '').strip())
        return '%s-%s-%s'%(m.group(3),m.group(2),m.group(1)) if m else None
    today=datetime.date.today().isoformat()
    best={}
    for d in docs:
        code=(d.get('shs_isin') or '').strip().upper()
        end=iso(d.get('shs_exemptionEndDateStr')); start=iso(d.get('shs_exemptionStartDateStr'))
        if not code or not start: continue
        if end and end < today: continue          # έληξε
        if start > today: continue                # δεν ισχύει ακόμη
        if code not in best or start < best[code]['since']:
            best[code]={'since':start,'name':(d.get('shs_name') or '').strip()}
    out={}
    for code,v in best.items():
        tk=isin_map.get(code)
        if tk: out[tk]={'isin':code,'since':v['since']}
        else:  log('ESMA: εξαιρούμενη εκτός κάλυψης — %s %s'%(code, v['name']))
    sha=hashlib.sha1(json.dumps(out, sort_keys=True).encode('utf-8')).hexdigest()[:12]
    log('ESMA: %d εγγραφές GR · %d σε ισχύ · %d δικές μας (%s)'
        %(len(docs), len(best), len(out), ', '.join(sorted(out)) or '—'))
    return out, sha

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
                p=round(r['pct'], DEC)
                chg=None if prev is None else round(p-prev, DEC)
                prev=p
                rows.append({'d':r['date'],'p':p,'c':chg,'x':(p < THRESHOLD)})
            last=rs[-1]
            fl.append({'f':fund,'open':bool(last.get('cur')),'n':len(rows),
                       'lp':round(last['pct'],DEC),'ld':last['date'],
                       'rows':list(reversed(rows))})
        fl.sort(key=lambda g:(0 if g['open'] else 1, -g['lp'] if g['open'] else 0,
                              '' if g['open'] else g['ld']), reverse=False)
        op=[g for g in fl if g['open']];  op.sort(key=lambda g:-g['lp'])
        cl=[g for g in fl if not g['open']]; cl.sort(key=lambda g:g['ld'], reverse=True)
        out[tk]={'funds':op+cl,
                 'nopen':len(op), 'tot':round(sum(g['lp'] for g in op), DEC),
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

    # §140 — η FCA κατεβαίνει ΠΡΙΝ τον έλεγχο έκδοσης: μπορεί να έχει αλλάξει ακόμη κι αν
    # το αρχείο της Επιτροπής Κεφαλαιαγοράς είναι το ίδιο (δημοσιεύει κάθε εργάσιμη).
    isin=isin_from_datajs(DATAJS)
    fca_block, fca_sha = fca_fetch(isin)
    fca_arch, fh_sha, fh_rev = (None, None, 0)
    if FCA_ON:
        fca_arch, fh_sha, fh_rev = fca_history(isin, FCA_CUR_RAW)
    exempt, ex_sha = esma_exempt(isin)

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
        if (src_date and state.get('src')==src_date and state.get('fmt')==FMT
                and state.get('fca')==fca_sha and state.get('esma')==ex_sha
                and state.get('fcah')==fh_sha):
            log('καμία αλλαγή (έκδοση %s, μορφή %d, FCA %s, ιστορικό FCA %s, ESMA %s) — τέλος.'
                %(src_date, FMT, fca_sha or '—', fh_sha or '—', ex_sha or '—')); return 0
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

    by, unmatched, dups = build(cur_rows, hist_rows, pub, isin, load_aliases())

    payload={'pub':pub,'src':src_date,'sha':sha,
             'built':datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
             'threshold':THRESHOLD,'by':by}
    # §140 — ΔΙΠΛΑ, όχι ανακατεμένα: άλλο καθεστώς, άλλο κατώφλι, χωρίς ονόματα κατόχων.
    if fca_block: payload['fca']=fca_block
    # §143 — ιστορικό FCA: ANSP σειρά (`hist`) + ονομαστικές θέσεις έως 10/07/2026 (`legacy`).
    # Το αρχείο γράφεται ΕΔΩ (όχι νωρίτερα) για να μη μένει ενημερωμένο ιστορικό χωρίς shorts.js.
    if fca_arch is not None:
        io.open(FCA_ARCH,'w',encoding='utf-8').write(
            json.dumps(fca_arch, ensure_ascii=False, indent=1, sort_keys=True))
        h, lg = fca_hist_payload(fca_arch, isin)
        if fca_block is None and (h or lg):
            fca_block={'rows':{}, 'pub':None, 'n':0, 'threshold':FCA_THR, 'attr':FCA_ATTR}
            payload['fca']=fca_block
        if fca_block is not None:
            fca_block['hist']=h; fca_block['legacy']=lg
    # §142.2 — ποιες μετοχές ΔΕΝ υπάγονται καν στο ελληνικό καθεστώς. Το site το λέει
    # ρητά στη σελίδα τους αντί να δείχνει άδεια στήλη.
    if exempt: payload['exempt']=exempt
    io.open(OUTJS,'w',encoding='utf-8').write(
        '/* Axion Metrics — short θέσεις. ΠΑΡΑΓΕΤΑΙ ΑΥΤΟΜΑΤΑ από .github/scripts/shorts.py\n'
        '   · ονομαστικές θέσεις ≥0,5%%: Επιτροπή Κεφαλαιαγοράς (έκδοση %s)\n'
        '   · κλειδί `fca`: ανώνυμο άθροισμα από 0,2%%, Financial Conduct Authority (§140)\n'
        '   · κλειδί `exempt`: μετοχές εκτός άρθρων 5 & 6 (άρθρο 16 Καν. 236/2012, ESMA)\n'
        '   ΜΗΝ το επεξεργάζεσαι με το χέρι. */\n'
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
    # §142.2 — ο κατάλογος της ESMA αλλάζει σπάνια αλλά όταν αλλάζει, αλλάζει το νόημα
    # ολόκληρης της στήλης: μετοχή που μπαίνει σταματά να έχει ελληνικές γνωστοποιήσεις,
    # μετοχή που βγαίνει αρχίζει να έχει. Κάθε μεταβολή θέλει ανθρώπινο μάτι.
    if ex_sha and state.get('esma') and state.get('esma')!=ex_sha:
        old=set((state.get('exempt') or {}).keys()); new=set((exempt or {}).keys())
        issue('Short θέσεις: άλλαξε ο κατάλογος εξαιρούμενων μετοχών της ESMA',
              'Ο κατάλογος του άρθρου 16 (Καν. ΕΕ 236/2012 — κύρια αγορά σε τρίτη χώρα) άλλαξε.\n\n'
              + '- μπήκαν: %s\n- βγήκαν: %s\n- τώρα: %s\n\n'
                %(', '.join(sorted(new-old)) or '—', ', '.join(sorted(old-new)) or '—',
                  ', '.join('%s (%s, από %s)'%(k,v['isin'],v['since'])
                            for k,v in sorted((exempt or {}).items())) or '—')
              + 'Για όσες ΜΠΗΚΑΝ: η Επιτροπή Κεφαλαιαγοράς παύει να δημοσιεύει γνωστοποιήσεις '
                'και η σελίδα τους πρέπει να το λέει ρητά (το κάνει αυτόματα από αυτό το κλειδί). '
                'Για όσες ΒΓΗΚΑΝ: επανέρχονται στο ελληνικό καθεστώς ≥0,5%. '
                'Πηγή: https://registers.esma.europa.eu/ (esma_registers_mifid_shsexs).')
    if new_dp:
        dups=new_dp
        issue('Short θέσεις: πιθανά διπλά ονόματα fund',
              'Τα παρακάτω ονόματα μοιάζουν ίδια μετά την κανονικοποίηση αλλά γράφονται διαφορετικά:\n\n'
              + '\n'.join('- %s'%(' · '.join('`%s`'%x for x in v)) for v in dups.values())
              + '\n\nΑν πρόκειται για την ΙΔΙΑ νομική οντότητα, πρόσθεσέ τα στο '
                '`.github/data/fund_aliases.json`. Αν είναι διαφορετικοί υπόχρεοι, άφησέ τα ως έχουν.')
    if fh_rev:
        issue('Short θέσεις: η FCA αναθεώρησε %d ιστορικές τιμές ANSP'%fh_rev,
              'Τιμές ANSP που είχαμε ήδη αποθηκεύσει δημοσιεύτηκαν με άλλο ποσοστό. Οι νέες τιμές '
              'ισχύουν· οι παλιές κρατήθηκαν στο πεδίο `rev` του `.github/shorts/fca_history.json`.')
    json.dump({'src':src_date,'sha':sha,'pub':pub,'fmt':FMT,'fca':fca_sha,'fcah':fh_sha,
               'esma':ex_sha,'exempt':exempt or {},
               'unmatched':sorted(set(list(known_un)+list(unmatched))),
               'dups':sorted(set(list(known_dp)+list(dups)))},
              io.open(state_p,'w',encoding='utf-8'), ensure_ascii=False)
    return 0

if __name__ == '__main__':
    sys.exit(main())
