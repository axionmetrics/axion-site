
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Axion Metrics — ημερήσια ενημέρωση EOD τιμών στο assets/data.js."""
import json, re, sys, datetime, urllib.request, statistics

URL  = "https://athens.euronext.com/sites/default/files/json_data_files/stocks_details_el.json"
DATA = "assets/data.js"
UA   = "Mozilla/5.0 (compatible; AxionMetricsBot/1.0)"

def to_num(v):
    if v is None: return None
    if isinstance(v,(int,float)): return float(v)
    s=str(v).strip()
    if not s or s in ('-','—','N/A','n/a'): return None
    s=s.replace('\xa0','').replace(' ','').replace('€','')
    s=re.sub(r'[^0-9,.\-]','',s)
    if not s: return None
    if ',' in s and '.' in s:
        if s.rfind(',')>s.rfind('.'):
            s=s.replace('.','').replace(',','.')
        else:
            s=s.replace(',','')
    elif ',' in s:
        s=s.replace(',','.') if (s.count(',')==1 and re.search(r',\d{1,2}$',s)) else s.replace(',','')
    elif '.' in s:
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
                'st':st,'isin':str(x.get('ISIN') or '').strip()}
    return m

def latest(series):
    if not series: return None
    for v in reversed(series):
        if isinstance(v,(int,float)): return v
    return None

def apply_current(ax, eu, today):
    n=0; ratios=[]
    for base in ('annual','interim'):
        for c in ax.get('companies',{}).get(base,[]) or []:
            e=eu.get(c.get('tk'))
            mcap=e['mcap'] if e else None
            if not e or not mcap or e['st']!='1':
                c['current']=None; continue
            np_=latest(c.get('metrics',{}).get('net_profit'))
            amc=latest(c.get('metrics',{}).get('mcap'))
            apbv=latest((c.get('ratios',{}).get('pbv') or {}).get('series'))
            eq=(amc/apbv) if (amc and apbv and apbv>0) else None
            pe =round(mcap/np_,4) if (np_ and np_>0) else None
            pbv=round(mcap/eq,4)  if (eq  and eq>0)  else None
            c['current']={'mcap':mcap,'pe':pe,'pbv':pbv,'date':today}
            if amc and amc>0: ratios.append(mcap/amc)
            n+=1
    return n, ratios

def load_axion(path):
    txt=open(path,encoding='utf-8').read()
    mm=re.search(r'window\.AXION\s*=\s*(\{.*\})\s*;', txt, re.S)
    if not mm: raise SystemExit("δεν βρέθηκε window.AXION στο "+path)
    return txt[:mm.start()], json.loads(mm.group(1))

def save_axion(path, head, ax):
    body='window.AXION = '+json.dumps(ax,ensure_ascii=False,separators=(',',':'))+';\n'
    open(path,'w',encoding='utf-8').write(head+body)

def main():
    req=urllib.request.Request(URL, headers={'User-Agent':UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        eu_raw=json.load(r)
    arr=eu_raw.get('data') if isinstance(eu_raw,dict) else eu_raw
    if not arr: raise SystemExit("κενό feed Euronext")
    eu=build_eu_map(arr)
    head, ax=load_axion(DATA)
    today=datetime.datetime.utcnow().strftime('%Y-%m-%d')
    n, ratios=apply_current(ax, eu, today)
    if ratios:
        med=statistics.median(ratios)
        print(f"sanity: median(euronext_mcap/annual_mcap)={med:.3f}")
        if med<0.02 or med>50:
            raise SystemExit(f"ΑΚΥΡΟ: πιθανή αναντιστοιχία μονάδων mcap (ratio={med}).")
    if n==0: raise SystemExit("καμία αντιστοίχιση — δεν γράφτηκε τίποτα")
    save_axion(DATA, head, ax)
    print(f"OK: current updated for {n} companies ({today}).")

if __name__=='__main__':
    main()
