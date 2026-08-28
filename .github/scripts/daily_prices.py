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
import json, re, sys, os, datetime, urllib.request, statistics

URL     = "https://athens.euronext.com/sites/default/files/json_data_files/stocks_details_el.json"
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

def build_current(ax, eu, today):
    """Χτίζει {tk: {mcap, pe, pbv, date}} για τις ΕΝΕΡΓΕΣ μετοχές. Τα οικονομικά (καθαρά
    κέρδη/ίδια κεφάλαια) έρχονται από τη βάση `annual` του data.js (κοινά, ανεξάρτητα βάσης).
    Ανενεργές/μη-αντιστοιχισμένες → ΛΕΙΠΟΥΝ από τον χάρτη (η μπάρα «Τρέχον» κρύβεται)."""
    out={}; ratios=[]
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
        out[tk]={'mcap':mcap,'pe':pe,'pbv':pbv,'date':today}
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

def main():
    req=urllib.request.Request(URL, headers={'User-Agent':UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        eu_raw=json.load(r)
    arr=eu_raw.get('data') if isinstance(eu_raw,dict) else eu_raw
    if not arr: raise SystemExit("κενό feed Euronext")
    eu=build_eu_map(arr)
    ax=load_axion(DATA)          # ΜΟΝΟ ανάγνωση (οικονομικά για P/E, P/BV)
    today=session_date(eu_raw)   # ημερομηνία τελευταίας κλεισμένης συνεδρίασης (όχι ώρα εκτέλεσης)
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
    print(f"ΟΚ: γράφτηκε {CURRENT} για {len(curmap)} εταιρείες ({today}).")

if __name__=='__main__':
    main()
