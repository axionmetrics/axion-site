#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Axion Metrics — graft του πεδίου `current` (μπάρα «Τρέχον») μετά το build_site_data.py.

Το τοπικό bridge ΔΕΝ παράγει το `current` (mcap/pe/pbv/date κλεισίματος)· αυτό το
γράφει ΜΟΝΟ το ημερήσιο GitHub Action (daily_prices.py) στο data.js του origin.
Αν ανεβάσεις σκέτο bridge-output, ΣΒΗΝΕΙ το current μέχρι το επόμενο daily run.

Αυτό το script το εμβολιάζει πίσω: διαβάζει το `current` από το `origin/<branch>:assets/data.js`
και το περνά στο τοπικό assets/data.js, ανά εταιρεία (κλειδί = ticker `tk`, ανά βάση).
Τρέξ' το ΑΜΕΣΩΣ ΜΕΤΑ το bridge και ΠΡΙΝ το commit/push. Best-effort: αν δεν υπάρχει
git/origin, δεν πειράζει τίποτα (το daily action θα το ξαναγράψει ούτως ή άλλως).

Χρήση:  python .github/scripts/graft_current.py   [--data assets/data.js]
"""
import json, re, subprocess, sys, argparse

def load(txt):
    m=re.search(r'window\.AXION\s*=\s*(\{.*\})\s*;', txt, re.S)
    if not m: raise SystemExit("δεν βρέθηκε window.AXION")
    return json.loads(m.group(1)), txt[:m.start()]

def cur_index(ax):
    """{base: {tk: current}} μόνο για μη-κενά current."""
    out={}
    for b in ax.get('meta',{}).get('bases',[]):
        d={}
        for c in ax.get('companies',{}).get(b,[]) or []:
            cc=c.get('current')
            if cc and cc.get('mcap') is not None:
                d[c.get('tk')]=cc
        out[b]=d
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--data', default='assets/data.js')
    ap.add_argument('--remote', default='origin')
    args=ap.parse_args()

    # ποιο branch; ρώτα το git (default: αυτό που δείχνει το origin/HEAD, αλλιώς main)
    branch='main'
    try:
        r=subprocess.run(['git','rev-parse','--abbrev-ref','HEAD'],capture_output=True,text=True)
        if r.returncode==0 and r.stdout.strip() and r.stdout.strip()!='HEAD':
            branch=r.stdout.strip()
    except Exception: pass

    try:
        subprocess.run(['git','fetch',args.remote,'--quiet'],check=False)
        ref=f'{args.remote}/{branch}:assets/data.js'
        r=subprocess.run(['git','show',ref],capture_output=True,text=True)
        if r.returncode!=0 or not r.stdout.strip():
            print(f"graft: δεν βρέθηκε {ref} — παράλειψη (θα το γράψει το daily action)."); return
        OLD,_=load(r.stdout)
    except Exception as ex:
        print(f"graft: git μη διαθέσιμο ({ex}) — παράλειψη."); return

    idx=cur_index(OLD)
    local=open(args.data,encoding='utf-8').read()
    A,head=load(local)
    n=0; dates={}
    for b in A.get('meta',{}).get('bases',[]):
        for c in A.get('companies',{}).get(b,[]) or []:
            cc=idx.get(b,{}).get(c.get('tk'))
            if cc:
                c['current']=cc; n+=1
                dates[cc.get('date')]=dates.get(cc.get('date'),0)+1
    if n==0:
        print("graft: το origin δεν είχε current — τίποτα δεν άλλαξε (θα το γράψει το daily action)."); return
    body='window.AXION = '+json.dumps(A,ensure_ascii=False,separators=(',',':'))+';\n'
    open(args.data,'w',encoding='utf-8').write(head+body)
    print(f"graft: μεταφέρθηκε το current σε {n} εταιρείες από {args.remote}/{branch} (ημ/νίες: {dates}).")

if __name__=='__main__':
    main()
