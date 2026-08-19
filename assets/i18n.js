/* Axion Metrics — i18n engine (GR/EN). Κοινό για όλες τις σελίδες.
   Χρήση: data-i18n="key" (textContent), data-i18n-html, data-i18n-ph (placeholder),
   data-i18n-title. Κάθε σελίδα δηλώνει το λεξικό της με AX_I18N.add({...}).
   Μετάφραση δεδομένων: AX_I18N.sector(name), AX_I18N.evtype(t). */
(function(){
  var LS='am-lang';
  var LANG=(function(){try{return localStorage.getItem(LS)||'el';}catch(e){return 'el';}})();
  var DICT={};

  function add(o){ if(o){ for(var k in o) DICT[k]=o[k]; } apply(); }
  function t(k){ var e=DICT[k]; if(e==null) return null; return (e[LANG]!=null)?e[LANG]:(e.el!=null?e.el:null); }

  function apply(root){
    root=root||document;
    var i,els;
    els=root.querySelectorAll('[data-i18n]');
    for(i=0;i<els.length;i++){ var v=t(els[i].getAttribute('data-i18n')); if(v!=null) els[i].textContent=v; }
    els=root.querySelectorAll('[data-i18n-html]');
    for(i=0;i<els.length;i++){ var vh=t(els[i].getAttribute('data-i18n-html')); if(vh!=null) els[i].innerHTML=vh; }
    els=root.querySelectorAll('[data-i18n-ph]');
    for(i=0;i<els.length;i++){ var vp=t(els[i].getAttribute('data-i18n-ph')); if(vp!=null) els[i].setAttribute('placeholder',vp); }
    els=root.querySelectorAll('[data-i18n-title]');
    for(i=0;i<els.length;i++){ var vt=t(els[i].getAttribute('data-i18n-title')); if(vt!=null) els[i].setAttribute('title',vt); }
    document.documentElement.setAttribute('lang', LANG==='en'?'en':'el');
    var togs=root.querySelectorAll('[data-langtog]');
    for(i=0;i<togs.length;i++){ togs[i].textContent = (LANG==='en'?'ΕΛ':'EN'); }
  }

  function setLang(l){
    if(l===LANG) return;
    LANG=l; try{localStorage.setItem(LS,l);}catch(e){}
    apply();
    document.dispatchEvent(new CustomEvent('axion:langchange',{detail:{lang:l}}));
  }
  function toggle(){ setLang(LANG==='en'?'el':'en'); }

  /* ---- data translation maps ---- */
  var SECTORS={
    'Holding':'Holdings',
    'Ακίνητα':'Real Estate',
    'Βιομηχανία & Βασικά Υλικά':'Industry & Basic Materials',
    'Εμπόριο & Διανομή':'Trade & Distribution',
    'Ενέργεια & Κοινής Ωφέλειας':'Energy & Utilities',
    'Καταναλωτικά Αγαθά':'Consumer Goods',
    'Κατασκευές, Υποδομές & Μεταφορές':'Construction, Infrastructure & Transport',
    'Τεχνολογία, ΜΜΕ & Τηλεπικοινωνίες':'Technology, Media & Telecom',
    'Τράπεζες':'Banks',
    'Χρηματοοικονομικά':'Financials'
  };
  function sector(s){ return (LANG==='en'&&SECTORS[s])?SECTORS[s]:s; }

  // event display types (site families): div, amk(capital), listing, index
  var EVTYPE={ 'div':'Distributions', 'amk':'Capital', 'listing':'Listings/Delistings', 'index':'Index changes' };
  function evtype(x){ return (LANG==='en'&&EVTYPE[x])?EVTYPE[x]:x; }

  window.AX_I18N={
    get lang(){return LANG;},
    add:add, t:t, apply:apply, setLang:setLang, toggle:toggle,
    sector:sector, evtype:evtype
  };

  // global click handler for any [data-langtog]
  document.addEventListener('click',function(e){
    var b=e.target.closest && e.target.closest('[data-langtog]');
    if(b){ e.preventDefault(); toggle(); }
  });

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',function(){apply();});
  else apply();
})();
