/* ---------- Γρήγορη εύρεση εταιρείας ---------- */
const QS_CURRENT=(AX?AX.name:'');
const QS_PAGE='';   // προσωρινά: όλες δείχνουν στην ίδια σελίδα
const qsNorm=s=>(s||'').toUpperCase()
 .replace(/[ΆΑ]/g,'Α').replace(/[ΈΕ]/g,'Ε').replace(/[ΉΗ]/g,'Η').replace(/[ΊΪΐΙ]/g,'Ι')
 .replace(/[ΌΟ]/g,'Ο').replace(/[ΎΫΰΥ]/g,'Υ').replace(/[ΏΩ]/g,'Ω');
// Αλφαβητικά: πρώτα οι λατινικές επωνυμίες (A–Z), μετά οι ελληνικές (Α–Ω)· εμφάνιση χωρίς κλάδο.
// Ομαδοποίηση με βάση το ΚΥΡΙΑΡΧΟ αλφάβητο (αντέχει σε επωνυμίες με ανάμεικτους χαρακτήρες).
const _qsLatin=function(s){s=s||'';for(var i=0;i<s.length;i++){if(/[A-Za-z]/.test(s[i]))return true;if(/[\u0370-\u03FF\u1F00-\u1FFF]/.test(s[i]))return false;}return false;};
const _qsKey=s=>qsNorm(s).replace(/^[^A-Za-z\u0370-\u03FF\u1F00-\u1FFF]+/,'');
const QS_DATA=((window.AXION&&window.AXION.companies&&window.AXION.companies[AXBASIS])||[])
 .map(function(c){return [c.name,c.tk,(c.calculated!==false)];})   // r[2]=live? (false=frozen)
 .sort(function(a,b){
   const la=_qsLatin(a[0]), lb=_qsLatin(b[0]);
   if(la!==lb) return la?-1:1;
   return _qsKey(a[0]).localeCompare(_qsKey(b[0]),'el');
 });
let qsSel=0, qsRows=[];

// τελευταία ενημερωμένη περίοδος ανά ticker (από rowsByPeriod, ανεξάρτητα τρέχουσας βάσης)
const QS_PERIOD=(function(){
  try{
    const ax=window.AXION||{}, rbp=ax.rowsByPeriod||{}, ann=rbp.annual||{}, inter=rbp.interim||{};
    const rs=coll=>{const m={};for(const p in coll){m[p]=new Set((coll[p]||[]).filter(r=>r&&r.reported).map(r=>r.tk));}return m;};
    const A=rs(ann), I=rs(inter);
    const ay=Object.keys(A).sort((a,b)=>(+a)-(+b));
    const ipk=p=>(+p.slice(0,4))*10+(+String(p).slice(5).replace('H',''));
    const ip=Object.keys(I).sort((a,b)=>ipk(a)-ipk(b));
    let maxAY=null; for(const y of ay) if(A[y].size) maxAY=+y;
    const out={};
    ((ax.companies&&ax.companies.annual)||[]).forEach(c=>{
      const tk=c.tk; let la=null,li=null;
      for(const y of ay) if(A[y].has(tk)) la=+y;
      for(const p of ip) if(I[p].has(tk)) li=p;
      const cand=[];
      if(la) cand.push([la*100+12, String(la), false]);
      if(li) cand.push([(+li.slice(0,4))*100+6, li, true]);
      if(!cand.length){ out[tk]={label:'—',tier:'p-old'}; return; }
      cand.sort((a,b)=>a[0]-b[0]);
      const t=cand[cand.length-1];
      // §71 — «6M», όχι «H1»: η υπόλοιπη σελίδα (λωρίδα, γράφημα, πίνακες δεικτών) και οι
      // σελίδες κατατάξεων/σύγκρισης γράφουν ήδη 6M· το pill της λίστας ήταν το τελευταίο «H1».
      if(t[2]) out[tk]={label:'6M '+t[1].slice(0,4), tier:'p-fresh'};
      else out[tk]={label:t[1], tier:(+t[1]===maxAY?'p-cur':'p-old')};
    });
    return out;
  }catch(e){ return {}; }
})();

function qsRender(){
  const term=qsNorm(document.getElementById('qsInput').value.trim());
  qsRows = term ? QS_DATA.filter(r=>qsNorm(r[0]).includes(term)||qsNorm(r[1]).includes(term)) : QS_DATA;
  const body=document.getElementById('qsBody');
  if(!qsRows.length){ body.innerHTML='<div class="qs-empty">'+L('co.qs.empty')+'</div>'; return; }
  if(qsSel>=qsRows.length) qsSel=qsRows.length-1;
  let html='';
  qsRows.forEach((r,i)=>{
    const here = r[0]===QS_CURRENT ? ' here' : '';
    const sel  = i===qsSel && !here ? ' sel' : '';
    const dead = r[2]===false ? ' qs-dead' : '';
    const _p = QS_PERIOD[r[1]];
    // δεξί τοίχωμα: frozen → σήμανση κατάστασης· αλλιώς → pill τελευταίας περιόδου
    let right='';
    if(r[2]===false) right=`<span class="tbadge sm t-frozen">${L('co.entity.badge')}</span>`;
    else if(_p && _p.label!=='—') right=`<span class="qs-per ${_p.tier}">${_p.label}</span>`;
    html+=`<a class="qs-item${here}${sel}${dead}" data-i="${i}" href="${encodeURI(QS_PAGE)}?tk=${encodeURIComponent(r[1])}">
      <span class="qs-nm">${r[0]}</span><span class="qs-tk">${r[1]}</span><span class="qs-right">${right}</span></a>`;
  });
  body.innerHTML=html;
  const el=body.querySelector(`[data-i="${qsSel}"]`);
  if(el) el.scrollIntoView({block:'nearest'});
}
function qsOpen(){
  document.getElementById('qs').classList.add('on');
  document.getElementById('qsOv').classList.add('on');
  document.body.style.overflow='hidden';
  qsSel=0; document.getElementById('qsInput').value=''; qsRender();
  setTimeout(()=>document.getElementById('qsInput').focus(),80);
}
function qsClose(){
  document.getElementById('qs').classList.remove('on');
  document.getElementById('qsOv').classList.remove('on');
  document.body.style.overflow='';
  document.getElementById('qsInput').blur();   // ώστε το «/» να ξαναδουλεύει
}
document.getElementById('qsInput').addEventListener('input',()=>{qsSel=0;qsRender();});
document.addEventListener('keydown',e=>{
  const open=document.getElementById('qs').classList.contains('on');
  if(!open && e.key==='/' && !/^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName)){ e.preventDefault(); qsOpen(); return; }
  if(!open) return;
  if(e.key==='Escape'){ qsClose(); }
  else if(e.key==='ArrowDown'){ e.preventDefault(); qsSel=Math.min(qsSel+1,qsRows.length-1); qsRender(); }
  else if(e.key==='ArrowUp'){ e.preventDefault(); qsSel=Math.max(qsSel-1,0); qsRender(); }
  else if(e.key==='Enter'){ const el=document.querySelector(`.qs-item[data-i="${qsSel}"]`); if(el) el.click(); }
});
qsRender();
