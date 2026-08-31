/* Axion Metrics — shared chrome. Injects nav+footer, wires tabs, basis toggle (Ετήσια/Εξάμηνο),
   και GR/EN toggle. Τα κείμενα είναι δίγλωσσα· η γλώσσα έρχεται από το AX_I18N (ή localStorage). */
(function(){
 function curLang(){ try{ return window.AX_I18N?window.AX_I18N.lang:(localStorage.getItem('am-lang')||'el'); }catch(e){ return 'el'; } }
 function L(o){ var l=curLang(); return (o&&o[l]!=null)?o[l]:(o&&o.el!=null?o.el:''); }
 function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

 const NAV=[
   {g:{el:'Εταιρείες',en:'Companies'},items:[
     [{el:'Σελίδα εταιρείας',en:'Company page'},'../company/'],
     [{el:'Σύγκριση εταιρειών',en:'Compare companies'},'../compare/'],
     [{el:'Κατατάξεις / League tables',en:'Rankings / League tables'},'../rankings/']]},
   {g:{el:'Κλάδοι',en:'Sectors'},items:[
     [{el:'Ευρετήριο κλάδων',en:'Sector index'},'../sectors/'],
     [{el:'Σελίδα κλάδου',en:'Sector page'},'../sector/']]},
   {g:{el:'Εργαλεία',en:'Tools'},items:[
     [{el:'Αναθεωρήσεις δεικτών',en:'Index reviews'},'../index-reviews/'],
     [{el:'Γεγονότα αγοράς',en:'Market events'},'../market-events/']]},
   {g:{el:'Σχετικά',en:'About'},items:[
     [{el:'Μεθοδολογία & δείκτες',en:'Methodology & ratios'},'../methodology/'],
     [{el:'Περί',en:'About'},'../about/'],
     [{el:'Όροι χρήσης',en:'Terms of use'},'../terms/']]}
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
   aria:{el:'Βάση δεδομένων',en:'Data basis'} };

 var NAVHTML="<nav class=\"site-nav\">\n <div class=\"bar1\"><a class=\"lock\" href=\"../\"><span class=\"am\">A<i>M</i></span><span class=\"lrule\"></span><span class=\"lname\">AXION<br>METRICS</span></a><ul class=\"tabs\" id=\"navtabs\"></ul><div class=\"am-right\"><div class=\"am-basis\" id=\"ambasis\"></div><button class=\"langtog\" data-langtog aria-label=\"Language\">EN</button></div></div>\n <div class=\"bar2\" id=\"navbar2\"></div>\n</nav>";

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
   st.textContent=".am-right{display:flex;align-items:center;gap:10px}.langtog{border:1px solid rgba(255,255,255,.28);background:transparent;color:#eaf1fb;font:700 11.5px Inter,system-ui,sans-serif;padding:5px 9px;border-radius:8px;cursor:pointer;letter-spacing:.05em;line-height:1}.langtog:hover{background:rgba(255,255,255,.12)}";
   document.head.appendChild(st);
 }

 function mount(){
   var nm=document.getElementById('am-nav');
   if(nm){nm.outerHTML=NAVHTML;} else if(!document.querySelector('.site-nav')){document.body.insertAdjacentHTML('afterbegin',NAVHTML);}
   var fm=document.getElementById('am-foot');
   if(fm){fm.outerHTML=footerHTML();} else if(!document.querySelector('.site-ft')){document.body.insertAdjacentHTML('beforeend',footerHTML());}
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
   if(nav){ if(window.AX_NO_BASIS){ nav.innerHTML=''; } else { nav.innerHTML=basisSegHTML(cur,hasInterim); wireBasis(nav,cur); } }
   var page=document.getElementById('ambasis-page');
   if(page){ page.innerHTML=basisSegHTML(cur,hasInterim); wireBasis(page,cur); }
 }
 function relabelLangBtn(){
   var b=document.querySelector('.langtog[data-langtog]');
   if(b) b.textContent=(curLang()==='en'?'ΕΛ':'EN');
 }
 // fallback: αν ΔΕΝ υπάρχει AX_I18N, το κουμπί διαχειρίζεται μόνο του τη γλώσσα
 document.addEventListener('click',function(e){
   var b=e.target.closest && e.target.closest('.langtog[data-langtog]');
   if(b && !window.AX_I18N){
     e.preventDefault();
     var nl=(curLang()==='en'?'el':'en');
     try{localStorage.setItem('am-lang',nl);}catch(_){}
     document.dispatchEvent(new CustomEvent('axion:langchange',{detail:{lang:nl}}));
   }
 });
 function relocalize(){ buildNav(); renderBasis(); var f=document.querySelector('.site-ft'); if(f) f.outerHTML=footerHTML(); relabelLangBtn(); }
 document.addEventListener('axion:langchange', relocalize);

 function injectAnalytics(){
   if(document.getElementById('cf-beacon')) return;
   var s=document.createElement('script');
   s.id='cf-beacon'; s.defer=true;
   s.src='https://static.cloudflareinsights.com/beacon.min.js';
   s.setAttribute('data-cf-beacon','{"token": "a9e573e27dd34f6784b7df2d706c1bee"}');
   document.head.appendChild(s);
 }
 function init(){ injectStyle(); mount(); buildNav(); renderBasis(); relabelLangBtn(); injectAnalytics(); }
 if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',init);} else {init();}
})();
