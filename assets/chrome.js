/* Axion Metrics — shared chrome. Injects nav+footer, wires tabs, basis toggle (Ετήσια/Εξάμηνο),
   και GR/EN toggle. Τα κείμενα είναι δίγλωσσα· η γλώσσα έρχεται από το AX_I18N (ή localStorage). */
(function(){
 function curLang(){ try{ return window.AX_I18N?window.AX_I18N.lang:(localStorage.getItem('am-lang')||'el'); }catch(e){ return 'el'; } }
 function L(o){ var l=curLang(); return (o&&o[l]!=null)?o[l]:(o&&o.el!=null?o.el:''); }
 function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

 const NAV=[
   {g:{el:'Εταιρείες',en:'Companies'},items:[
     [{el:'Σελίδα εταιρείας',en:'Company page'},'/company/'],
     [{el:'Σύγκριση εταιρειών',en:'Compare companies'},'/compare/'],
     [{el:'Κατατάξεις / League tables',en:'Rankings / League tables'},'/rankings/'],
     [{el:'Τελευταία αποτελέσματα',en:'Latest results'},'/apotelesmata/']]},
   {g:{el:'Κλάδοι',en:'Sectors'},items:[
     [{el:'Ευρετήριο κλάδων',en:'Sector index'},'/sectors/'],
     [{el:'Σελίδα κλάδου',en:'Sector page'},'/sector/']]},
   {g:{el:'Γεγονότα',en:'Events'},items:[
     [{el:'Αναθεωρήσεις δεικτών',en:'Index reviews'},'/index-reviews/'],
     [{el:'Γεγονότα αγοράς',en:'Market events'},'/market-events/']]},
   {g:{el:'Σχετικά',en:'About'},items:[
     [{el:'Μεθοδολογία & δείκτες',en:'Methodology & ratios'},'/methodology/'],
     [{el:'Περί',en:'About the project'},'/about/'],
     [{el:'Όροι χρήσης',en:'Terms of use'},'/terms/']]}
 ];
 var NAV_ACTIVE=(typeof window.NAV_ACTIVE==='number')?window.NAV_ACTIVE:0;
 var NAV_CUR=window.NAV_CUR||(NAV[NAV_ACTIVE]&&NAV[NAV_ACTIVE].items[0][0].el);

 var FT={
   tag:{el:'Θεμελιώδης ανάλυση για εισηγμένες του Χρηματιστηρίου Αθηνών — δείκτες, σύγκριση κλάδου, ποιότητα & δυναμική.',
        en:'Fundamental analysis for companies listed on the Athens Stock Exchange — ratios, sector comparison, quality & momentum.'},
   bot:{el:'Δεν αποτελεί επενδυτική συμβουλή',en:'Not investment advice'}
 };
 var BASIS={ annual:{el:'Ετήσια',en:'Annual'}, interim:{el:'Εξάμηνο',en:'Interim'},
   soon:{el:'σύντομα',en:'soon'}, soonT:{el:'Σύντομα διαθέσιμο',en:'Coming soon'},
   aria:{el:'Βάση δεδομένων',en:'Data basis'},
   annualOnly:{el:'Ετήσια στοιχεία',en:'Annual figures'} };

 /* §118 — επιλογή γλώσσας με σημαίες: και οι δύο πάντα ορατές, η τρέχουσα ανενεργή */
 var LANGHTML="<div class=\"langflags\" role=\"group\" aria-label=\"Language\"><button type=\"button\" data-langset=\"el\" title=\"Ελληνικά\" aria-label=\"Ελληνικά\"><svg viewBox=\"0 0 27 18\" aria-hidden=\"true\"><rect width=\"27\" height=\"18\" fill=\"#fff\"/><g fill=\"#0D5EAF\"><rect width=\"27\" height=\"2\"/><rect width=\"27\" height=\"2\" y=\"4\"/><rect width=\"27\" height=\"2\" y=\"8\"/><rect width=\"27\" height=\"2\" y=\"12\"/><rect width=\"27\" height=\"2\" y=\"16\"/></g><rect width=\"10\" height=\"10\" fill=\"#0D5EAF\"/><path d=\"M0 4h10v2H0z M4 0h2v10H4z\" fill=\"#fff\"/><rect width=\"27\" height=\"18\" fill=\"none\" stroke=\"rgba(0,0,0,.18)\"/></svg></button><button type=\"button\" data-langset=\"en\" title=\"English\" aria-label=\"English\"><svg viewBox=\"0 0 60 30\" aria-hidden=\"true\"><clipPath id=\"axukj\"><path d=\"M30,15 h30 v15 z v15 h-30 z h-30 v-15 z v-15 h30 z\"/></clipPath><rect width=\"60\" height=\"30\" fill=\"#012169\"/><path d=\"M0,0 L60,30 M60,0 L0,30\" stroke=\"#fff\" stroke-width=\"6\"/><path d=\"M0,0 L60,30 M60,0 L0,30\" clip-path=\"url(#axukj)\" stroke=\"#C8102E\" stroke-width=\"4\"/><path d=\"M30,0 v30 M0,15 h60\" stroke=\"#fff\" stroke-width=\"10\"/><path d=\"M30,0 v30 M0,15 h60\" stroke=\"#C8102E\" stroke-width=\"6\"/><rect width=\"60\" height=\"30\" fill=\"none\" stroke=\"rgba(0,0,0,.18)\" stroke-width=\"2\"/></svg></button></div>";
 var NAVHTML="<nav class=\"site-nav\">\n <div class=\"bar1\"><a class=\"lock\" href=\"/\"><span class=\"am\">A<i>M</i></span><span class=\"lrule\"></span><span class=\"lname\">AXION<br>METRICS</span></a><ul class=\"tabs\" id=\"navtabs\"></ul><div class=\"am-right\"><div class=\"am-basis\" id=\"ambasis\"></div>"+LANGHTML+"</div></div>\n <div class=\"bar2\" id=\"navbar2\"></div>\n <div class=\"am-upd\" id=\"amupd\" hidden></div>\n <div class=\"am-ev\" id=\"amev\" hidden></div>\n</nav>";

 function footerHTML(){
   /* Οι στήλες παράγονται ΑΠΟ ΤΟΝ ΙΔΙΟ πίνακα NAV με το header — καμία χειροκίνητη λίστα,
      άρα header και footer δεν μπορούν να ξεσυγχρονιστούν. */
   var cols='';
   for(var i=0;i<NAV.length;i++){
     var g=NAV[i], links='';
     for(var j=0;j<g.items.length;j++){ links+='<a href="'+g.items[j][1]+'">'+esc(L(g.items[j][0]))+'</a>'; }
     cols+='<div class="fcol"><h4>'+esc(L(g.g))+'</h4>'+links+'</div>';
   }
   return "<footer class=\"site-ft\"><div class=\"in\">"
     +"<div class=\"fbrand\"><div class=\"flogo\">AXION<i>METRICS</i></div><div class=\"ftag\">"+esc(L(FT.tag))+"</div></div>"
     +cols
     +"</div><div class=\"fbot\">© 2026 Axion Metrics · "+esc(L(FT.bot))+" · <a href=\"mailto:info@axionmetrics.gr\" style=\"color:inherit\">info@axionmetrics.gr</a></div></footer>";
 }

 function injectStyle(){
   if(document.getElementById('am-langtog-css')) return;
   var st=document.createElement('style'); st.id='am-langtog-css';
   st.textContent=".am-right{display:flex;align-items:center;gap:10px}"+".langflags{display:inline-flex;align-items:center;gap:6px}"+".langflags button{all:unset;display:block;line-height:0;cursor:pointer;border-radius:3px;padding:2px;transition:opacity .15s,transform .15s}"+".langflags svg{display:block;width:22px;height:15px;border-radius:2.5px}"+".langflags button[aria-current]{opacity:.35;cursor:default}"+".langflags button:not([aria-current]):hover{transform:translateY(-1px)}"+".langflags button:focus-visible{outline:2px solid #57a5df;outline-offset:2px}";
   document.head.appendChild(st);
 }

 function mount(){
   var nm=document.getElementById('am-nav');
   if(nm){nm.outerHTML=NAVHTML;} else if(!document.querySelector('.site-nav')){document.body.insertAdjacentHTML('afterbegin',NAVHTML);}
   var fm=document.getElementById('am-foot');
   if(fm){fm.outerHTML=footerHTML();} else if(!document.querySelector('.site-ft')){document.body.insertAdjacentHTML('beforeend',footerHTML());}
   syncLangFlags();
 }
 function align(){
   var tabs=document.getElementById('navtabs'), bar2=document.getElementById('navbar2');
   if(!tabs||!bar2) return;
   if(innerWidth<=820){bar2.style.paddingLeft='';return;}
   var at=tabs.querySelector('li.on'), fa=bar2.querySelector('a'); if(!at||!fa)return;
   var ts=getComputedStyle(at), fs=getComputedStyle(fa);
   var off=(at.getBoundingClientRect().left+parseFloat(ts.paddingLeft))-(bar2.getBoundingClientRect().left+parseFloat(fs.paddingLeft));
   bar2.style.paddingLeft=Math.max(0,off)+'px';
 }
 function buildNav(){
   var tabs=document.getElementById('navtabs'), bar2=document.getElementById('navbar2');
   if(!tabs||!bar2) return;
   tabs.innerHTML=NAV.map(function(s,i){return '<li data-i="'+i+'" class="'+(i===NAV_ACTIVE?'on':'')+'">'+esc(L(s.g))+'</li>';}).join('');
   bar2.innerHTML=NAV[NAV_ACTIVE].items.map(function(it){return '<a href="'+it[1]+'" class="'+(it[0].el===NAV_CUR?'cur':'')+'">'+esc(L(it[0]))+'</a>';}).join('');
   if(!buildNav._wired){
     tabs.addEventListener('click',function(e){var li=e.target.closest('li');if(li){var g=NAV[+li.dataset.i];if(g&&g.items[0])location.href=g.items[0][1];}});
     addEventListener('resize',align); addEventListener('load',align);
     addEventListener('resize',setScrollPad); addEventListener('load',setScrollPad);
     if(document.fonts&&document.fonts.ready)document.fonts.ready.then(align);
     buildNav._wired=true;
   }
   align();
 }
 function curBasis(hasInterim){
   var b='annual';
   try{var u=new URLSearchParams(location.search).get('basis'); b=u||localStorage.getItem('am-basis')||'annual';}catch(e){}
   if(b==='interim'&&!hasInterim) b='annual';
   return b;
 }
 function basisSegHTML(cur,hasInterim){
   return '<div class="seg" role="group" aria-label="'+esc(L(BASIS.aria))+'">'
     +'<button type="button" data-b="annual" class="'+(cur==='annual'?'on':'')+'">'+esc(L(BASIS.annual))+'</button>'
     +'<button type="button" data-b="interim" class="'+(cur==='interim'?'on':'')+'"'+(hasInterim?'':' disabled title="'+esc(L(BASIS.soonT))+'"')+'>'+esc(L(BASIS.interim))+(hasInterim?'':'<span class="soon">'+esc(L(BASIS.soon))+'</span>')+'</button>'
     +'</div>';
 }
 function wireBasis(el,cur){
   el.querySelectorAll('button[data-b]').forEach(function(btn){
     btn.addEventListener('click',function(){
       if(btn.disabled) return;
       var nb=btn.dataset.b; if(nb===cur) return;
       try{localStorage.setItem('am-basis',nb);}catch(e){}
       try{var url=new URL(location.href); url.searchParams.set('basis',nb); history.replaceState(null,'',url);}catch(e){}
       document.dispatchEvent(new CustomEvent('axion:basischange',{detail:{basis:nb}}));
       renderBasis();
     });
   });
 }
 function renderBasis(){
   var bases=(window.AXION&&window.AXION.meta&&window.AXION.meta.bases)||['annual'];
   var hasInterim=bases.indexOf('interim')>-1;
   var cur=curBasis(hasInterim);
   var nav=document.getElementById('ambasis');
   // §35 — ΠΡΟΣΟΧΗ: το AX_NO_BASIS σημαίνει «όχι διακόπτης ΣΤΟ NAV» — οι περισσότερες
   // σελίδες τον μεταφέρουν στο σώμα (#ambasis-page). Η στατική ένδειξη μπαίνει ΜΟΝΟ με
   // ρητό AX_ANNUAL_ONLY (Κλάδοι/Κλάδος): συνειδητή απόφαση ότι τα εξαμηνιαία δεν έχουν
   // νόημα σε επίπεδο κλάδου — το λέμε, αντί να αφήνουμε τον χρήστη να μαντεύει.
   // Τα «Γεγονότα αγοράς» / «Αναθεωρήσεις δεικτών» ΔΕΝ παίρνουν ένδειξη: είναι
   // χρονολόγια γεγονότων, δεν είναι ούτε ετήσια ούτε εξαμηνιαία μεγέθη.
   if(nav){ if(window.AX_NO_BASIS){
              nav.innerHTML = window.AX_ANNUAL_ONLY
                ? '<span class="fixedbasis">'+esc(L(BASIS.annualOnly))+'</span>' : '';
            } else { nav.innerHTML=basisSegHTML(cur,hasInterim); wireBasis(nav,cur); } }
   var page=document.getElementById('ambasis-page');
   if(page){ page.innerHTML=basisSegHTML(cur,hasInterim); wireBasis(page,cur); }
 }

 /* ===== λωρίδα «Νέα αποτελέσματα» =====
    Πηγή: AXION.updates (γέφυρα) — οι 10 τελευταίες ΔΗΜΟΣΙΕΥΣΕΙΣ που έχουν
    ενσωματωθεί, με ημερομηνία δημοσίευσης έκθεσης από το Euronext.
    Το tag περιόδου είναι ΑΓΓΛΙΚΟ και στις δύο γλώσσες (6M 2026 / YR 2026). */
 var UPD_T={el:'Νέα αποτελέσματα',en:'New results'};
 function updPeriod(u){
   if(u.basis==='interim') return {cls:'p-h1',txt:'6M '+String(u.period).replace(/H1$/,'')};
   return {cls:'p-yr',txt:'YR '+u.period};
 }
 function updDate(iso){
   var p=String(iso).split('-'); if(p.length!==3) return '';
   return parseInt(p[2],10)+'/'+parseInt(p[1],10);
 }
 function renderUpdates(){
   var el=document.getElementById('amupd'); if(!el) return;
   var U=(window.AXION&&window.AXION.updates)||[];
   if(!U.length){ el.hidden=true; el.innerHTML=''; return; }
   var chips=U.map(function(u){
     var pr=updPeriod(u), nm=u.name||u.tk;
     return '<a class="chip" href="'+AX_CO(u.tk,u.basis)+'">'
          + '<span class="co">'+esc(nm)+'</span>'
          + '<span class="per '+pr.cls+'">'+esc(pr.txt)+'</span>'
          + '<span class="dt">'+updDate(u.date)+'</span></a>';
   }).join('');
   // σήμα εκπομπής: ραντάρ με σάρωση (§30/§114) — καθαρά διακοσμητικό, aria-hidden
   var sig='<span class="sig" aria-hidden="true"><u></u><i></i><i></i><s></s><b></b></span>';
   el.innerHTML='<div class="uhd">'+sig+'<span class="t">'+esc(L(UPD_T))+'</span></div>'
              + '<div class="chips">'+chips+'</div>';
   el.hidden=false;
 }
 /* §119 — η κολλητή κεφαλίδα ψήλωσε· τα in-page scroll (#anchors, scrollIntoView)
    πρέπει να σταματούν ΚΑΤΩ από αυτήν, αλλιώς ο στόχος κρύβεται από πίσω της */
 function setScrollPad(){
   var n=document.querySelector('.site-nav'); if(!n) return;
   document.documentElement.style.scrollPaddingTop=Math.round(n.getBoundingClientRect().height)+8+'px';
 }
 /* §119 — λωρίδα «Τελευταία γεγονότα»: τα 15 νεότερα εταιρικά γεγονότα, συνεχής κύλιση */
 var EV_T={el:'Τελευταία γεγονότα',en:'Latest events'};
 var EV_TYPE={amk:{el:'Μετ.Κεφαλαίου',en:'Capital'},
              div:{el:'Χρημ.Διανομές',en:'Distributions'},
              listing:{el:'Εισαγωγές/Διαγραφές',en:'Listings/Delistings'},
              index:{el:'Δείκτες',en:'Index changes'}};
 var EV_N=15, EV_PXS=75;   // πλήθος γεγονότων · ταχύτητα κύλισης σε px/δευτερόλεπτο
 function evDate(iso){ var p=String(iso).split('-'); if(p.length!==3) return '';
   return parseInt(p[2],10)+'/'+parseInt(p[1],10); }
 /* Η ΔΙΑΡΚΕΙΑ υπολογίζεται από το ΠΡΑΓΜΑΤΙΚΟ πλάτος του περιεχομένου, όχι σταθερή:
    αλλιώς μια μέρα με μακροσκελή κείμενα γεγονότων θα έτρεχε τη λωρίδα πιο γρήγορα
    από μια μέρα με σύντομα. Έτσι τα px/s μένουν σταθερά. */
 function evDur(el){
   var tr=el.querySelector('.track'); if(!tr) return;
   var d=(tr.scrollWidth/2)/EV_PXS;
   if(d>0) el.style.setProperty('--amev-dur', d.toFixed(1)+'s');
 }
 function renderEvents(){
   var el=document.getElementById('amev'); if(!el) return;
   var src=(window.AXION&&window.AXION.marketEvents)||[];
   var E=src.slice(0,EV_N);
   if(!E.length){ el.hidden=true; el.innerHTML=''; return; }
   var one=E.map(function(e){
     var tag=EV_TYPE[e.t]?L(EV_TYPE[e.t]):String(e.t||'');
     var inner='<span class="d">'+evDate(e.d)+'</span>'
             + '<span class="co">'+esc(e.co||e.tk||'')+'</span>'
             + '<span class="pill p-'+esc(e.t)+'">'+esc(tag)+'</span>'
             + '<span class="x">'+esc(e.x||'')+'</span>';
     var href=(typeof AX_CO==='function'&&e.tk)?AX_CO(e.tk):null;
     return href ? '<a class="ev" href="'+href+'">'+inner+'</a>'
                 : '<span class="ev">'+inner+'</span>';
   }).join('');
   el.innerHTML='<div class="elab"><span class="edot" aria-hidden="true"></span><span class="t">'+esc(L(EV_T))+'</span></div>'
              + '<div class="eview"><div class="track">'+one+one+'</div></div>';
   el.hidden=false;
   evDur(el); setScrollPad();
   // οι γραμματοσειρές φορτώνουν αργότερα και αλλάζουν το πλάτος -> ξαναμέτρηση
   try{ if(document.fonts&&document.fonts.ready) document.fonts.ready.then(function(){ evDur(el); setScrollPad(); }); }catch(_){}
 }
 function syncLangFlags(){
   var l=curLang(), bs=document.querySelectorAll('.langflags button[data-langset]');
   for(var i=0;i<bs.length;i++){
     if(bs[i].getAttribute('data-langset')===l){ bs[i].setAttribute('aria-current','true'); bs[i].disabled=true; }
     else { bs[i].removeAttribute('aria-current'); bs[i].disabled=false; }
   }
 }
 // fallback: αν ΔΕΝ υπάρχει AX_I18N, το κουμπί διαχειρίζεται μόνο του τη γλώσσα
 document.addEventListener('click',function(e){
   var b=e.target.closest && e.target.closest('.langflags button[data-langset]');
   if(b && !window.AX_I18N){
     e.preventDefault();
     var nl=b.getAttribute('data-langset');
     if(nl===curLang()) return;
     try{localStorage.setItem('am-lang',nl);}catch(_){}
     document.dispatchEvent(new CustomEvent('axion:langchange',{detail:{lang:nl}}));
   }
 });
 function relocalize(){ buildNav(); renderBasis(); renderUpdates(); renderEvents(); var f=document.querySelector('.site-ft'); if(f) f.outerHTML=footerHTML(); syncLangFlags(); }
 document.addEventListener('axion:langchange', relocalize);

 function injectAnalytics(){
   if(document.getElementById('cf-beacon')) return;
   var s=document.createElement('script');
   s.id='cf-beacon'; s.defer=true;
   s.src='https://static.cloudflareinsights.com/beacon.min.js';
   s.setAttribute('data-cf-beacon','{"token": "a9e573e27dd34f6784b7df2d706c1bee"}');
   document.head.appendChild(s);
 }
 function init(){ injectStyle(); mount(); buildNav(); renderBasis(); renderUpdates(); renderEvents(); syncLangFlags(); setScrollPad(); injectAnalytics(); }
 if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',init);} else {init();}
})();
