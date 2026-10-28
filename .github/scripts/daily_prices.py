#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Axion Metrics — ημερήσια ενημέρωση EOD τιμών στο assets/current.js.

Τραβάει το δημόσιο αρχείο του Euronext Athens (stocks_details), παίρνει την
κεφαλαιοποίηση κλεισίματος ανά μετοχή, και γράφει το πεδίο `current`
{mcap, pe, pbv, date} ανά μετοχή — για τη μπάρα «Τρέχον» της σελίδας εταιρείας.

⚠ ΑΠΟΣΥΝΔΕΣΗ (2026-08): το `current` ΔΕΝ γράφεται πλέον μέσα στο data.js. Γράφεται
σε ΞΕΧΩΡΙΣΤΟ αρχείο `assets/current.js` (window.AXION_CURRENT = {tk: {...}}). Έτσι:
 - το βραδινό job αγγίζει ΜΟΝΟ το current.js (ποτέ το data.js),
 - οι δικές μας ενημερώσεις οικονομικών (γέφυρα → data.js) ΔΕΝ σβήνουν τη μπάρα «Τρέχον».
Το data.js διαβάζεται ΜΟΝΟ ως είσοδος (καθαρά κέρδη/ίδια κεφάλαια για P/E, P/BV) — δεν τροποποιείται.

Σχεδιασμός:
 - Το mcap λαμβάνεται ΟΛΟΚΛΗΡΟ από το Euronext (σωστός αριθμός μετοχών × τιμή).
 - P/E  = mcap ÷ καθαρά κέρδη (τελευταία ετήσια)          — ανεξάρτητο μετοχών
 - P/BV = mcap ÷ ίδια κεφάλαια, όπου ίδια κεφάλαια = ετήσιο mcap ÷ ετήσιο P/BV
   (το βιβλιακό μέγεθος — ο αριθμός μετοχών απαλείφεται στη διαίρεση).
 - Αντιστοίχιση Euronext↔δικά μας με το ελληνικό σύμβολο (Symbol == tk).
 - Ενεργές μόνο (Trading Status = 1)· αλλιώς η μετοχή ΛΕΙΠΕΙ από το current.js (η μπάρα κρύβεται).

Τρέχει από GitHub Action (root του repo). Αν αποτύχει το fetch, ΔΕΝ γράφει τίποτα.
"""
import json, re, sys, os, io, datetime, urllib.request, statistics, subprocess, tempfile, collections

URL     = "https://athens.euronext.com/sites/default/files/json_data_files/stocks_details_el.json"
# ── §148 — ΗΜΕΡΗΣΙΟΣ ΤΖΙΡΟΣ ΑΠΟ ΤΟ ΗΔΤ ───────────────────────────────────────
# ΓΙΑΤΙ: το ATVR της MSCI (κατώφλι ένταξης στους δείκτες) θέλει ημερήσια ΑΞΙΑ
# ΣΥΝΑΛΛΑΓΩΝ. ΚΑΝΕΝΑ από τα 8 json του Euronext Athens δεν τη δίνει — ελέγχθηκαν
# όλα (stocks_details_el/en, stocks_el/en, indices_details_el, indices_el,
# etfs_details_el, bonds_details_el). Το Ημερήσιο Δελτίο Τιμών (PDF) τη δίνει.
# ΑΝΤΙΣΤΟΙΧΙΣΗ: ΟΧΙ με όνομα (το ΗΔΤ γράφει «ΠΡΟΝΤΕΑ (ΚΟ)») αλλά με το ΠΛΗΘΟΣ
# ΜΕΤΟΧΩΝ, που είναι το 1ο πεδίο κάθε γραμμής και υπάρχει και στο json. Δοκιμή
# 27/10/2026: 119 από 119 γραμμές με όγκο ταίριαξαν μονοσήμαντα, 0 αταίριαστες.
# ΠΡΟΣΟΧΗ: πρέπει να ευρετηριάζονται ΚΑΙ τα δύο πεδία πλήθους του json — η 19
# CREDIA BANK έχει Listed 1.995.632.829 αλλά Total 2.207.890.029, και το ΗΔΤ
# χρησιμοποιεί το Total.
HDT_ON   = True
HDT_IDX  = "https://athens.euronext.com/el/market-data/data-services/statistics/reports-daily"
LIQ_DIR  = ".github/liquidity"   # ένα json ανά ΜΗΝΑ: {ΣΥΜΒΟΛΟ: {YYYY-MM-DD: [όγκος, τζίρος]}}
DATA    = "assets/data.js"        # ΕΙΣΟΔΟΣ μόνο (οικονομικά για P/E, P/BV) — ΔΕΝ γράφεται
CURRENT = "assets/current.js"     # ΕΞΟΔΟΣ: window.AXION_CURRENT
SNAP_DIR = "snapshots"            # μόνιμο αρχείο στιγμιότυπων τιμών/μετοχών ανά περίοδο
UA   = "Mozilla/5.0 (compatible; AxionMetricsBot/1.0)"
CLOSE_HOUR_ATH = 18   # ώρα Αθήνας μετά την οποία η σημερινή συνεδρίαση θεωρείται κλεισμένη/εκκαθαρισμένη

def session_date(eu_raw):
    """Ημερομηνία της τελευταίας ΟΛΟΚΛΗΡΩΜΕΝΗΣ συνεδρίασης του ΧΑΑ — αυτή στην οποία
    ανήκει το `Last Trading Close` του feed. Βασίζεται στο πότε *παρήχθη* το feed
    (`lastUpdated`), όχι στην ώρα εκτέλεσης του script· έτσι μια χειροκίνητη/πρόωρη
    εκτέλεση μέσα στη συνεδρίαση δεν σφραγίζει λάθος (μελλοντική) ημερομηνία."""
    try:
        from zoneinfo import ZoneInfo
        tz=ZoneInfo('Europe/Athens')
    except Exception:
        tz=None
    ts=eu_raw.get('lastUpdated') if isinstance(eu_raw,dict) else None
    try: ts=int(ts)
    except (TypeError,ValueError): ts=None
    if ts is not None:
        if tz is not None:
            now=datetime.datetime.fromtimestamp(ts, tz)
        else:  # χωρίς tz βάση: προσέγγιση Αθήνας = UTC + (3 θέρος / 2 χειμώνας)
            u=datetime.datetime.utcfromtimestamp(ts); now=u+datetime.timedelta(hours=3 if 4<=u.month<=10 else 2)
    else:      # τελευταία άμυνα: ώρα εκτέλεσης σε ώρα Αθήνας
        if tz is not None: now=datetime.datetime.now(tz)
        else:
            u=datetime.datetime.utcnow(); now=u+datetime.timedelta(hours=3 if 4<=u.month<=10 else 2)
    d=now.date()
    if now.hour < CLOSE_HOUR_ATH:          # η σημερινή συνεδρίαση δεν έχει ολοκληρωθεί → προηγούμενη
        d-=datetime.timedelta(days=1)
    while d.weekday()>=5:                   # γύρνα πίσω σε εργάσιμη (Σάββ/Κυρ)
        d-=datetime.timedelta(days=1)
    return d.strftime('%Y-%m-%d')

def report_feed_time(eu_raw, sdate):
    """Γράφει στο log και στο summary του Action το `lastUpdated` του feed (ώρα Αθήνας),
    την ώρα εκτέλεσης και την ημερομηνία συνεδρίασης που προέκυψε — για να ελέγχεται
    καθημερινά αν το όριο CLOSE_HOUR_ATH σφραγίζει σωστή ημερομηνία."""
    try:
        from zoneinfo import ZoneInfo
        tz=ZoneInfo('Europe/Athens')
        ts=eu_raw.get('lastUpdated') if isinstance(eu_raw,dict) else None
        lu=datetime.datetime.fromtimestamp(int(ts),tz).strftime('%a %d/%m/%Y %H:%M:%S') if ts else '—'
        now=datetime.datetime.now(tz).strftime('%a %d/%m/%Y %H:%M:%S')
    except Exception as ex:
        lu, now = 'σφάλμα (%s)' % ex, '—'
    print(f"feed: lastUpdated={lu} (Αθήνα) · εκτέλεση={now} · συνεδρίαση={sdate}")
    path=os.environ.get('GITHUB_STEP_SUMMARY')
    if path:
        try:
            with open(path,'a',encoding='utf-8') as f:
                f.write("\n| feed | |\n|---|---|\n")
                f.write(f"| `lastUpdated` (Αθήνα) | {lu} |\n")
                f.write(f"| ώρα εκτέλεσης (Αθήνα) | {now} |\n")
                f.write(f"| ημερομηνία συνεδρίασης που γράφεται | **{sdate}** |\n")
                f.write(f"| όριο `CLOSE_HOUR_ATH` | {CLOSE_HOUR_ATH}:00 |\n")
        except Exception:
            pass

def to_num(v):
    """Ανθεκτικό parse αριθμού: δέχεται number ή string με ελληνικούς/αγγλικούς διαχωριστές."""
    if v is None: return None
    if isinstance(v,(int,float)): return float(v)
    s=str(v).strip()
    if not s or s in ('-','—','N/A','n/a'): return None
    s=s.replace('\xa0','').replace(' ','').replace('€','')
    # κράτα μόνο ψηφία και , . -
    s=re.sub(r'[^0-9,.\-]','',s)
    if not s: return None
    if ',' in s and '.' in s:
        # ο τελευταίος διαχωριστής είναι το δεκαδικό
        if s.rfind(',')>s.rfind('.'):      # ευρωπαϊκό: . χιλιάδες, , δεκαδικό
            s=s.replace('.','').replace(',','.')
        else:                               # αγγλικό: , χιλιάδες, . δεκαδικό
            s=s.replace(',','')
    elif ',' in s:
        # μόνο κόμματα: δεκαδικό αν 1-2 ψηφία στο τέλος & ένα κόμμα, αλλιώς χιλιάδες
        s=s.replace(',','.') if (s.count(',')==1 and re.search(r',\d{1,2}$',s)) else s.replace(',','')
    elif '.' in s:
        # μόνο τελείες: δεκαδικό αν μία τελεία & 1-2 ψηφία στο τέλος, αλλιώς χιλιάδες (π.χ. 8.288.635.661)
        if not (s.count('.')==1 and re.search(r'\.\d{1,2}$',s)):
            s=s.replace('.','')
    try: return float(s)
    except ValueError: return None

def build_eu_map(arr):
    m={}
    for x in arr:
        sym=str(x.get('Symbol') or '').strip()
        if not sym: continue
        st=str(x.get('Trading Status') or '').split('|')[0].strip()
        m[sym]={'mcap':to_num(x.get('Market Capitalisation')),
                'close':to_num(x.get('Last Trading Close')),
                'shares':to_num(x.get('Total Number Of Securities')),
                'st':st,'isin':str(x.get('ISIN') or '').strip()}
    return m

def latest(series):
    if not series: return None
    for v in reversed(series):
        if isinstance(v,(int,float)): return v
    return None

def _period_label(dstr):
    """'YYYY-MM-DD' -> 'YYYYH1' (Ιαν–Ιουν) ή 'YYYYH2' (Ιουλ–Δεκ). Το H2 τελειώνει 31/12 = ετήσιο κλείσιμο."""
    y,m,_=(int(t) for t in dstr.split('-'))
    return f"{y}H{1 if m<=6 else 2}"

def write_snapshots(eu, today):
    """Κρατάει «κυλιόμενο» στιγμιότυπο (τιμή/μετοχές/κεφ-ση/ISIN ανά Symbol) της τρέχουσας
    περιόδου· όταν αλλάξει η περίοδος, ΠΑΓΩΝΕΙ το προηγούμενο σε μόνιμο αρχείο. Έτσι το
    snapshots/<YYYYH1>.json = δεδομένα 30/6 και snapshots/<YYYYH2>.json = 31/12 (ετήσιο),
    χωρίς να χρειάζεται να ξέρουμε εκ των προτέρων ποια είναι η τελευταία συνεδρίαση."""
    try:
        os.makedirs(SNAP_DIR, exist_ok=True)
        cur=_period_label(today)
        data={sym:{'close':v.get('close'),'shares':v.get('shares'),
                   'mcap':v.get('mcap'),'isin':v.get('isin')}
              for sym,v in eu.items()
              if (v.get('close') is not None or v.get('mcap') is not None)}
        roll=os.path.join(SNAP_DIR,'_rolling.json')
        if os.path.exists(roll):
            try: prev=json.load(open(roll,encoding='utf-8'))
            except Exception: prev=None
            if prev and prev.get('period') and prev['period']!=cur:
                frozen=os.path.join(SNAP_DIR,prev['period']+'.json')
                if not os.path.exists(frozen):
                    json.dump(prev,open(frozen,'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
                    print(f"snapshot: πάγωσε {prev['period']} ({prev.get('date')}, {len(prev.get('data',{}))} μετοχές) -> {frozen}")
        json.dump({'period':cur,'date':today,'data':data},
                  open(roll,'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
        print(f"snapshot: rolling {cur} ({today}, {len(data)} μετοχές)")
    except Exception as ex:
        print(f"snapshot: ΠΡΟΕΙΔΟΠΟΙΗΣΗ — δεν γράφτηκε ({ex})")

def _at(series, i):
    """Τιμή στη θέση i (ή None) — ανθεκτικό σε λάθος index/τύπο."""
    try:
        v=series[i]
        return v if isinstance(v,(int,float)) else None
    except (TypeError, IndexError, KeyError):
        return None

def build_current(ax, eu, today):
    """Χτίζει {tk: {mcap, pe, pbv, date [, pe_i, pbv_i]}} για τις ΕΝΕΡΓΕΣ μετοχές. Τα ετήσια
    οικονομικά (καθαρά κέρδη/ίδια κεφάλαια) έρχονται από τη βάση `annual` του data.js.

    Interim variants (pe_i, pbv_i) — για τη ΣΕΛΙΔΑ όταν προβάλλεται η όψη 6μήνου, ΜΟΝΟ όταν
    το τελευταίο 6μηνο είναι ΠΙΟ πρόσφατο από το τελευταίο ετήσιο (Yi>Ya, δηλ. δημοσιεύτηκε
    H1 του επόμενου έτους) — αλλιώς τα ετήσια είναι πιο πρόσφατα και η σελίδα κάνει fallback:
      • pe_i  = mcap ÷ TTM,  TTM (κυλιόμενο 12μηνο) = FY(Yi-1) + H1(Yi) − H1(Yi-1)
      • pbv_i = mcap ÷ ίδια κεφάλαια 6μήνου, όπου ίδια κεφάλαια = interim_mcap ÷ interim_pbv (30/6).
    Ανενεργές/μη-αντιστοιχισμένες → ΛΕΙΠΟΥΝ από τον χάρτη (η μπάρα «Τρέχον» κρύβεται)."""
    out={}; ratios=[]
    interim_by_tk={c.get('tk'):c for c in (ax.get('companies',{}).get('interim',[]) or [])}
    for c in ax.get('companies',{}).get('annual',[]) or []:
        tk=c.get('tk'); e=eu.get(tk)
        mcap=e['mcap'] if e else None
        if not e or not mcap or e['st']!='1':
            continue
        np_=latest(c.get('metrics',{}).get('net_profit'))
        amc=latest(c.get('metrics',{}).get('mcap'))
        apbv=latest((c.get('ratios',{}).get('pbv') or {}).get('series'))
        abvps=latest((c.get('ratios',{}).get('bvps') or {}).get('series'))
        eq=(amc/apbv) if (amc and apbv and apbv>0) else None
        neg_eq=(abvps is not None and abvps<0)
        pe =round(mcap/np_,4) if (np_ and not neg_eq) else None
        pbv=round(mcap/eq,4)  if (eq  and eq>0)  else None
        rec={'mcap':mcap,'pe':pe,'pbv':pbv,'date':today}
        # --- interim variants (μόνο όταν το 6μηνο είναι πιο πρόσφατο από το ετήσιο) ---
        im=interim_by_tk.get(tk)
        if im:
            li_a=(c.get('latest',{}) or {}).get('idx'); years_a=c.get('years',[]) or []
            Ya=_at(years_a, li_a) if li_a is not None else None
            li_i=(im.get('latest',{}) or {}).get('idx'); years_i=im.get('years',[]) or []
            Yi=_at(years_i, li_i) if li_i is not None else None
            if Ya is not None and Yi is not None and Yi>Ya:
                inp=im.get('metrics',{}).get('net_profit',[]) or []
                h1c=_at(inp, li_i)
                pidx=years_i.index(Yi-1) if (Yi-1) in years_i else -1
                h1p=_at(inp, pidx) if pidx>=0 else None
                aidx=years_a.index(Yi-1) if (Yi-1) in years_a else -1
                fy=_at(c.get('metrics',{}).get('net_profit',[]) or [], aidx) if aidx>=0 else None
                if (h1c not in (None,0)) and (h1p not in (None,0)) and fy is not None:
                    ttm=fy+h1c-h1p
                    if ttm!=0: rec['pe_i']=round(mcap/ttm,4)
                imc=_at(im.get('metrics',{}).get('mcap',[]) or [], li_i)
                ipbv=_at((im.get('ratios',{}).get('pbv') or {}).get('series',[]) or [], li_i)
                ibvps=_at((im.get('ratios',{}).get('bvps') or {}).get('series',[]) or [], li_i)
                eqi=(imc/ipbv) if (imc and ipbv and ipbv>0) else None
                negi=(ibvps is not None and ibvps<0)
                if eqi and eqi>0 and not negi: rec['pbv_i']=round(mcap/eqi,4)
        out[tk]=rec
        if amc and amc>0: ratios.append(mcap/amc)
    return out, ratios

def load_axion(path):
    txt=open(path,encoding='utf-8').read()
    mm=re.search(r'window\.AXION\s*=\s*(\{.*\})\s*;', txt, re.S)
    if not mm: raise SystemExit("δεν βρέθηκε window.AXION στο "+path)
    return json.loads(mm.group(1))

def save_current(path, curmap):
    head=("/* Axion Metrics — τρέχουσες EOD τιμές (μπάρα «Τρέχον»). Παράγεται ΑΥΤΟΜΑΤΑ από το\n"
          "   .github/scripts/daily_prices.py κάθε βράδυ. ΜΗΝ το επεξεργάζεσαι με το χέρι και ΜΗΝ το\n"
          "   ξαναγράφει η γέφυρα — είναι ανεξάρτητο από το data.js. */\n")
    body='window.AXION_CURRENT = '+json.dumps(curmap,ensure_ascii=False,separators=(',',':'))+';\n'
    open(path,'w',encoding='utf-8').write(head+body)

# ---------------------------------------------------------------- ΗΔΤ / τζίρος
_HDT_ROW = re.compile(r'^\s*([\d,]{5,})\s+[\d.]+\s')   # ξεκινά: πλήθος μετοχών, ονομ. αξία
# Η ουρά: όγκος | συναλλαγές | ΤΖΙΡΟΣ | κεφαλαιοποίηση χιλ.€ | χαμηλό 52εβδ | υψηλό 52εβδ | ICB
# ⚠ ΣΤΙΣ ΜΕΓΑΛΕΣ ΕΤΑΙΡΕΙΕΣ ΤΖΙΡΟΣ ΚΑΙ ΚΕΦΑΛΑΙΟΠΟΙΗΣΗ ΓΡΑΦΟΝΤΑΙ ΚΟΛΛΗΤΑ, χωρίς κενό:
#   «44,542,037.1615,808,055.75» = τζίρος 44.542.037,16 + κεφαλ. 15.808.055,75 (EUROBANK).
# Γι' αυτό ΑΠΑΓΟΡΕΥΕΤΑΙ ο δεικτοδότης από το τέλος (f[-7], f[-5]) — έριχνε ΣΙΩΠΗΛΑ
# ακριβώς τις πιο εμπορεύσιμες μετοχές (Τράπεζες, ΔΕΗ). Το `\\.\\d{2}` κόβει σωστά το ζεύγος.
_HDT_TAIL = re.compile(
    r'\s(?P<vol>\d[\d,]*)\s+(?P<tr>\d[\d,]*)\s+'
    r'(?P<turn>\d[\d,]*\.\d{2})\s*(?P<mcap>\d[\d,]*\.\d{2})\s+'
    r'(?:[\d.]+|-{2,})\s+(?:[\d.]+|-{2,})\s+(?P<icb>\d{8})\s*$')
# Το ΠΡΩΤΟ αριθμητικό πεδίο μετά την επωνυμία = ΤΙΜΗ ΚΛΕΙΣΙΜΑΤΟΣ. Χρειάζεται γιατί το
# MSCI ορίζει daily traded value = όγκος × ΚΛΕΙΣΙΜΟ (ο τζίρος του ΗΔΤ βγαίνει με τη
# ΜΕΣΗ τιμή συνεδρίασης — διαφορά ~0,5%%). Κρατάμε και τα δύο.
_HDT_NM  = re.compile(r'\d{2}/\d{2}/\d{4}\s+\d{2}/\d{2}/\d{4}\s+\S+\s+(?:.+?)\s{2,}([\d.]+)\s')
_HDT_NM2 = re.compile(r'\d{2}/\d{2}/\d{4}\s+\S+\s+(?:.+?)\s{2,}([\d.]+)\s')
_HDT_END = re.compile(r'\s(\d{8})\s*$')                  # τελειώνει: κωδικός ICB

def _hdt_latest_url():
    """Το νεότερο PDF από τη σελίδα ευρετηρίου. ΠΟΤΕ κατασκευασμένο URL: το όνομα
    έχει αύξοντα αριθμό συνεδρίασης + ελληνική ημερομηνία («ΗΔΤ-2026-204 (27 Οκτ).pdf»),
    που σπάει σε κάθε αργία."""
    req=urllib.request.Request(HDT_IDX, headers={'User-Agent':UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        html=r.read().decode('utf-8','replace')
    links=re.findall(r'href="([^"]*/sites/default/files/[^"]*\.pdf)"', html)
    hdt=[u for u in links if '%CE%97%CE%94%CE%A4' in u or 'ΗΔΤ' in u]
    if not hdt: return None
    # ΟΧΙ η σειρά του εγγράφου — η σελίδα τα δίνει παλαιότερο-πρώτο. Παίρνουμε τον
    # ΜΕΓΑΛΥΤΕΡΟ αύξοντα αριθμό συνεδρίασης από το όνομα: «…-2026-204 (27 Οκτ).pdf».
    def seq(u):
        m=re.search(r'-(\d{4})-(\d{1,3})', u)
        return (int(m.group(1)), int(m.group(2))) if m else (0,0)
    u=max(hdt, key=seq)
    return u if u.startswith('http') else 'https://athens.euronext.com'+u

def fetch_turnover(arr):
    """{ΣΥΜΒΟΛΟ: (όγκος, τζίρος €, κεφαλ. εταιρείας €, κλείσιμο €, μετοχές)} από το ΗΔΤ. ΔΕΝ πετάει ΠΟΤΕ: οι τιμές είναι η
    κύρια αποστολή αυτού του script και δεν πρέπει να χαθούν για έναν τζίρο."""
    if not HDT_ON: return {}, None
    try:
        url=_hdt_latest_url()
        if not url: print('  ΗΔΤ: δεν βρέθηκε σύνδεσμος στο ευρετήριο'); return {}, None
        req=urllib.request.Request(url, headers={'User-Agent':UA})
        with urllib.request.urlopen(req, timeout=120) as r: pdf=r.read()
        with tempfile.TemporaryDirectory() as td:
            f=os.path.join(td,'h.pdf')
            open(f,'wb').write(pdf)
            txt=subprocess.run(['pdftotext','-layout',f,'-'],capture_output=True,timeout=180).stdout.decode('utf-8','replace')
    except Exception as e:
        print('  ΗΔΤ: δεν διαβάζεται —', e); return {}, None
    # πλήθος μετοχών → σύμβολο, και από τα ΔΥΟ πεδία του json
    bysh=collections.defaultdict(set)
    for x in arr:
        for k in ('Number Of Securities Listed','Total Number Of Securities'):
            try: bysh[int(str(x.get(k)).replace(',','').strip())].add(str(x.get('Symbol') or '').strip())
            except Exception: pass
    out={}; seen=0; unmatched=[]
    for L in txt.split('\n'):
        m=_HDT_ROW.match(L)
        if not m or not _HDT_END.search(L): continue
        tm=_HDT_TAIL.search(L)
        if not tm: continue               # γραμμή χωρίς συναλλαγές
        vol=int(tm.group('vol').replace(',','')); turn=float(tm.group('turn').replace(',',''))
        # η κεφαλαιοποίηση στο ΗΔΤ είναι σε ΧΙΛΙΑΔΕΣ ευρώ → ×1000 για ευρώ
        mcap=float(tm.group('mcap').replace(',',''))*1000.0
        seen+=1
        sh=int(m.group(1).replace(',',''))
        nm=_HDT_NM.search(L) or _HDT_NM2.search(L)
        try: cl=float(nm.group(1)) if nm else 0.0
        except Exception: cl=0.0
        # εφεδρεία: αν δεν διαβάστηκε το κλείσιμο, βγαίνει από κεφαλαιοποίηση ÷ μετοχές
        if cl<=0 and sh>0: cl=round(mcap/sh,4)
        syms={y for y in bysh.get(sh,set()) if y}
        if len(syms)==1: out[syms.pop()]=(vol,turn,mcap,cl,sh)
        else: unmatched.append(sh)
    print('  ΗΔΤ: %d γραμμές με όγκο · %d αντιστοιχίστηκαν · %d αταίριαστες'%(seen,len(out),len(unmatched)))
    return out, (url.rsplit('/',1)[-1] if url else None)

def save_turnover(turn, day):
    """Συσσωρευτικό αρχείο ΑΝΑ ΜΗΝΑ — ώστε το ετήσιο ιστορικό να μη ξαναγράφεται
    ολόκληρο σε κάθε commit."""
    if not turn: return
    os.makedirs(LIQ_DIR, exist_ok=True)
    path=os.path.join(LIQ_DIR, day[:7]+'.json')
    db=json.load(io.open(path,encoding='utf-8')) if os.path.exists(path) else {}
    for sym,(vol,tv,mc,cl,sh) in turn.items():
        # [όγκος, τζίρος €, κεφαλαιοποίηση ΕΤΑΙΡΕΙΑΣ €, κλείσιμο €, μετοχές σειράς]
        # ⚠ Στις μετοχές διπλής σειράς (ΚΟ+ΠΟ) το ΗΔΤ γράφει ΤΗΝ ΙΔΙΑ συνολική
        # κεφαλαιοποίηση σε ΚΑΙ ΤΙΣ ΔΥΟ γραμμές (π.χ. ΙΝΤΕΡΓΟΥΝΤ-ΞΥΛΕΜΠΟΡΙΑ).
        # Για το ATVR χρειάζεται η κεφαλαιοποίηση ΤΗΣ ΣΕΙΡΑΣ = μετοχές × κλείσιμο.
        db.setdefault(sym,{})[day]=[vol, round(tv,2), round(mc,2), cl, sh]
    io.open(path,'w',encoding='utf-8').write(json.dumps(db,ensure_ascii=False,sort_keys=True,separators=(',',':')))
    print('  ΗΔΤ: γράφτηκε %s (%d σύμβολα αυτόν τον μήνα)'%(path,len(db)))

def main():
    req=urllib.request.Request(URL, headers={'User-Agent':UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        eu_raw=json.load(r)
    arr=eu_raw.get('data') if isinstance(eu_raw,dict) else eu_raw
    if not arr: raise SystemExit("κενό feed Euronext")
    eu=build_eu_map(arr)
    ax=load_axion(DATA)          # ΜΟΝΟ ανάγνωση (οικονομικά για P/E, P/BV)
    today=session_date(eu_raw)   # ημερομηνία τελευταίας κλεισμένης συνεδρίασης (όχι ώρα εκτέλεσης)
    report_feed_time(eu_raw, today)
    write_snapshots(eu, today)   # αρχείο στιγμιότυπων περιόδου (τέλος 6μήνου/έτους)
    curmap, ratios=build_current(ax, eu, today)
    # sanity: το euronext mcap πρέπει να είναι στην ίδια τάξη μεγέθους με το δικό μας
    if ratios:
        med=statistics.median(ratios)
        print(f"sanity: διάμεσος(euronext_mcap/ετήσιο_mcap)={med:.3f} (αναμένεται ~κοντά στο 1)")
        if med<0.02 or med>50:
            raise SystemExit(f"ΑΚΥΡΟ: πιθανή αναντιστοιχία μονάδων mcap (ratio={med}). Δεν γράφτηκε τίποτα.")
    if not curmap: raise SystemExit("καμία αντιστοίχιση — δεν γράφτηκε τίποτα")
    save_current(CURRENT, curmap)
    # §148 — ο τζίρος ΜΕΤΑ το current.js: αν σκάσει, οι τιμές έχουν ήδη γραφτεί
    try:
        turn,fname=fetch_turnover(arr)
        if turn: save_turnover(turn, today)
    except Exception as e:
        print('  ΗΔΤ: παραλείπεται —', e)
    print(f"ΟΚ: γράφτηκε {CURRENT} για {len(curmap)} εταιρείες ({today}).")

if __name__=='__main__':
    main()
