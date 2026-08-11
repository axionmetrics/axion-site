/* Axion Metrics — shared chrome. Injects nav+footer, wires tabs, builds the Ετήσια/Εξάμηνο basis toggle. */
(function(){
 const NAV=[{g:'Εταιρείες',items:[['Σελίδα εταιρείας','../company/'],['Σύγκριση εταιρειών','../compare/']]},{g:'Κλάδοι',items:[['Ευρετήριο κλάδων','../sectors/'],['Σελίδα κλάδου','../sector/']]},{g:'Εργαλεία',items:[['Κατατάξεις / League tables','../rankings/'],['Αναθεωρήσεις δεικτών','../index-reviews/'],['Γεγονότα αγοράς','../market-events/']]},{g:'Σχετικά',items:[['Μεθοδολογία & δείκτες','../methodology/'],['Περί','../about/'],['Όροι χρήσης','../terms/']]}];
 var NAV_ACTIVE=(typeof window.NAV_ACTIVE==='number')?window.NAV_ACTIVE:0;
 var NAV_CUR=window.NAV_CUR||(NAV[NAV_ACTIVE]&&NAV[NAV_ACTIVE].items[0][0]);
 var NAVHTML="<nav class=\"site-nav\">\n <div class=\"bar1\"><a class=\"lock\" href=\"../\"><span class=\"am\">A<i>M</i></span><span class=\"lrule\"></span><span class=\"lname\">AXION<br>METRICS</span></a><ul class=\"tabs\" id=\"navtabs\"></ul><div class=\"am-basis\" id=\"ambasis\"></div></div>\n <div class=\"bar2\" id=\"navbar2\"></div>\n</nav>";
 var FOOTERHTML="<footer class=\"site-ft\"><div class=\"in\"><div class=\"fbrand\"><div class=\"flogo\">AXION<i>METRICS</i></div><div class=\"ftag\">Θεμελιώδης ανάλυση για 133 εισηγμένες του Χρηματιστηρίου Αθηνών — δείκτες, σύγκριση κλάδου, ποιότητα &amp; δυναμική.</div></div><div class=\"fcol\"><h4>Κλάδοι</h4><a href=\"../sectors/\">Ευρετήριο κλάδων</a><a href=\"../sector/\">Σελίδα κλάδου</a><a href=\"../compare/\">Σύγκριση εταιρειών</a></div><div class=\"fcol\"><h4>Εργαλεία</h4><a href=\"../rankings/\">Κατατάξεις</a><a href=\"../index-reviews/\">Αναθεωρήσεις δεικτών</a><a href=\"../market-events/\">Γεγονότα αγοράς</a></div><div class=\"fcol\"><h4>Πληροφορίες</h4><a href=\"../methodology/\">Μεθοδολογία &amp; δείκτες</a><a href=\"../about/\">Περί</a><a href=\"../terms/\">Όροι χρήσης</a></div></div><div class=\"fbot\">© 2026 Axion Metrics · Δεν αποτελεί επενδυτική συμβουλή · <a href=\"mailto:info@axionmetrics.gr\" style=\"color:inherit\">info@axionmetrics.gr</a></div></footer>";
 function mount(){
   var nm=document.getElementById('am-nav');
   if(nm){nm.outerHTML=NAVHTML;} else if(!document.querySelector('.site-nav')){document.body.insertAdjacentHTML('afterbegin',NAVHTML);}
   var fm=document.getElementById('am-foot');
   if(fm){fm.outerHTML=FOOTERHTML;} else if(!document.querySelector('.site-ft')){document.body.insertAdjacentHTML('beforeend',FOOTERHTML);}
 }
 function buildNav(){
   var tabs=document.getElementById('navtabs'), bar2=document.getElementById('navbar2');
   if(!tabs||!bar2) return;
   tabs.innerHTML=NAV.map(function(s,i){return '<li data-i="'+i+'" class="'+(i===NAV_ACTIVE?'on':'')+'">'+s.g+'</li>';}).join('');
   bar2.innerHTML=NAV[NAV_ACTIVE].items.map(function(it){return '<a href="'+it[1]+'" class="'+(it[0]===NAV_CUR?'cur':'')+'">'+it[0]+'</a>';}).join('');
   tabs.addEventListener('click',function(e){var li=e.target.closest('li');if(li){var g=NAV[+li.dataset.i];if(g&&g.items[0])location.href=g.items[0][1];}});
   function align(){
     if(innerWidth<=820){bar2.style.paddingLeft='';return;}
     var at=tabs.querySelector('li.on'), fa=bar2.querySelector('a'); if(!at||!fa)return;
     var ts=getComputedStyle(at), fs=getComputedStyle(fa);
     var off=(at.getBoundingClientRect().left+parseFloat(ts.paddingLeft))-(bar2.getBoundingClientRect().left+parseFloat(fs.paddingLeft));
     bar2.style.paddingLeft=Math.max(0,off)+'px';
   }
   align(); addEventListener('resize',align); addEventListener('load',align);
   if(document.fonts&&document.fonts.ready)document.fonts.ready.then(align);
 }
 function curBasis(hasInterim){
   var b='annual';
   try{var u=new URLSearchParams(location.search).get('basis'); b=u||localStorage.getItem('am-basis')||'annual';}catch(e){}
   if(b==='interim'&&!hasInterim) b='annual';
   return b;
 }
 function renderBasis(){
   var el=document.getElementById('ambasis'); if(!el) return;
   var bases=(window.AXION&&window.AXION.meta&&window.AXION.meta.bases)||['annual'];
   var hasInterim=bases.indexOf('interim')>-1;
   var cur=curBasis(hasInterim);
   el.innerHTML='<div class="seg" role="group" aria-label="Βάση δεδομένων">'
     +'<button type="button" data-b="annual" class="'+(cur==='annual'?'on':'')+'">Ετήσια</button>'
     +'<button type="button" data-b="interim" class="'+(cur==='interim'?'on':'')+'"'+(hasInterim?'':' disabled title="Σύντομα διαθέσιμο"')+'>Εξάμηνο'+(hasInterim?'':'<span class="soon">σύντομα</span>')+'</button>'
     +'</div>';
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
 function init(){ mount(); buildNav(); renderBasis(); }
 if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',init);} else {init();}
})();
