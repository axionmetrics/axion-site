AX_I18N.add({
 'co.hero.h1':{el:'Εταιρεία', en:'Company'},
 'co.hs.ratios':{el:'Αριθμοδείκτες', en:'Ratios'},
 'co.hs.hist':{el:'Ιστορικότητα', en:'History'}, 'co.hs.histl':{el:'από 2020', en:'since 2020'},
 'co.hs.cons':{el:'Ενοποιημένη', en:'Consolidated'}, 'co.hs.consl':{el:'Βάση', en:'Basis'},
 'co.hs.median':{el:'Διάμεσος κλάδου', en:'Sector median'}, 'co.hs.medianl':{el:'Σημείο σύγκρισης', en:'Benchmark'},
 'co.qsopen':{el:'Επιλογή εταιρείας', en:'Select company'},
 'co.qsopen.title':{el:'Γρήγορη εύρεση εταιρείας', en:'Quick company search'},
 'co.ph.holders':{el:'Μέτοχοι', en:'Shareholders'},
 'co.ph.subs':{el:'Θυγατρικές & συμμετοχές', en:'Subsidiaries & holdings'},
 'co.ph.glance':{el:'Με μια ματιά', en:'At a glance'},
 'co.hint.vssec':{el:'έναντι κλάδου', en:'vs sector'},
 'co.ph.dist':{el:'Χρηματικές διανομές', en:'Cash distributions'},
 'co.hint.3y':{el:'3ετία', en:'3-year'},
 'co.ph.ratios':{el:'Αριθμοδείκτες', en:'Ratios'},
 'co.ph.traj':{el:'Τροχιά μεγεθών', en:'Key figures over time'},
 'co.leg.rev':{el:'Τζίρος', en:'Revenue'},
 'co.leg.ppi':{el:'PPI', en:'PPI'},
 'co.unit.meur2':{el:'(εκατ. €)', en:'(€M)'},
 'co.subs.ph':{el:'Αναζήτηση θυγατρικής ή χώρας…', en:'Search subsidiary or country…'},
 'co.subs.none':{el:'Δεν εντοπίστηκαν θυγατρικές ή συμμετοχές στις δημοσιευμένες οικονομικές καταστάσεις.', en:'No subsidiaries or holdings identified in the published financial statements.'},
 'co.ratios.note':{el:'<strong>Διάμεσος κλάδου:</strong> η σύγκριση γίνεται με τη διάμεση («τυπική») τιμή των εταιρειών του κλάδου, όχι με μέσο όρο — έτσι ακραίες τιμές λίγων εταιρειών δεν αλλοιώνουν τη σύγκριση. Οι τράπεζες εξετάζονται χωριστά.', en:'<strong>Sector median:</strong> the comparison uses the median (“typical”) value of the sector’s companies, not the average — so extreme values from a few companies do not distort the comparison. Banks are examined separately.'},
 'co.qs.title':{el:'Εύρεση εταιρείας', en:'Find company'},
 'co.qs.ph':{el:'Όνομα ή σύμβολο…', en:'Name or symbol…'},
 'co.qs.nav':{el:'πλοήγηση', en:'navigate'},
 'co.qs.open':{el:'άνοιγμα', en:'open'},
 'co.qs.close':{el:'κλείσιμο', en:'close'},
 'co.qs.empty':{el:'Καμία εταιρεία δεν ταιριάζει.', en:'No company matches.'},
 // metrics
 'co.m.revenue':{el:'Τζίρος', en:'Revenue'},
 'co.m.net_profit':{el:'Καθαρά κέρδη', en:'Net profit'},
 'co.m.ebitda':{el:'EBITDA', en:'EBITDA'},
 // §45 — EBITDA: δημοσιευμένο έναντι υπολογισμένου
 'co.eb.s.reponly':{el:'Ο αριθμός είναι το <b>δημοσιευμένο</b> EBITDA της εταιρείας. Για αυτή την εταιρεία δεν υπολογίζουμε δικό μας EBITDA — ο ενιαίος τύπος δεν έχει νόημα στη δομή της.', en:'This figure is the company\u2019s <b>reported</b> EBITDA. We do not compute our own EBITDA for this company \u2014 the standard formula is not meaningful for its structure.'},
 'co.eb.s.own':{el:'<b>Η εταιρεία δεν δημοσιεύει EBITDA.</b> Ο αριθμός είναι <b>υπολογισμός Axion</b> με τον ίδιο τύπο που εφαρμόζεται σε όλες τις εισηγμένες: κέρδη προ φόρων + τόκοι − χρηματοοικονομικά έσοδα + αποσβέσεις.', en:'<b>The company does not report EBITDA.</b> This figure is an <b>Axion calculation</b> using the same formula applied to every listed company: pre-tax profit + interest − financial income + depreciation.'},
 /* §45.8 — ΣΥΓΚΡΙΣΙΜΟ (ADJUSTED) EBITDA: το δημοσιεύει η ΙΔΙΑ η εταιρεία δίπλα στο
    κανονικό, με δικό της ορισμό (έκτακτα, επιδράσεις αποτίμησης, φάσεις κόστους). Δεν
    συγκρίνεται μεταξύ εισηγμένων, άρα ΔΕΝ τροφοδοτεί δείκτη ή κατάταξη — μπαίνει μόνο
    στη λωρίδα, ώστε να μη λείπει από τη σελίδα μέγεθος που ανακοίνωσε η εταιρεία. */
 'co.eb.s.adj':{el:'Η εταιρεία δημοσιεύει και <b>συγκρίσιμο (adjusted) EBITDA {v}</b> για την ίδια περίοδο — μέγεθος με δικό της ορισμό, που αφαιρεί έκτακτα και επιδράσεις αποτίμησης. Δεν είναι συγκρίσιμο μεταξύ εισηγμένων, γι\u2019 αυτό οι δείκτες και οι κατατάξεις χρησιμοποιούν πάντα το <b>υπολογισμένο Axion</b>.',
                en:'The company also reports an <b>adjusted EBITDA of {v}</b> for the same period — a measure it defines itself, stripping out one-off items and valuation effects. It is not comparable across listed companies, so ratios and rankings always use the <b>Axion calculation</b>.'},
 'co.eb.s.plain':{el:'Και τα δύο είναι <b>κανονικό EBITDA</b>. Η διαφορά προκύπτει από τον τρόπο δόμησης: η εταιρεία ξεκινά συνήθως από το λειτουργικό αποτέλεσμα, ο <b>υπολογισμός Axion</b> από τα κέρδη προ φόρων — άρα διαφέρουν κατά στοιχεία όπως τα αποτελέσματα συγγενών και οι αποσβέσεις επιχορηγήσεων.', en:'Both are <b>standard EBITDA</b>. The difference comes from how each is built: the company typically starts from operating profit, the <b>Axion calculation</b> from pre-tax profit — so they differ by items such as results of associates and amortisation of grants.'},
 'co.eb.s.kind':{el:'Η εταιρεία δημοσιεύει EBITDA {k} — {w}. Το <b>υπολογισμένο Axion</b> εφαρμόζει τον ίδιο τύπο σε όλες τις εισηγμένες και είναι αυτό που χρησιμοποιείται στις κατατάξεις και στις διαμέσους κλάδου.', en:'The company reports EBITDA {k} — {w}. The <b>Axion calculation</b> applies the same formula to every listed company and is what feeds the rankings and sector medians.'},
 'co.eb.w.val':{el:'<b>εξαιρεί κέρδη ή ζημιές από αναπροσαρμογή σε εύλογη αξία</b>', en:'<b>it excludes fair-value revaluation gains and losses</b>'},
 'co.eb.w.adj':{el:'<b>εξαιρεί έκτακτα ή μη επαναλαμβανόμενα στοιχεία</b>', en:'<b>it excludes one-off or non-recurring items</b>'},
 'co.eb.w.met':{el:'<b>απομονώνει το αποτέλεσμα εμπορεύματος</b>', en:'<b>it isolates the commodity result</b>'},
 'co.eb.w.fx':{el:'<b>εξαιρεί τις συναλλαγματικές διαφορές</b>', en:'<b>it excludes foreign-exchange differences</b>'},
 'co.eb.w.gen':{el:'<b>ακολουθεί διαφορετικό ορισμό από τον δικό μας</b>', en:'<b>it follows a different definition from ours</b>'},
 // §68 — ΚΑΘΑΡΑ ΚΕΡΔΗ έναντι ΚΕΡΔΩΝ ΜΕΤΑ ΦΟΡΩΝ. Εμφανίζεται ΜΟΝΟ όταν τα δύο διαφέρουν.
 'co.np.s.mi':{el:'Τα καθαρά κέρδη (ή ζημίες) είναι όσα αναλογούν στους μετόχους της μητρικής, χωρίς το μερίδιο <b>«μη ελεγχουσών συμμετοχών σε θυγατρικές»</b>.', en:'Net profit (or loss) is the share attributable to the parent company\u2019s shareholders, excluding the share of <b>non-controlling interests in subsidiaries</b>.'},
 'co.m.ppi':{el:'PPI', en:'PPI'},
 'co.na.banks':{el:'Δεν εφαρμόζεται σε τράπεζες', en:'Not applicable to banks'},
 'co.m.mcap':{el:'Κεφαλαιοποίηση', en:'Market cap'},
 'co.m.pe':{el:'P/E', en:'P/E'},
 'co.m.pbv':{el:'P/BV', en:'P/BV'},
 'co.m.cash':{el:'Ταμείο', en:'Cash'},
 'co.m.loans':{el:'Δάνεια', en:'Loans'},
 'co.m.deposits':{el:'Καταθέσεις', en:'Deposits'},
 'co.m.total_debt':{el:'Συν. δανεισμός', en:'Total debt'},
 'co.m.net_debt':{el:'Καθ. δανεισμός', en:'Net debt'},
 // current band
 // FAM / event families
 'co.fam.capital':{el:'Μετ.Κεφαλαίου', en:'Capital'},
 'co.fam.div':{el:'Χρημ.Διανομές', en:'Distributions'},
 'co.fam.listing':{el:'Εισαγωγές/Διαγραφές', en:'Listings/Delistings'},
 'co.fam.index':{el:'Δείκτες', en:'Index'},
 'co.evk.plural':{el:'γεγονότα', en:'events'},
 // status banners
 'co.entity.badge':{el:'Εκτός κάλυψης', en:'Out of coverage'},
 'co.echange.badge':{el:'Αλλαγή οντότητας', en:'Entity change'},
 'co.echange.text':{el:'Από το {year} η δομή της εταιρείας άλλαξε ουσιωδώς — τα ιστορικά μεγέθη δεν είναι απευθείας συγκρίσιμα με την τρέχουσα οντότητα.', en:'From {year} the company\'s structure changed materially — historical figures are not directly comparable with the current entity.'},
 'co.echange.mark':{el:'νέα οντότητα', en:'new entity'},
 // interim banner
 'co.h1.pill':{el:'εξάμηνα', en:'semesters'},
 'co.h1.of':{el:'από 2 εξάμηνα', en:'of 2 semesters'},
 'co.h1.detail':{el:'— διαθέσιμοι οι δείκτες στιγμιότυπου (αποτίμηση, περιθώρια, ρευστότητα, D/E). Η σύγκριση με πέρσι, το Piotroski και οι τάσεις ενεργοποιούνται με το 2ο εξάμηνο.', en:'— snapshot ratios are available (valuation, margins, liquidity, D/E). Year-on-year comparison, the Piotroski score and trends activate with the 2nd semester.'},
 // chart
 'co.chart.events':{el:'Εταιρικά γεγονότα', en:'Corporate events'},
 'co.chart.netprofit':{el:'Καθ. κέρδη', en:'Net profit'},
 'co.chart.totaldebt':{el:'Συν. δανεισμός', en:'Total debt'},
 'co.chart.netdebt':{el:'Καθ. δανεισμός', en:'Net debt'},
 'co.chart.npe':{el:'NPE ratio', en:'NPE ratio'},
 // subs / geo
 'co.geo.entities':{el:'οντότητες', en:'entities'},
 'co.geo.countries':{el:'χώρες', en:'countries'},
 'co.geo.country':{el:'χώρα', en:'country'},
 'co.geo.other':{el:'Λοιπές', en:'Other'},
 'co.geo.listed':{el:'εισηγμένη', en:'listed'},
 'co.geo.entities_n':{el:'οντότητες', en:'entities'},
 'co.geo.in':{el:' σε ', en:' in '},
 // ratios table
 'co.rt.ratio':{el:'Δείκτης', en:'Ratio'},
 'unit.days':{el:' ημ.', en:' d'},
 // glance
 'co.gl.profit':{el:'Κερδοφορία', en:'Profitability'},
 'co.gl.growth':{el:'Ανάπτυξη', en:'Growth'},
 'co.gl.lev':{el:'Μόχλευση', en:'Leverage'},
 'co.gl.liq':{el:'Ρευστότητα', en:'Liquidity'},
 'co.gl.b3':{el:'μ.ο. 3ετίας', en:'3-yr avg'},
 'co.gl.bp':{el:'περιόδου', en:'period'},
 // §31 — δυναμική ετικέτα βάσης στην όψη 6μήνου: λέει ΠΟΣΕΣ και ΠΟΙΕΣ περίοδοι μπήκαν
 'co.gl.sector':{el:'κλάδος ', en:'sector '},
 'co.gl.met.ebt':{el:'Κέρδη προ φόρων', en:'Pre-tax profit'},
 'co.gl.met.rev':{el:'Τζίρος', en:'Revenue'},
 'co.gl.met.de':{el:'Χρέος/Ίδια', en:'Debt/Equity'},
 'co.gl.met.cur':{el:'Γενική', en:'Current'},
 'co.gl.r.lossmk':{el:'Ζημιογόνα', en:'Loss-making'},
 'co.gl.r.profit':{el:'Κερδοφόρα', en:'Profitable'},
 'co.gl.r.low':{el:'Χαμηλή', en:'Low'},
 'co.gl.r.mod':{el:'Μέτρια', en:'Moderate'},
 'co.gl.r.high':{el:'Υψηλή', en:'High'},
 'co.gl.r.shrink':{el:'Συρρίκνωση', en:'Shrinking'},
 'co.gl.r.stag':{el:'Στάσιμη', en:'Stagnant'},
 'co.gl.r.steady':{el:'Σταθερή', en:'Steady'},
 'co.gl.r.strong':{el:'Ισχυρή', en:'Strong'},
 'co.gl.r.negeq':{el:'Αρνητικά ίδια', en:'Negative equity'},
 'co.gl.r.adeq':{el:'Επαρκής', en:'Adequate'},
 'co.gl.r.marg':{el:'Οριακή', en:'Marginal'},
 'co.gl.r.strained':{el:'Πιεσμένη', en:'Strained'},
 'co.gl.liqNpe':{el:'Ποιότητα', en:'Asset quality'},
 'co.gl.met.npe':{el:'NPE ratio', en:'NPE ratio'},
 'co.gl.r.npeLow':{el:'Χαμηλό', en:'Low'},
 'co.gl.r.npeMod':{el:'Μέτριο', en:'Moderate'},
 'co.gl.r.npeHigh':{el:'Υψηλό', en:'High'},
 // dist
 'co.dist.yr':{el:'Έτος', en:'Year'},
 'co.dist.divsh':{el:'Μέρισμα', en:'Dividend'},
 'co.dist.capsh':{el:'Επιστρ. κεφ.', en:'Capital ret.'},
 'co.dist.yield':{el:'Απόδοση', en:'Yield'},
 'co.dist.note':{el:'Μέρισμα ανά χρήση· επιστροφές κεφαλαίου ανά έτος πληρωμής.', en:'Dividend per fiscal year; capital returns per payment year.'},
 'co.dist.none':{el:'Δεν διανέμει', en:'No distributions'},
 'co.dist.none.s':{el:'Καμία χρηματική διανομή στους μετόχους την τελευταία 3ετία.', en:'No cash distribution to shareholders in the last 3 years.'},
 'co.latest.note':{el:'Στοιχεία τελευταίας ενημερωμένης περιόδου', en:'Figures for the latest updated period'},
 'co.basis.annual':{el:'ΕΤΗΣΙΑ', en:'ANNUAL'},
});
// §185 — κλειδιά της νέας διάταξης (Μεγέθη περιόδου · Αριθμοδείκτες · compact blocks)
AX_I18N.add({
 'co.ph.per':{el:'Μεγέθη περιόδου', en:'Period figures'},
 'co.ph.shorts':{el:'Short θέσεις', en:'Short positions'},
 'co.per.fig':{el:'Μέγεθος', en:'Figure'},
 'co.per.unit':{el:'(εκ. €)', en:'(€M)'},
 'co.per.annual':{el:'Ετήσια {y}', en:'Annual {y}'},
 'co.per.h1':{el:'6Μ {y}', en:'6M {y}'},
 'co.per.q1':{el:'3Μ {y}', en:'3M {y}'},
 'co.per.q3':{el:'9Μ {y}', en:'9M {y}'},
 'co.per.px':{el:'Τιμές {d}', en:'Prices {d}'},
 'co.per.note':{el:'Η μεταβολή συγκρίνει με την ίδια περίοδο πέρσι. Το P/E του 6μήνου υπολογίζεται με τα κέρδη 12μήνου (TTM) και το P/BV με τα ίδια κεφάλαια της 30/06. Οι στήλες «Τιμές {d}» εφαρμόζουν την κεφαλαιοποίηση της {d}.',
                en:'Changes compare with the same period a year earlier. The 6M P/E uses trailing twelve-month earnings (TTM) and the P/BV uses equity at 30/06. The «Prices {d}» columns apply the market capitalisation of {d}.'},
 'co.per.note1':{el:'Η μεταβολή συγκρίνει με την προηγούμενη χρήση. Η στήλη «Τιμές {d}» εφαρμόζει την κεφαλαιοποίηση της {d}.',
                 en:'Changes compare with the previous fiscal year. The «Prices {d}» column applies the market capitalisation of {d}.'},
 'co.per.note0':{el:'Η μεταβολή συγκρίνει με την προηγούμενη χρήση.', en:'Changes compare with the previous fiscal year.'},
 'co.per.fnp':{el:'{p}: ', en:'{p}: '},
 'co.np.s.patq':{el:'Η εταιρεία δημοσίευσε μόνο τα <b>κέρδη μετά φόρων του ομίλου</b>, χωρίς τον διαχωρισμό του μεριδίου των μη ελεγχουσών συμμετοχών.', en:'The company published only the <b>group profit after tax</b>, without separating the share of non-controlling interests.'},
 'co.eb.s.reponlyq':{el:'Ο αριθμός είναι το <b>δημοσιευμένο</b> EBITDA της εταιρείας. Η ανακοίνωση της περιόδου δεν περιέχει τα στοιχεία για δικό μας υπολογισμό.', en:'This figure is the company\u2019s <b>reported</b> EBITDA. The period announcement does not contain the figures needed for our own calculation.'},
 'co.per.noteq':{el:'Στο 3μηνο και στο 9μηνο εμφανίζονται μόνο τα μεγέθη που δημοσιεύει η εταιρεία· η μεταβολή συγκρίνει με την ίδια περίοδο πέρσι.', en:'The 3M and 9M columns show only the figures the company publishes; changes compare with the same period a year earlier.'},
 'co.eb.s.axv':{el:' Υπολογισμός Axion: <b>{v}</b>.', en:' Axion calculation: <b>{v}</b>.'},
 'co.rt.sector':{el:'Κλάδος', en:'Sector'},
 'co.rt.close':{el:'κλείσιμο', en:'close'},
 'co.rt.n1':{el:'δείκτης', en:'ratio'},
 'co.rt.nn':{el:'δείκτες', en:'ratios'},
 'co.rt.half':{el:'μισού έτους, μη ετησιοποιημένο', en:'half-year, not annualised'},
 'co.geo.all':{el:'Όλες οι οντότητες', en:'All entities'},
 'co.geo.entity':{el:'οντότητα', en:'entity'},
 'co.geo.listedh':{el:'Εισηγμένες', en:'Listed'},
 'co.ff':{el:'Free float', en:'Free float'}
});
function L(k){var v=AX_I18N.t(k);return v==null?'':v;}
function curLang(){return window.AX_I18N?AX_I18N.lang:'el';}
function EN(){return curLang()==='en';}
function LOC(){return EN()?'en-US':'el-GR';}
document.addEventListener('axion:langchange',function(){location.reload();});

// §185 — Η ΣΕΛΙΔΑ ΔΕΙΧΝΕΙ ΠΑΝΤΑ ΕΤΗΣΙΑ ΚΑΙ 6ΜΗΝΟ ΜΑΖΙ. Ο διακόπτης «Ετήσια | Εξάμηνο» καταργήθηκε:
// η βάση της σελίδας είναι η ετήσια (τροχιά, ιστορικό δεικτών, διανομές) και τα 6μηνα
// μεγέθη/δείκτες διαβάζονται παράλληλα από το AXION.companies.interim (AXI παρακάτω).
// Το ?basis=interim και το localStorage 'am-basis' αγνοούνται εδώ.
const AXBASIS='annual';
const _AXC=(window.AXION&&window.AXION.companies&&window.AXION.companies[AXBASIS])||[];
// §75 — στις στατικές σελίδες /etaireia/<slug>/ δεν υπάρχει ?tk=· το κέλυφος ψήνει AX_TK.
let _tk=new URLSearchParams(location.search).get('tk')||window.AX_TK||null;
try{ if(!_tk){ const _saved=localStorage.getItem('am-last-company'); if(_saved&&_AXC.find(function(c){return c.tk===_saved;})) _tk=_saved; } }catch(e){}
const AX=(_tk&&_AXC.find(function(c){return c.tk===_tk;}))||_AXC[0]||null;
try{ if(AX&&AX.tk) localStorage.setItem('am-last-company', AX.tk); }catch(e){}
document.addEventListener('axion:basischange',function(){location.reload();});
const company = AX ? {ticker:AX.tk,name:AX.name,euronext_name:(AX.en||''),sector:AX.s,latest:AX.latest,years:AX.years,metrics:AX.metrics,figNotes:(AX.figNotes||null),byNature:(AX.bynature||null),current:((window.AXION_CURRENT&&window.AXION_CURRENT[AX.tk])||AX.current||null)} : {ticker:'',name:'—',euronext_name:'',sector:'',latest:{period:'',type:''},years:[2020,2021,2022,2023,2024,2025],metrics:{revenue:[],net_profit:[],ebitda:[],pe:[],pbv:[],total_debt:[],net_debt:[]}};;
// ΔΙΑΝΟΜΕΣ = μέγεθος ΧΡΗΣΗΣ. Δεν υπάρχει «μέρισμα εξαμήνου»: το RATIOS H1 κουβαλά την
// ετήσια τιμή στη στήλη της χρήσης και 0 στο τρέχον εξάμηνο. Άρα στην όψη 6μήνου τόσο η
// κάρτα «Χρηματικές διανομές» όσο και οι δείκτες dps/dy/payout διαβάζουν ΠΑΝΤΑ την ετήσια
// βάση — αλλιώς η κάρτα κόβεται σε 1 γραμμή και το DPS δείχνει ψευδές «0,00 €».
const DIV_SLUGS_UI=['dps','dy','payout'];
// §185 — η 6μηνη εγγραφή της ίδιας εταιρείας. Στήλες 6Μ εμφανίζονται ΜΟΝΟ όταν το 6μηνο
// είναι νεότερο από την τελευταία χρήση (π.χ. 6Μ 2026 μετά τη χρήση 2025)· ένα 6μηνο της
// ίδιας χρονιάς με την τελευταία χρήση είναι ήδη παλιό και δεν προστίθεται.
const AXI=(function(){ try{ var _L=(window.AXION&&window.AXION.companies&&window.AXION.companies.interim)||[];
  return (AX&&_L.find(function(c){return c.tk===AX.tk;}))||null; }catch(e){ return null; } })();
const SD=function(d){ return String(d==null?'':d).replace(/\/(\d\d)(\d\d)$/,'/<span class="cy">$1</span>$2'); };
const HAS6=!!(AXI && !AXI.nodata && AXI.latest && AXI.latest.idx!=null && AX && AX.latest &&
  Number(AXI.latest.period)>Number(AX.latest.period));
const IS_BANK = !!(AX && AX.s==='Τράπεζες');   // banks: EBITDA-family δεν εφαρμόζεται
const NA_RATIO  = new Set(['ebitdam','evebitda','gm','cogs','selling','dio']);
if(IS_BANK){var _ebl=document.getElementById('eb-leg'); if(_ebl)_ebl.innerHTML='<i style="background:#3f9e6a"></i>'+L('co.leg.ppi');}  // τράπεζες: 2η γραμμή = Κέρδη προ προβλέψεων (PPI) αντί EBITDA
// Τράπεζες: δεν έχουν εταιρικό δανεισμό (§5.1) → οι δύο στήλες δανεισμού αντικαθίστανται
// από τα δικά τους μεγέθη ισολογισμού. Το Ταμείο μένει Ταμείο.
const BANK_SWAP={ebitda:{k:'ppi',l:'co.m.ppi'},total_debt:{k:'loans',l:'co.m.loans'},net_debt:{k:'deposits',l:'co.m.deposits'}};
const fMil=v=>{if(v==null||isNaN(v))return '—';const m=v/1e6,a=Math.abs(m),d=a<100?2:a<1000?1:0;return m.toLocaleString(LOC(),{minimumFractionDigits:d,maximumFractionDigits:d});};
const fX=v=>(v==null||(typeof v==='number'&&isNaN(v)))?'—':v.toLocaleString(LOC(),{minimumFractionDigits:1,maximumFractionDigits:1});
const EURSUF=()=>EN()?' €M':' εκ.€';

document.getElementById('co-name').textContent=company.name;
// Λογότυπο εταιρείας (μετά το όνομα, με κάθετο διαχωριστικό)· fallback: κρύβεται αν λείπει.
// §134 — στις 140 στατικές σελίδες το src/width/height τα ψήνει η γέφυρα και το μπλοκ εδώ
// ΔΕΝ τρέχει (ο έλεγχος getAttribute('src')). Μένει ζωντανό μόνο για το /company/?tk=.
// §201 — ζητά πρώτα .webp (όπως η γέφυρα) και .png μόνο ως εφεδρεία (7 λογότυπα χωρίς webp).
window.AX_LOGO={"ALWN":1,"ΑΣΤΑΚ":2,"ΑΝΔΡΟ":3,"ΑΤΡΑΣΤ":4,"ΑΛΦΑ":5,"AEM":6,"ΑΣΚΟ":7,"ΑΤΤΙΚΑ":8,"ACAG":9,"ΟΤΟΕΛ":10,"ΑΒΕ":11,"BYLOT":12,"ΜΠΡΙΚ":13,"CENER":14,"ΣΕΝΤΡ":15,"CNLCAP":16,"ΕΕΕ":17,"ΣΠΙ":18,"CREDIA":19,"DIMAND":20,"ΝΤΟΤΣΟΦΤ":21,"ΕΧΑΕ":22,"ΕΧ":23,"ΦΛΕΞΟ":24,"ΦΡΛΚ":25,"ΦΡΙΓΟ":26,"ΕΛΠΕ":27,"ΙΝΤΕΚ":28,"ΜΠΕΛΑ":29,"ΛΑΜΔΑ":30,"ΛΟΓΟΣ":31,"ΛΟΥΛΗ":32,"ΜΑΣΤΙΧΑ":33,"MTLN":34,"ΜΕΒΑ":35,"ΜΙΓ":36,"ΟΡΙΛΙΝΑ":37,"ΠΕΡΦ":38,"ΠΡΕΜΙΑ":39,"ΠΡΟΦ":40,"ΚΟΥΑΛ":41,"ΚΟΥΕΣ":42,"REALCONS":43,"SOFTWEB":44,"ΣΠΕΙΣ":45,"TITC":46,"ΤΡΕΣΤΑΤΕΣ":47,"ΤΡΑΣΤΟΡ":48,"ΒΙΟΣΚ":49,"ΒΙΝΤΑ":50,"ΒΙΟ":51,"ΑΒΑΞ":52,"ΣΠΥΡ":53,"ΚΟΡΔΕ":54,"ΑΡΑΙΓ":55,"AKTR":56,"ΑΛΜΥ":57,"ΛΑΒΙ":59,"ΑΔΜΗΕ":60,"ΛΕΒΚ":61,"ΜΑΘΙΟ":62,"ΑΤΕΚ":63,"ΜΕΝΤΙ":64,"ΜΙΝ":65,"ΒΙΟΚΑ":66,"ΒΙΟΤ":67,"ΒΟΣΥΣ":68,"ΓΕΚΤΕΡΝΑ":69,"ΓΕΒΚΑ":70,"ΣΑΡ":71,"ΔΑΙΟΣ":72,"ΔΕΗ":73,"ΔΑΑ":74,"ΔΟΜΙΚ":75,"ΠΑΙΡ":76,"ΕΒΡΟΦ":77,"ΕΤΕ":78,"ΕΚΤΕΡ":79,"ΕΛΣΤΡ":80,"ΕΛΧΑ":81,"ΕΛΒΕ":82,"ΜΟΥΖΚ":83,"ΕΛΙΝ":84,"ΕΛΛΑΚΤΩΡ":85,"ΙΚΤΙΝ":86,"ΕΛΤΟΝ":87,"ΜΟΤΟ":88,"ΑΑΑΚ":89,"ΛΑΜΨΑ":90,"ΕΥΑΠΣ":91,"ΕΥΔΑΠ":92,"EIS":93,"EVR":94,"ΙΑΤΡ":95,"ΙΛΥΔΑ":96,"ΞΥΛΚ":97,"ΙΝΛΙΦ":98,"ΙΝΤΕΤ":99,"ΙΝΤΚΑ":100,"ΚΑΡΕΛ":101,"ΝΑΥΠ":102,"ΚΡΙ":103,"ΣΑΡΑΝ":104,"ΛΑΝΑΚ":105,"ΜΟΗ":106,"ΜΠΛΕΚΕΔΡΟΣ":107,"NOVAL":108,"ΝΤΟΠΛΕΡ":109,"ΚΕΚΡ":110,"ONYX":111,"ΟΠΤΡΟΝ":112,"ΟΛΘ":113,"ΟΛΠ":114,"ΟΤΕ":115,"ΔΡΟΜΕ":116,"ΠΑΠ":117,"ΠΕΤΡΟ":118,"ΠΛΑΘ":119,"ΠΛΑΚΡ":120,"ΠΡΟΝΤΕΑ":121,"ΠΡΔ":122,"ΡΕΒΟΙΛ":123,"ΣΙΔΜΑ":124,"ΤΖΚΑ":125,"ΤΕΝΕΡΓΑ":126,"ΕΥΡΩΒ":127,"OPTIMA":128,"ΠΕΙΡ":129,"ΦΑΙΣ":130,"ΝΑΚΑΣ":131,"ΦΟΥΝΤΛ":132,"ΧΑΙΔΕ":133,"QLCO":134,"ADPS":135,"ΟΛΥΜΠ":136,"YKNOT":137,"SB":138,"SBLK":139,"VRLS":140,"CMFC":141,"METK":142};
(function(){try{var lw=document.getElementById('co-logo-wrap'),lg=document.getElementById('co-logo'),hr=document.getElementById('co-hrule');var code=lw&&lg&&company&&company.ticker&&window.AX_LOGO[company.ticker];if(code&&!lg.getAttribute('src')){lg.onload=function(){lw.hidden=false;if(hr)hr.hidden=false;};lg.onerror=function(){if(!lg._png){lg._png=1;lg.src='/assets/logos/'+code+'.png';return;}lw.hidden=true;if(hr)hr.hidden=true;};lg.alt=company.name||'';lg.src='/assets/logos/'+code+'.webp';}}catch(e){}})();
// (ο τίτλος τίθεται στο §73 παρακάτω — και για τη γενική περίπτωση χωρίς εταιρεία)
if(!(company&&company.name&&company.name!=='—')) document.title='Axion Metrics';
document.getElementById('co-ticker').textContent=company.ticker;
document.getElementById('co-eur').textContent=company.euronext_name+' · Euronext Athens';
// §79 — ΕΣΩΤΕΡΙΚΗ ΣΥΝΔΕΣΗ. Ο κλάδος ήταν σκέτο κείμενο· τώρα κάθε μία από τις 133
// σελίδες δίνει έναν σύνδεσμο στη σελίδα του κλάδου της, χτίζοντας ιεραρχία θέματος
// (εταιρεία → κλάδος) αντί για 133 σελίδες που δείχνουν μόνο η μία στην άλλη.
(function(){var _e=document.getElementById('co-sector'), _s=company.sector;
 var _u=null; try{ _u=(typeof AX_KLADOS==='function')?AX_KLADOS(_s):null; }catch(x){}
 if(_u) _e.innerHTML='<a href="'+_u.replace('https://www.axionmetrics.gr','')+'">'+
        _s.replace(/&/g,'&amp;').replace(/</g,'&lt;')+'</a>';
 else _e.textContent=_s;})();
// §73 — SEO ΑΝΑ ΕΤΑΙΡΕΙΑ. Τρία πράγματα: canonical/og, ο ΤΙΤΛΟΣ, και η ΠΕΡΙΛΗΨΗ σε ορατό
// κείμενο. Τεκμήριο από το Search Console (16/09/2026): κάθε ερώτημα που μας φέρνει είναι
// «όνομα εταιρείας + μετοχή/μέρισμα» (πρδ μετοχη · ευαθ μετοχη · αραιγ μετοχη · ιντκα
// μερισμα), ενώ 242 εμφανίσεις έδωσαν 4 κλικ σε μέσες θέσεις 5-8 — δηλαδή ο τίτλος δεν
// απαντούσε στο ερώτημα. Και 89 από τις 133 εμφανίζονταν ΜΟΝΟ με λατινικό όνομα, ενώ ο
// κόσμος πληκτρολογεί ελληνικά.
(function(){try{
  if(!company||!company.name||company.name==='—') return;
  var C=company;
  // §75 — κανονική διεύθυνση = η στατική σελίδα. Το `?tk=` μένει ζωντανό αλλά δηλώνει
  // ότι η κανονική του έκδοση είναι η /etaireia/<slug>/, ώστε να μη μετρηθούν δύο φορές.
  // §77 — ΤΟ `company` ΔΕΝ ΕΧΕΙ `slug`. Το slug ζει στο AXION.companies (ανά ticker), όχι στο
  // αντικείμενο της τρέχουσας εταιρείας· το `C.slug` ήταν πάντα undefined, άρα ΟΛΕΣ οι σελίδες
  // —μαζί και οι 133 στατικές— έγραφαν στο canonical το `/company/?tk=…`, δηλαδή ακριβώς τις
  // διευθύνσεις που το Search Console αρνείται να δει. Μοναδική πηγή: η AX_CO του i18n.js.
  var _path=(typeof AX_CO==='function') ? AX_CO(C.ticker)
          : ('/company/?tk='+encodeURIComponent(C.ticker));
  var url='https://www.axionmetrics.gr'+_path;
  var li=(C.latest&&C.latest.idx!=null)?C.latest.idx:((C.years&&C.years.length-1)||0);
  var M=C.metrics||{};
  var num=function(v){return (typeof v==='number'&&!isNaN(v))?v:null;};
  var at=function(k){var a=M[k]; return (a&&a.length>li)?num(a[li]):null;};
  var eur=function(v){return fMil(v)+(EN()?'m':' εκατ. €');};
  var x1=function(v){return (v==null||isNaN(v))?null:v.toLocaleString(LOC(),{minimumFractionDigits:1,maximumFractionDigits:1});};
  // ΠΡΟΣΟΧΗ: ένωση σε επίπεδο στοιχείων. Regex πάνω στο τελικό κείμενο σπάει στο ελληνικό
  // δεκαδικό κόμμα («83,89 εκατ. €») και αφήνει προτάσεις χωρίς «και».
  var join=function(a){ if(a.length<2) return a[0]||''; return a.slice(0,-1).join(', ')+(EN()?' and ':' και ')+a[a.length-1]; };

  // ── ΟΝΟΜΑ 2: η ελληνική (ή λατινική) επωνυμία, καθαρισμένη από νομική μορφή και
  //    περιγραφικό προσδιορισμό, κομμένη σε ΑΚΕΡΑΙΕΣ ΛΕΞΕΙΣ έως 30 χαρακτήρες — αλλιώς
  //    τίτλοι σαν «ΕΒΡΟΦΑΡΜΑ ΒΙΟΜΗΧΑΝΙΑ ΓΑΛΑΚΤΟΣ ΑΝΩΝΥΜΗ ΒΙΟΜΗΧΑΝΙΚΗ & ΕΜΠΟΡΙΚΗ ΕΤΑΙΡΕΙΑ».
  var LEG=/\s*(ΑΝΩΝΥΜ[ΗΟ]Σ?\s+ΕΤΑΙΡ[ΕΙ]?[ΙΑ]Α?|Α\.?Ε\.?Ε\.?Α\.?Π|Α\.?Ε\.?Ε\.?Χ|Α\.?Ε\.?Π\.?Ε\.?Υ|Α\.?Ε\.?Β\.?Ε|Α\.?Β\.?Ε\.?Ε|Α\.?Ξ\.?Ε|Α\.?Ε|S\.?A|PLC|LTD|A\.?G|N\.?V)\.?\s*$/i;
  // γενικοί όροι που μένουν κρεμασμένοι μετά την κοπή («ΕΛΒΑΛΧΑΛΚΟΡ ΕΛΛΗΝΙΚΗ»)
  // ΠΡΟΣΟΧΗ: το \w της JS είναι ΜΟΝΟ ASCII — δεν πιάνει ελληνικές καταλήξεις. Χρήση \S*.
  var GEN=/^(ΕΛΛΗΝΙΚ\S*|ΒΙΟΜΗΧΑΝΙ\S*|ΕΜΠΟΡΙΚ\S*|ΓΕΝΙΚ[ΗΟ]Σ?|ΑΝΩΝΥΜ\S*|ΕΤΑΙΡ\S*|ΤΕΧΝΙΚ\S*|ΝΑΥΤΙΛΙΑΚ\S*|ΞΕΝΟΔΟΧΕΙΑΚ\S*|ΕΙΣΑΓΩΓΙΚ\S*|ΚΑΙ|&)$/i;
  function norm(t){ return String(t||'').toUpperCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^A-ZΑ-Ω0-9]/g,''); }
  function alt2(){
    var t=String(C.euronext_name||'').split(/\s+[-–—]\s+/)[0].trim();
    t=t.replace(LEG,'').replace(LEG,'').replace(/[\s,.·]+$/,'').trim();
    if(!t) return '';
    var w=t.split(/\s+/), out=w[0];
    for(var k=1;k<w.length;k++){ if((out+' '+w[k]).length>30) break; out+=' '+w[k]; }
    var ww=out.split(/\s+/);
    while(ww.length>1 && GEN.test(ww[ww.length-1])) ww.pop();
    out=ww.join(' ');
    var a=norm(out), b=norm(C.name);
    return (a && a!==b && b.indexOf(a)<0 && a.indexOf(b)<0) ? out : '';
  }
  var A=alt2(), both=C.name+(A?' / '+A:'');

  // ── ΤΙΤΛΟΣ: και τα δύο ονόματα, το σύμβολο, και οι λέξεις που όντως πληκτρολογούνται.
  var ttl = EN()
    ? both+' ('+C.ticker+') — share, results & financial ratios'
    : both+' ('+C.ticker+') — μετοχή, αποτελέσματα & αριθμοδείκτες';

  // ── ΜΕΓΕΘΗ ΤΕΛΕΥΤΑΙΑΣ ΠΕΡΙΟΔΟΥ
  var per=(C.latest&&C.latest.period)||'';
  var pw = EN() ? ('in FY '+per) : ('τη χρήση '+per);
  var rev=at('revenue'), np=at('net_profit'), eb=at('ebitda'), ppi=at('ppi'), nd=at('net_debt');
  var cur=C.current||{}, mc=num(cur.mcap)!=null?num(cur.mcap):at('mcap');
  var _pe=num(cur.pe);
  var pe=(_pe!=null&&_pe>0)?x1(_pe):null;      // αρνητικό P/E (ζημιογόνος) δεν πληροφορεί — έξω
  var pbv=x1(num(cur.pbv));

  var sec=(C.sector&&C.sector!=='—')?C.sector:'';
  var P=[];
  P.push(EN()
    ? (C.name+' ('+C.ticker+') is listed on the Athens Stock Exchange'+(sec?', in the '+sec+' sector':'')+'.')
    : ('Η '+C.name+' ('+C.ticker+') είναι εισηγμένη στο Χρηματιστήριο Αθηνών'+(sec?', στον κλάδο '+sec:'')+'.'));

  // Τράπεζες: δεν ορίζεται EBITDA (§5.1) — στη θέση του τα κέρδη προ προβλέψεων.
  var f=[];
  if(rev!=null) f.push(EN()?('revenue of '+eur(rev)):((IS_BANK?'τα συνολικά έσοδα ':'ο κύκλος εργασιών ')+eur(rev)));
  if(!IS_BANK&&eb!=null) f.push(EN()?('EBITDA of '+eur(eb)):('το EBITDA '+eur(eb)));
  if(IS_BANK&&ppi!=null) f.push(EN()?('pre-provision income of '+eur(ppi)):('τα κέρδη προ προβλέψεων '+eur(ppi)));
  // ζημιά: γράφεται ως ζημιά, όχι ως «καθαρά κέρδη -3,26»
  if(np!=null) f.push(np<0 ? (EN()?('a net loss of '+eur(-np)):('ζημιές '+eur(-np)))
                           : (EN()?('net profit of '+eur(np)):('τα καθαρά κέρδη '+eur(np))));
  if(f.length){
    // το «ήταν» μπαίνει μετά το ΠΡΩΤΟ στοιχείο, όποιο κι αν είναι αυτό
    var f2=f.slice(); if(!EN()){ var m0=f2[0].match(/^(.*?)(\s[^\s]*\d.*)$/); if(m0) f2[0]=m0[1]+' ήταν'+m0[2]; }
    P.push(EN() ? ('The company reported '+join(f2)+' '+pw+'.')
                : (pw.charAt(0).toUpperCase()+pw.slice(1)+' '+join(f2)+'.'));
  }
  if(!IS_BANK&&nd!=null) P.push(nd<0
    ? (EN()?('It holds net cash of '+eur(-nd)+'.'):('Διαθέτει καθαρό ταμείο '+eur(-nd)+'.'))
    : (EN()?('Net debt stood at '+eur(nd)+'.'):('Ο καθαρός δανεισμός διαμορφώθηκε σε '+eur(nd)+'.')));

  var v=[];
  if(mc!=null) v.push(EN()?('a market capitalisation of '+eur(mc)):('κεφαλαιοποίηση '+eur(mc)));
  if(pe) v.push(EN()?('a P/E of '+pe):('δείκτη P/E '+pe));
  if(pbv) v.push(EN()?('a P/BV of '+pbv):('δείκτη P/BV '+pbv));
  if(v.length) P.push(EN()
    ? ('At the latest closing price it has '+join(v)+'.')
    : ('Με βάση την τελευταία τιμή κλεισίματος έχει '+join(v)+'.'));

  P.push(EN()
    ? 'This page covers the company’s financial results and financial statements, 26 financial ratios benchmarked against its sector, the trajectory of its figures since 2020, its main shareholders, subsidiaries, dividends and corporate events.'
    : 'Στη σελίδα θα βρείτε τα οικονομικά αποτελέσματα και τις οικονομικές καταστάσεις της εταιρείας, 26 αριθμοδείκτες με σύγκριση έναντι του κλάδου, την τροχιά των μεγεθών από το 2020, τους βασικούς μετόχους, τις θυγατρικές, τα μερίσματα και τα εταιρικά γεγονότα.');
  var summary=P.join(' ');

  // §75 — ΜΙΑ ΠΗΓΗ ΓΙΑ ΤΟ ΕΛΛΗΝΙΚΟ ΚΕΙΜΕΝΟ. Η γέφυρα το χτίζει (co_seo) και το στέλνει
  // στο data.js ως `seo`· το ίδιο κείμενο ψήνεται και στις στατικές σελίδες. Έτσι ό,τι
  // βλέπει ο Google χωρίς JavaScript ταυτίζεται με ό,τι βλέπει μετά.
  // Τα ΑΓΓΛΙΚΑ μένουν εδώ: η αγγλική όψη δεν έχει δική της διεύθυνση, άρα δεν είναι
  // περιουσιακό στοιχείο αναζήτησης — είναι διευκόλυνση οθόνης.
  var _S=(!EN() && C.seo && C.seo.summary) ? C.seo : null;
  if(_S) summary=_S.summary;

  // ── META DESCRIPTION: πιο σφιχτή από την περίληψη, με τους ίδιους όρους.
  var dbits=[];
  if(rev!=null) dbits.push((EN()?'revenue ':'κύκλος εργασιών ')+eur(rev));
  if(np!=null)  dbits.push(np<0 ? ((EN()?'net loss ':'ζημιές ')+eur(-np)) : ((EN()?'net profit ':'καθαρά κέρδη ')+eur(np)));
  if(pe) dbits.push('P/E '+pe);
  if(pbv) dbits.push('P/BV '+pbv);
  var desc = EN()
    ? (both+' ('+C.ticker+'): financial results '+per+(dbits.length?' — '+dbits.join(', '):'')+'. Ratios, dividends, shareholders and sector comparison'+(sec?' in '+sec:'')+'.')
    : (both+' ('+C.ticker+'): οικονομικά αποτελέσματα '+per+(dbits.length?' — '+dbits.join(', '):'')+'. Αριθμοδείκτες, μερίσματα, μέτοχοι και σύγκριση με τον κλάδο'+(sec?' '+sec:'')+'.');

  if(_S){ ttl=_S.title; desc=_S.desc; }
  // η αποτίμηση μπαίνει ΜΟΝΟ στην απόδοση (το current.js αλλάζει κάθε βράδυ· αν ψηνόταν
  // στο HTML, το νυχτερινό Action θα ξανάγραφε 133 αρχεία καθημερινά)
  if(_S && v.length){
    var _t=' Στη σελίδα θα βρείτε', _i=summary.indexOf(_t);
    var _vs='Με βάση την τελευταία τιμή κλεισίματος έχει '+join(v)+'.';
    summary = (_i>0) ? (summary.slice(0,_i)+' '+_vs+summary.slice(_i)) : (summary+' '+_vs);
  }
  function S(sel,a,val){var e=document.querySelector(sel); if(e) e.setAttribute(a,val);}
  document.title=ttl;
  // §127 — ΤΟ ΚΕΝΟ `/company/` ΔΕΝ ΑΠΟΚΗΡΥΣΣΕΙ ΤΟΝ ΕΑΥΤΟ ΤΟΥ.
  // Τεκμήριο (30/09/2026): φορτώνοντας το σκέτο `/company/` το JS έγραφε canonical
  // `/etaireia/allwyn/` — δηλαδή η σελίδα, που ΕΙΝΑΙ μέσα στο sitemap, δήλωνε στη
  // Google «είμαι αντίγραφο της πρώτης εταιρείας του καταλόγου». Η επανεγγραφή είναι
  // σωστή μόνο όταν η οντότητα έχει δηλωθεί ρητά: ψημένο AX_TK (σελίδες /etaireia/)
  // ή ?tk= στη διεύθυνση (εκεί η συγχώνευση στην καθαρή διεύθυνση είναι το ζητούμενο).
  var _explicit = !!window.AX_TK || !!new URLSearchParams(location.search).get('tk');
  if(_explicit){
    var cn=document.querySelector('link[rel="canonical"]'); if(cn) cn.setAttribute('href',url);
  }
  S('meta[name="description"]','content',desc);
  S('meta[property="og:description"]','content',desc);
  S('meta[name="twitter:description"]','content',desc);
  S('meta[property="og:title"]','content',ttl);
  S('meta[name="twitter:title"]','content',ttl);
  if(_explicit) S('meta[property="og:url"]','content',url);
  function fill(){var e=document.getElementById('co-summary'); if(e) e.textContent=summary;}
  if(document.getElementById('co-summary')) fill(); else document.addEventListener('DOMContentLoaded',fill);
}catch(e){}})();
// Δυναμική ετικέτα «ΕΤΗΣΙΑ/ΕΞΑΜΗΝΟ + περίοδος» + σημείωση + χρωματισμός block/toggle ανά βάση
(function(){
  var per=company.latest&&company.latest.period;
  var blabel=L('co.basis.annual');
  var yh=document.getElementById('yr-h'); if(yh) yh.textContent=(per?(blabel+' '+per):blabel);
  var yn=document.getElementById('yr-note');
  if(yn&&per){ yn.textContent='('+L('co.latest.note')+')'; yn.hidden=false; }
})();
(function(){
  // ΕΝΙΑΙΟ «Εκτός κάλυψης» — frozen (UPDATED=NO): ΕΝΑ badge (#co-status) + ΜΙΑ υποσημείωση (#co-corp-banner)
  var frozen=!!(AX&&AX.calculated===false);
  var pill=document.getElementById('co-status'),
      ban=document.getElementById('co-corp-banner'),
      oldban=document.getElementById('co-banner');
  if(oldban) oldban.hidden=true;
  var ech=(AX&&AX.echange)||null;
  if(frozen){
    var e=(AX&&AX.enote)||null, txt=e?(e[curLang()]||e.el||''):'';
    var icon='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="7" y="6" width="3.5" height="12" rx="1"/><rect x="13.5" y="6" width="3.5" height="12" rx="1"/></svg>';
    var lab=L('co.entity.badge');
    if(pill){ pill.className='tbadge t-frozen'; pill.innerHTML=icon+'<span>'+lab+'</span>'; pill.hidden=false; }
    if(ban){ ban.className='tbanner t-frozen';
      ban.innerHTML=icon+'<span><b>'+lab+'</b>'+(txt?(' · <span class="thin">'+txt+'</span>'):'')+'</span>';
      ban.hidden=false; }
    return;
  }
  // Διακριτική «Αλλαγή οντότητας» — συγκρισιμότητα (ΟΧΙ «Εκτός κάλυψης»): αμπέρ, όχι δραματικό
  if(ech && ech.year){
    var det=(ech[curLang()]||ech.el||'');
    var head=L('co.echange.text').replace('{year}', ech.year);
    var lab2=L('co.echange.badge');
    var ic2='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"><path d="M12 4l9 16H3z"/><path d="M12 10v5" stroke-linecap="round"/><circle cx="12" cy="18" r=".6" fill="currentColor" stroke="none"/></svg>';
    if(pill){ pill.className='tbadge t-caution'; pill.innerHTML=ic2+'<span>'+lab2+'</span>'; pill.hidden=false; }
    if(ban){ ban.className='tbanner t-caution';
      ban.innerHTML=ic2+'<span><b>'+head+'</b>'+(det?(' <span class="thin">'+det+'</span>'):'')+'</span>';
      ban.hidden=false; }
    return;
  }
  if(pill)pill.hidden=true; if(ban)ban.hidden=true;
})();

// «Ελλιπές 6μηνο» — σήμανση όταν <2 εξάμηνα (μόνο στην προβολή 6μήνου)
(function(){
  var pill=document.getElementById('co-h1'), ban=document.getElementById('co-h1-banner');
  var partial=!!(AX&&AXBASIS==='interim'&&AX.interimPartial);
  if(!partial){ if(pill)pill.hidden=true; if(ban)ban.hidden=true; return; }
  var n=(AX&&AX.h1n)||1;
  var icon='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4.5" width="18" height="16" rx="2"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/></svg>';
  if(pill){ pill.className='tbadge t-prov'; pill.innerHTML='<b>'+n+'</b>/2 '+L('co.h1.pill'); pill.hidden=false; }
  if(ban){ ban.className='tbanner t-prov';
    ban.innerHTML=icon+'<span><b>'+n+' '+L('co.h1.of')+'</b> <span class="thin">'+L('co.h1.detail')+'</span></span>';
    ban.hidden=false; }
})();

// «Αλλαγή οντότητας / εταιρική πράξη» — badge + υποσημείωση, τροφοδοτείται από τον master (INDEX ΕΠΙΧΕΙΡΗΣΕΩΝ)
// (Η «αλλαγή οντότητας» ενοποιήθηκε στο «Εκτός κάλυψης» παραπάνω) — κρύψε το παλιό corp pill.
(function(){ var p=document.getElementById('co-corp'); if(p)p.hidden=true; })();

const li=(company.latest && company.latest.idx!=null) ? company.latest.idx : company.years.length-1;
// §45 — κατάσταση EBITDA για την τελευταία χρήση.
// ΕΝΑ κατώφλι (5 %, απόφαση χρήστη): κάτω από αυτό δείχνουμε ΕΝΑ νούμερο — το δημοσιευμένο —
// και **καμία** λωρίδα εξήγησης. Δεν χρειάζεται δεύτερο κατώφλι για το κείμενο: όταν ο
// αναγνώστης βλέπει έναν αριθμό, δεν υπάρχει διαφορά να εξηγηθεί.
const EB_TOL=0.05;
function EB_WHY(k){
  const t=String(k||'').toLowerCase();
  if(t.indexOf('αποτιμ')>=0) return 'co.eb.w.val';
  if(t.indexOf('προσαρμ')>=0) return 'co.eb.w.adj';
  if(t.indexOf('μετάλλ')>=0||t.indexOf('a-ebitda')>=0) return 'co.eb.w.met';
  // §61 — 101 ΚΑΡΕΛΙΑΣ: το EBITDA της ορίζεται «προ συναλλαγματικών διαφορών», που κατά
  // τον §26.7.2 μένουν ΜΕΣΑ στο δικό μας. Χωρίς αυτόν τον κλάδο η λωρίδα θα έπεφτε στο
  // γενικό «άλλος ορισμός» — αληθές αλλά άχρηστο, ενώ ο λόγος είναι συγκεκριμένος.
  if(t.indexOf('συναλλαγμ')>=0) return 'co.eb.w.fx';
  return 'co.eb.w.gen';
}
/* ══ §185 — «ΜΕΓΕΘΗ ΠΕΡΙΟΔΟΥ» ════════════════════════════════════════════════════
   Αντικαθιστά τη σκούρα ζώνη «Ετήσια/Τρέχοντα μεγέθη». ΟΛΕΣ οι δημοσιευμένες περίοδοι του
   έτους δίπλα-δίπλα: Ετήσια (τελευταία χρήση) · [3Μ] · 6Μ · [9Μ]. Σε ετήσιο και 6μηνο, δεύτερη
   στήλη με P/E · P/BV · κεφαλαιοποίηση στην τρέχουσα τιμή (AXION_CURRENT).
   ΙΔΙΟΙ κανόνες με την παλιά ζώνη: EBITDA κατά §45 (ένα νούμερο εντός ανοχής 5%, αλλιώς το
   δημοσιευμένο με υποσημείωση), τράπεζες κατά BANK_SWAP, υποσημειώσεις κατά §68 (δυναμική
   αρίθμηση), μεταβολή κατά §76 (|βάση|, φορά από τη Δ).
   3Μ / 9Μ: έτοιμες στήλες· εμφανίζονται μόνο αν υπάρχει AX.quarters.q1 / .q3 με μορφή
   {y:<έτος>, m:{revenue:..,…}, p:{revenue:..,…}, px:'31/03/2026'} (p = ίδια περίοδος πέρσι). */
(function(){
  const host=document.getElementById('per'); if(!host) return;
  const has=v=>typeof v==='number'&&!isNaN(v);
  const cur=company.current;
  const fmtd=s=>{const m=/^(\d{4})-(\d{2})-(\d{2})$/.exec(s||'');return m?`${m[3]}/${m[2]}/${m[1]}`:(s||'');};
  const curD=cur&&cur.date?fmtd(cur.date):'';
  const hasCur=!!(cur&&(has(cur.mcap)||has(cur.pe)||has(cur.pbv)));
  function ebState(M,i){
    const own=(M.ebitda||[])[i];
    if(!('ebitda_rep' in M)) return has(own)?{s:'legacy',own:own}:{s:'na'};
    const rep=(M.ebitda_rep||[])[i], kind=(M.ebitda_kind||[])[i]||null, _a=(M.ebitda_adj||[])[i], adj=has(_a)?_a:null;
    if(!has(own)&&!has(rep)) return {s:'na',adj:adj};
    if(!has(rep)) return {s:'own',own:own,adj:adj};
    if(!has(own)) return {s:'reponly',rep:rep,kind:kind,adj:adj};
    const d=Math.abs(own-rep)/Math.max(Math.abs(rep),1);
    return d<=EB_TOL?{s:'same',rep:rep,own:own,kind:kind,adj:adj}:{s:'diff',rep:rep,own:own,kind:kind,adj:adj};
  }
  // περίοδοι-στήλες
  const PS=[];
  const fromSeries=(C,lab,px,now)=>{ const i=(C.latest&&C.latest.idx!=null)?C.latest.idx:C.years.length-1;
    const M=C.metrics||{}; return {lab:lab,y:C.years[i],px:px,now:now,
      v:k=>(M[k]||[])[i], p:k=>(M[k]||[])[i-1], M:M, i:i, series:true}; };
  const ya=AX&&AX.latest?AX.latest.period:'';
  PS.push(fromSeries(AX,L('co.per.annual').replace('{y}',ya),'31/12/'+ya,
    hasCur?{mcap:cur.mcap,pe:cur.pe,pbv:cur.pbv}:null));
  // §190 — Τα 3Μ/9Μ έρχονται από τη γέφυρα ως {y, m:{…}, p:{…}} (p = ίδια περίοδος πέρσι).
  // Περνούν από την ΙΔΙΑ λογική με το ετήσιο/6μηνο: φτιάχνεται μια σειρά δύο θέσεων [πέρσι, φέτος]
  // ώστε το EBITDA να ακολουθεί το §45 (δημοσιευμένο/δικό μας + υποσημείωση) και τα καθαρά
  // κέρδη την υποσημείωση μειοψηφιών. Χωρίς στήλη «Τιμές»: στο τρίμηνο δεν υπάρχει αποτίμηση.
  // Εμφανίζονται μόνο όταν το έτος τους είναι νεότερο από την τελευταία χρήση (όπως το 6μηνο).
  const Q=(AX&&AX.quarters)||{};
  const fromQ=(q,key)=>{ const m=q.m||{}, p=q.p||{}, M={};
    ['ebitda','ebitda_rep','ebitda_kind','pat'].forEach(k=>{ M[k]=[(k in p)?p[k]:null,(k in m)?m[k]:null]; });
    return {lab:L(key).replace('{y}',q.y),y:q.y,px:'',now:null,
      v:k=>m[k], p:k=>p[k], M:M, i:1, series:true, opt:true}; };
  const qOk=q=>!!(q&&q.m&&Number(q.y)>Number(ya));
  const HASQ=qOk(Q.q1)||qOk(Q.q3);
  if(qOk(Q.q1)) PS.push(fromQ(Q.q1,'co.per.q1'));
  if(HAS6) PS.push(fromSeries(AXI,L('co.per.h1').replace('{y}',AXI.latest.period),'30/06/'+AXI.latest.period,
    hasCur?{mcap:cur.mcap,pe:(cur.pe_i!=null?cur.pe_i:null),pbv:(cur.pbv_i!=null?cur.pbv_i:null)}:null));
  if(qOk(Q.q3)) PS.push(fromQ(Q.q3,'co.per.q3'));
  PS.forEach((P,j)=>{ P.cls=j===0?'ya':(P.opt?'q':'h1'); });
  // γραμμές
  const R=[
    [{k:'revenue',d:true,up:true},{k:'ebitda',d:true,up:true},{k:'net_profit',d:true,up:true}],
    [{k:'total_debt'},{k:'cash'},{k:'net_debt'}],
    [{k:'mcap',now:true},{k:'pe',x:true,now:true},{k:'pbv',x:true,now:true}]
  ];
  // υποσημειώσεις (§68: δυναμική αρίθμηση, μία φορά κάθε κείμενο)
  const FNS=[]; const fnIdx=html=>{ let n=FNS.indexOf(html); if(n<0){FNS.push(html); n=FNS.length-1;} return n+1; };
  const sup=n=>`<sup class="fnm">${n}</sup>`;
  const dl=(v,p,up)=>{
    if(!has(v)||!has(p)||!p) return '<i class="d n">(—)</i>';
    const d=(v-p)/Math.abs(p)*100, good=up?d>=0:d<0;
    return `<i class="d ${good?'u':'w'}">(${d>=0?'+':'−'}${Math.abs(d).toLocaleString(LOC(),{minimumFractionDigits:1,maximumFractionDigits:1})}%)</i>`;
  };
  const val=(v,x)=>has(v)?(x?fX(v):fMil(v)):'—';
  function cell(P,r){
    const sw=IS_BANK?BANK_SWAP[r.k]:null, k=sw?sw.k:r.k;
    let v=P.v(k), pv=P.p(k), mark='';
    // §190 — 3Μ/9Μ: όταν το δελτίο δίνει μόνο τα κέρδη μετά φόρων του ομίλου (όχι τα αναλογούντα
    // στη μητρική), δείχνεται αυτό το νούμερο ΜΕ υποσημείωση — ποτέ σιωπηλά στη θέση του άλλου.
    if(r.k==='net_profit'&&P.opt&&!has(v)&&has(P.v('pat'))){
      v=P.v('pat'); pv=P.p('pat');
      mark=sup(fnIdx(L('co.per.fnp').replace('{p}',P.lab)+L('co.np.s.patq')));
    }
    if(r.k==='ebitda'&&!sw&&P.series){
      const st=ebState(P.M,P.i);
      if(st.s==='na'){ v=null; }
      else{
        v=(st.s==='same'||st.s==='diff'||st.s==='reponly')?st.rep:st.own;
        const ser=(v===st.rep)?(P.M.ebitda_rep||[]):(P.M.ebitda||[]); pv=ser[P.i-1];
        const parts=[];
        if(!(st.s==='legacy'||st.s==='same')){
          if(st.s==='reponly') parts.push(L(P.opt?'co.eb.s.reponlyq':'co.eb.s.reponly'));
          else if(st.s==='own') parts.push(L('co.eb.s.own'));
          else { parts.push(st.kind?L('co.eb.s.kind').replace('{k}',`<span class="kt">${st.kind}</span>`).replace('{w}',L(EB_WHY(st.kind))):L('co.eb.s.plain'));
                 parts.push(L('co.eb.s.axv').replace('{v}',fMil(st.own)+EURSUF())); }
        }
        if(st.adj!=null) parts.push(L('co.eb.s.adj').replace('{v}',`${fMil(st.adj)}${EURSUF()}`));
        if(parts.length) mark=sup(fnIdx(L('co.per.fnp').replace('{p}',P.lab)+parts.join(' ')));
      }
    }
    if(r.k==='net_profit'&&P.series){
      const pat=(P.M.pat||[])[P.i];
      if(has(v)&&has(pat)&&fMil(v)!==fMil(pat)) mark=sup(fnIdx(L('co.np.s.mi')));
    }
    const dd=(r.d&&P.lab)?dl(v,pv,r.up):'';
    return `<td class="${P.cls}">${dd}<b class="v">${val(v,r.x)}</b>${mark}</td>`;
  }
  const nowCell=(P,r)=>{ if(!P.now) return ''; const v=r.now?P.now[r.k]:null;
    return `<td class="nw">${r.now&&has(v)?`<b class="now">${val(v,r.x)}</b>`:''}</td>`; };
  // κεφαλίδα (δύο σειρές)
  let h1=`<th class="l" rowspan="2">${L('co.per.fig')} <span class="u">${L('co.per.unit')}</span></th>`, h2='';
  PS.forEach(P=>{
    if(P.now){ h1+=`<th class="${P.cls} grp" colspan="2">${P.lab}</th>`;
               h2+=`<th class="${P.cls} sub2">${L('co.per.px').replace('{d}',SD(P.px))}</th><th class="nw sub2">${L('co.per.px').replace('{d}',SD(curD))}</th>`; }
    else { h1+=`<th class="${P.cls} grp">${P.lab}</th>`; h2+=`<th class="${P.cls} sub2">${P.px?L('co.per.px').replace('{d}',SD(P.px)):''}</th>`; }
  });
  const lab=r=>{ const sw=IS_BANK?BANK_SWAP[r.k]:null; return sw?L(sw.l):L('co.m.'+r.k); };
  let body='';
  R.forEach((g,gi)=>g.forEach((r,ri)=>{
    body+=`<tr${gi&&!ri?' class="gs"':''}><td class="l"><b>${lab(r)}</b></td>`+PS.map(P=>cell(P,r)+nowCell(P,r)).join('')+'</tr>';
  }));
  host.innerHTML=`<table class="pt"><thead><tr>${h1}</tr><tr>${h2}</tr></thead><tbody>${body}</tbody></table>`;
  const fe=document.getElementById('per-fn');
  if(fe){ if(FNS.length){ fe.innerHTML=FNS.map((t,i)=>`<div class="fn"><span class="fnn">${i+1}</span><span class="fnt">${t}</span></div>`).join(''); fe.hidden=false; } else fe.hidden=true; }
  const ne=document.getElementById('per-note');
  if(ne) ne.textContent=((HAS6&&hasCur)?L('co.per.note').replace(/\{d\}/g,curD):(hasCur?L('co.per.note1').replace(/\{d\}/g,curD):L('co.per.note0')))+(HASQ?' '+L('co.per.noteq'):'');
})();

const FAM={
  capital:{c:'#2f80c2',name:L('co.fam.capital')},
  div:{c:'#cf7f00',name:L('co.fam.div')},
  listing:{c:'#57a5df',name:L('co.fam.listing')},
  index:{c:'#2b4a6b',name:L('co.fam.index')}
};
const EVENTS=(AX&&AX.events)||[];;
// Ποσά €/μτχ στα labels γεγονότων → 3 δεκαδικά (κουκκίδες γραφήματος)
function fmt3(s){return String(s==null?'':s).replace(/€\s*([0-9][0-9.,]*)/g,function(_,num){var n=parseFloat(num.replace(/\./g,'').replace(',','.'));return isNaN(n)?('€'+num):('€'+n.toLocaleString(LOC(),{minimumFractionDigits:3,maximumFractionDigits:3}));});}
const REV_C='#2f80c2', EB_C='#3f9e6a';

const NS='http://www.w3.org/2000/svg';
const el=(n,a={})=>{const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);return e;};
let W=720,H=418,padL=72,padR=64,evLaneY=20,plotTop=74,plotBottom=232,yearY=248,ROWS_TOP=262,ROW_H=30,INSET=22,MOB=false;
// §185 — ΚΙΝΗΤΟ: κάτω από 560px το γράφημα σχεδιάζεται σε κλίμακα 1:1 με το πλάτος του (όχι το 720 σμικρυμένο),
// με τα μεγέθη του πίνακα σε δύο γραμμές (όνομα από πάνω, τιμή + μεταβολή κάτω από κάθε έτος).
function trajGeom(){
  const cw=Math.round((document.getElementById('host')||{}).clientWidth||720);
  MOB=cw>0&&cw<560;
  if(!MOB){ W=720;H=418;padL=72;padR=64;evLaneY=20;plotTop=74;plotBottom=232;yearY=248;ROWS_TOP=262;ROW_H=30;INSET=22; return; }
  W=Math.max(280,cw); padL=44; padR=24; INSET=12; evLaneY=26; plotTop=70; plotBottom=214; yearY=230; ROWS_TOP=244; ROW_H=40; H=ROWS_TOP+5*ROW_H+4;
}
const host=document.getElementById('host'),tip=document.getElementById('tip'),wrapEl=host.parentElement;
const WIN=6; let trajStart=Math.max(0,((company.years&&company.years.length)||6)-WIN);
const xOf=i=>padL+INSET+(W-padL-padR-INSET)*(i/(WIN-1));

function niceScale(minv,maxv){
  if(minv==null||isNaN(minv)) minv=0;
  if(maxv==null||isNaN(maxv)) maxv=1;
  const span=(maxv-Math.min(0,minv))||1;
  const rawStep=span/5;
  const mag=Math.pow(10,Math.floor(Math.log10(rawStep)));
  const norm=rawStep/mag;
  let step=norm<=1?1:norm<=2?2:norm<=2.5?2.5:norm<=5?5:10; step*=mag;
  const yMax=Math.ceil(maxv/step)*step;
  const yMin=minv<0 ? Math.floor(minv/step)*step : 0;   // περιλαμβάνει αρνητικές τιμές (π.χ. αρνητικό PPI τράπεζας)
  const lines=[];
  for(let v=yMin;v<=yMax+step*0.001;v+=step) lines.push(+v.toFixed(6));
  return {yMin,yMax,lines};
}
const pathOf=(arr,yOf)=>{ let d='',started=false; arr.forEach((v,i)=>{ if(v==null)return; d+=(started?' L ':'M ')+xOf(i)+' '+yOf(v); started=true; }); return d; };
// §76 — ΜΕΤΑΒΟΛΗ ΜΕ ΑΡΝΗΤΙΚΗ ΒΑΣΗ. Η διαίρεση με ΠΡΟΣΗΜΑΣΜΕΝΗ βάση αντιστρέφει το
// πρόσημο όταν το προηγούμενο μέγεθος είναι αρνητικό: η 8 ATTICA GROUP πήγε από ζημιές
// 13,2 εκατ. σε κέρδη 17,1 εκατ. και η σελίδα έγραφε −229,3 %. Χειρότερα, ζημιά που
// ΜΙΚΡΑΙΝΕΙ (−49,4 → −13,2) έβγαινε −73,3 % με κόκκινο, δηλαδή βελτίωση παρουσιαζόταν ως
// επιδείνωση. 404 από τα 4.655 ζεύγη του site (8,7 %) είχαν αρνητική βάση.
//
// ΚΑΝΟΝΑΣ: μέγεθος = |Δ| / |προηγούμενο| · πρόσημο και χρώμα από την ΠΡΑΓΜΑΤΙΚΗ φορά της
// μεταβολής (Δ), όχι από το πηλίκο.
const yoy=(arr,i)=> (i===0||arr[i]==null||arr[i-1]==null||!arr[i-1]) ? null
                  : (arr[i]-arr[i-1])/Math.abs(arr[i-1])*100;
function addPill(g,x,by,txt,col){
  const w=Math.max(MOB?24:30, txt.length*(MOB?5.4:5.9) + (MOB?4:10));
  const lx=Math.min(Math.max(x,w/2+4),W-w/2-4);
  const t=el('text',{x:lx,y:by,'text-anchor':'middle','font-family':"'Ubuntu Mono'",'font-size':(MOB?9:9.5),'font-weight':700,fill:col});
  t.textContent=txt; g.appendChild(t);
}
function ptLabel(x,py,val,d,place){
  const g=el('g',{});
  const _a=Math.abs(val),_d=_a<100?2:_a<1000?1:0;
  const valStr=val.toLocaleString(LOC(),{minimumFractionDigits:_d,maximumFractionDigits:_d});
  const nearBy = place==='above'? py-11 : py+16;
  const farBy  = place==='above'? py-28 : py+33;
  addPill(g,x,nearBy,valStr,'#16243d');
  if(d!==null){ const up=d>=0; addPill(g,x,farBy,(up?'+':'-')+Math.abs(d).toLocaleString(LOC(),{maximumFractionDigits:1})+'%',up?'#2f9e52':'#d64530'); }
  return g;
}

function metricRow(svg,name,arr,fmtV,color,top,goodUp,showPct){
  if(goodUp===undefined) goodUp=true;
  if(showPct===undefined) showPct=true;
  svg.appendChild(el('line',{x1:0,y1:top,x2:W,y2:top,stroke:'#eaf1f8','stroke-width':1}));
  if(MOB){
    const ml=el('text',{x:2,y:top+11,'font-family':"'Open Sans'",'font-size':9,'font-weight':700,fill:color}); ml.textContent=name; svg.appendChild(ml);
    for(let li=0; li<WIN; li++){
      const gi=trajStart+li; if(gi>=arr.length) continue;
      const vt=el('text',{x:xOf(li).toFixed(1),y:top+25,'text-anchor':'middle','font-family':"'Ubuntu Mono'",'font-size':10.5,fill:'#16243d'}); vt.textContent=fmtV(arr[gi]); svg.appendChild(vt);
      if(!showPct) continue;
      const d=yoy(arr,gi); if(d===null) continue;
      const good=goodUp?d>=0:d<0;
      const dt=el('text',{x:xOf(li).toFixed(1),y:top+36,'text-anchor':'middle','font-family':"'Ubuntu Mono'",'font-size':8.5,'font-weight':700,fill:good?'#2f9e52':'#d64530'});
      dt.textContent=(d>=0?'+':'-')+Math.abs(d).toLocaleString(LOC(),{maximumFractionDigits:1})+'%'; svg.appendChild(dt);
    }
    return;
  }
  const nl=el('text',{x:3,y:top+ROW_H/2+3.5,'font-family':"'Open Sans'",'font-size':9,'font-weight':700,fill:color}); nl.textContent=name; svg.appendChild(nl);
  const vy=top+ROW_H/2+4, YEAR_R=13, PCTG=38;
  for(let li=0; li<WIN; li++){
    const gi=trajStart+li; if(gi>=arr.length) continue;
    const nx=xOf(li)+YEAR_R, vstr=fmtV(arr[gi]);
    const vt=el('text',{x:nx.toFixed(1),y:vy,'text-anchor':'end','font-family':"'Ubuntu Mono'",'font-size':11,fill:'#16243d'}); vt.textContent=vstr; svg.appendChild(vt);
    if(!showPct) continue;
    const d=yoy(arr,gi); if(d===null) continue;
    const dstr=(d>=0?'+':'-')+Math.abs(d).toLocaleString(LOC(),{maximumFractionDigits:1})+'%';
    const good=goodUp?d>=0:d<0;
    const dt=el('text',{x:(nx+PCTG).toFixed(1),y:vy,'text-anchor':'end','font-family':"'Ubuntu Mono'",'font-size':8.5,'font-weight':700,fill:good?'#2f9e52':'#d64530'}); dt.textContent=dstr; svg.appendChild(dt);
  }
}

function draw(){
  trajGeom();
  const revF=(company.metrics.revenue||[]).map(v=>(v==null?null:v/1e6));
  const ebF=(company.metrics.ebitda||[]).map(v=>(v==null?null:v/1e6));
  const ppiF=(company.metrics.ppi||[]).map(v=>(v==null?null:v/1e6));   // τράπεζες: Κέρδη προ προβλέψεων
  const s=trajStart;
  const secF=IS_BANK?ppiF:ebF;   // 2η γραμμή γραφήματος: PPI για τράπεζες, EBITDA για τις υπόλοιπες
  const rev=revF.slice(s,s+WIN), eb=(IS_BANK && !ppiF.some(v=>v!=null&&v!==0) ? [] : secF).slice(s,s+WIN);
  const _all=rev.concat(eb).filter(v=>v!=null);   // τρέχον έτος = κενά μεγέθη → εκτός κλίμακας
  const {yMin,yMax,lines}=niceScale(_all.length?Math.min(0,..._all):0, _all.length?Math.max(..._all):1);
  const yOf=v=>plotBottom-((v-yMin)/((yMax-yMin)||1))*(plotBottom-plotTop);
  const zeroY=yOf(0);   // βάση αναφοράς: οι περιοχές κλείνουν στο μηδέν (όχι στο κάτω άκρο)

  host.innerHTML='';
  const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,role:'img'});

  lines.forEach(v=>{const y=yOf(v);
    svg.appendChild(el('line',{x1:padL,y1:y,x2:W-padR,y2:y,stroke:'#eaf1f8','stroke-width':1}));
    const tl=el('text',{x:padL-(MOB?5:10),y:y+(MOB?3:4),'text-anchor':'end','font-family':"'Ubuntu Mono'",'font-size':(MOB?9:10),fill:'#8199b3'}); tl.textContent=(v==null||isNaN(v))?'—':v.toLocaleString(LOC()); svg.appendChild(tl);
  });
  const evl=el('text',{x:MOB?2:3,y:MOB?9:evLaneY+4,'font-family':"'Open Sans'",'font-size':(MOB?8.5:9),'font-weight':700,fill:'#6b8199'}); evl.textContent=L('co.chart.events'); svg.appendChild(evl);

  const defs=el('defs',{});
  [['grev',REV_C],['geb',EB_C]].forEach(([id,c])=>{
    const lg=el('linearGradient',{id,x1:0,y1:0,x2:0,y2:1});
    lg.appendChild(el('stop',{offset:'0%','stop-color':c,'stop-opacity':.42}));
    lg.appendChild(el('stop',{offset:'100%','stop-color':c,'stop-opacity':.02}));
    defs.appendChild(lg);
  });
  svg.appendChild(defs);
  const rd=pathOf(rev,yOf), ed=pathOf(eb,yOf);
  const _fi=a=>{for(let i=0;i<a.length;i++)if(a[i]!=null)return i;return -1;}, _li=a=>{for(let i=a.length-1;i>=0;i--)if(a[i]!=null)return i;return -1;};
  const areaOf=(d,a)=>{const fi=_fi(a),li=_li(a); return (fi<0||!d)?'':d+` L ${xOf(li)} ${zeroY} L ${xOf(fi)} ${zeroY} Z`;};
  if(rd) svg.appendChild(el('path',{d:areaOf(rd,rev),fill:'url(#grev)'}));
  if(eb.length&&ed) svg.appendChild(el('path',{d:areaOf(ed,eb),fill:'url(#geb)'}));
  if(rd) svg.appendChild(el('path',{d:rd,fill:'none',stroke:REV_C,'stroke-width':2,'stroke-linejoin':'round'}));
  if(eb.length&&ed) svg.appendChild(el('path',{d:ed,fill:'none',stroke:EB_C,'stroke-width':2,'stroke-linejoin':'round'}));

  // axis baseline + year numbers close to axis
  svg.appendChild(el('line',{x1:padL,y1:zeroY,x2:W-padR,y2:zeroY,stroke:(yMin<0?'#b8c6d8':'#cfdcea'),'stroke-width':(yMin<0?1.4:1)}));
  company.years.slice(s,s+WIN).forEach((yr,li)=>{ const t=el('text',{x:xOf(li),y:yearY,'text-anchor':'middle','font-family':"'Ubuntu Mono'",'font-size':(MOB?10:11),fill:'#6b8199'});
    t.textContent=yr; svg.appendChild(t); });
  // «Αλλαγή οντότητας» — διακριτικό κάθετο σημάδι στο έτος τομής (τα αριστερά αφορούν την παλιά οντότητα)
  (function(){
    var ech=(AX&&AX.echange); if(!ech||!ech.year) return;
    var yrs=company.years.slice(s,s+WIN); var mi=yrs.indexOf(ech.year), mx=null;
    if(mi>0) mx=(xOf(mi-1)+xOf(mi))/2;                       // ανάμεσα στο προηγ. έτος και στο έτος αλλαγής
    else if(mi===0) mx=xOf(0)-INSET*0.55;                    // αρχή παραθύρου
    else if(ech.year>yrs[yrs.length-1]) mx=MOB?W-3:(xOf(WIN-1)+(W-padR))/2;  // πέρα από το παράθυρο → δεξί άκρο
    else return;                                             // πριν το παράθυρο → χωρίς σημάδι
    var CA='#c8862a';
    svg.appendChild(el('line',{x1:mx,y1:(MOB?13:plotTop-2),x2:mx,y2:yearY-9,stroke:CA,'stroke-width':1.3,'stroke-dasharray':'3 3',opacity:.7}));
    var tg=el('text',{x:(MOB?Math.min(W-36,Math.max(mx,128)):mx),y:(MOB?9:plotTop-6),'text-anchor':'middle','font-family':"'Open Sans'",'font-size':8.5,'font-weight':700,fill:CA,opacity:.95}); tg.textContent='▸ '+L('co.echange.mark'); svg.appendChild(tg);
  })();
  // έντονη διαχωριστική γραμμή ανάμεσα στο γράφημα/έτη και στον πίνακα μεγεθών
  svg.appendChild(el('line',{x1:0,y1:ROWS_TOP-7,x2:W,y2:ROWS_TOP-7,stroke:'#8299b3','stroke-width':1.8}));

  // secondary metrics as lines below the axis
  const np=company.metrics.net_profit.map(v=>v==null?null:v/1e6);
  const f0=v=>{if(v==null||isNaN(v))return '—';const a=Math.abs(v),d=a<100?2:a<1000?1:0;return v.toLocaleString(LOC(),{minimumFractionDigits:d,maximumFractionDigits:d});}, fx=v=>(v==null||isNaN(v))?'—':v.toLocaleString(LOC(),{maximumFractionDigits:1});
  metricRow(svg,L('co.chart.netprofit'), np, f0, '#cf7f00', ROWS_TOP, true, true);
  if(IS_BANK){ // τράπεζες: ο «συν. δανεισμός» (πάντα 0) αντικαθίσταται με τον δείκτη ΜΕΑ (NPE %)
    const fpct=v=>(v==null||isNaN(v))?'—':v.toLocaleString(LOC(),{minimumFractionDigits:1,maximumFractionDigits:1})+'%';
    metricRow(svg,L('co.chart.npe'), (AX&&AX.ratios&&AX.ratios.npe&&AX.ratios.npe.series)||[], fpct, '#8fc4ee', ROWS_TOP+ROW_H, false, false);
  } else {
    metricRow(svg,L('co.chart.totaldebt'), company.metrics.total_debt.map(v=>v==null?null:v/1e6), f0, '#8fc4ee', ROWS_TOP+ROW_H, false, true);
  }
  metricRow(svg,L('co.chart.netdebt'), company.metrics.net_debt.map(v=>v==null?null:v/1e6), f0, '#2b4a6b', ROWS_TOP+2*ROW_H, false, true);
  metricRow(svg,'P/E', company.metrics.pe, fx, '#57a5df', ROWS_TOP+3*ROW_H, true, false);
  metricRow(svg,'P/BV', company.metrics.pbv, fx, '#2f80c2', ROWS_TOP+4*ROW_H, true, false);

  // events on TOP lane, connectors down to revenue points
  const byYear={}; EVENTS.forEach(e=>{(byYear[e.year]=byYear[e.year]||[]).push(e);});
  Object.entries(byYear).forEach(([yr,list])=>{
    const gi=company.years.indexOf(+yr); if(gi<0) return;
    const li=gi-s; if(li<0||li>=WIN) return;
    const x=xOf(li), single=list.length===1;
    const ry=(rev[li]==null)?null:yOf(rev[li]);   // τρέχον έτος (κενά μεγέθη) → χωρίς σημείο εσόδων
    const g=el('g',{class:'evt',style:'cursor:pointer'});
    const conn=el('line',{x1:x,y1:evLaneY+8,x2:x,y2:(ry==null?plotBottom:ry),stroke:'#cfdcea','stroke-width':1,'stroke-dasharray':(ry==null?'3 3':'none')}); g.appendChild(conn);
    const DR=MOB?8.5:10;
    const dot=el('circle',{cx:x,cy:evLaneY,r:DR,fill:'#2f80c2',stroke:'#ffffff','stroke-width':2}); g.appendChild(dot);
    const n=el('text',{x:x,y:evLaneY+(MOB?3:3.5),'text-anchor':'middle','font-family':"'Ubuntu Mono'",'font-size':(MOB?9.5:10.5),fill:'#fff','font-weight':600}); n.textContent=list.length; g.appendChild(n);
    const ring=(ry==null)?null:el('circle',{cx:x,cy:ry,r:3.4,fill:'#ffffff',stroke:REV_C,'stroke-width':2}); if(ring) g.appendChild(ring);
    g.appendChild(el('circle',{cx:x,cy:evLaneY,r:15,fill:'transparent'}));
    g.addEventListener('mouseenter',()=>{
      let h=`<div class="ty">${single?list[0].date:yr+' · '+list.length+' '+L('co.evk.plural')}</div>`;
      list.forEach(e=>{ h+=`<div class="row"><i style="background:${(FAM[e.fam]||{c:'#8595ad'}).c}"></i><span class="l">${!single?`<span class="d">${e.date}</span> `:''}${fmt3(e.label)}</span></div>`; });
      tip.innerHTML=h; tip.classList.add('on');
      const wr=wrapEl.getBoundingClientRect(), dr=dot.getBoundingClientRect();
      const cx=dr.left-wr.left+dr.width/2, tw=tip.offsetWidth, pad=8;
      tip.style.left=Math.max(pad,Math.min(cx-tw/2, wr.width-tw-pad))+'px';
      tip.style.top=(dr.bottom-wr.top+8)+'px';
      conn.setAttribute('stroke','#b9cade'); conn.setAttribute('stroke-width',1.5);
      if(ring) ring.setAttribute('r',5); dot.setAttribute('r',DR+1.5);
    });
    g.addEventListener('mouseleave',()=>{
      tip.classList.remove('on');
      conn.setAttribute('stroke','#2b4a7d'); conn.setAttribute('stroke-width',1);
      if(ring) ring.setAttribute('r',3.4); dot.setAttribute('r',DR);
    });
    svg.appendChild(g);
  });

  rev.forEach((v,i)=>{ if(v==null)return; svg.appendChild(el('circle',{cx:xOf(i),cy:yOf(v),r:3.4,fill:'#ffffff',stroke:REV_C,'stroke-width':2})); });
  eb.forEach((v,i)=>{ if(v==null)return; svg.appendChild(el('circle',{cx:xOf(i),cy:yOf(v),r:3.4,fill:'#ffffff',stroke:EB_C,'stroke-width':2})); });
  // Όταν τα δύο σημεία μιας χρονιάς είναι κοντά, βάζουμε το label του καθενός σε αντίθετη πλευρά
  // (ψηλότερο→πάνω, χαμηλότερο→κάτω) ώστε να μην πέφτουν το ένα πάνω στο άλλο. Αλλιώς: πάνω.
  const CLOSE=32;
  rev.forEach((v,i)=>{ if(v==null)return; let place='above';
    if(eb.length&&eb[i]!=null){ const yr=yOf(v),ye=yOf(eb[i]); if(Math.abs(yr-ye)<CLOSE && yr>ye && yr+33<yearY-(MOB?12:2)) place='below'; }
    svg.appendChild(ptLabel(xOf(i),yOf(v),v,yoy(revF,s+i),place)); });
  // §78 — Η 2η γραμμή ΤΙΜΕΣ από `secF`, άρα και η ΜΕΤΑΒΟΛΗ από `secF`. Το `yoy(ebF,…)`
  // ήταν καρφωμένο στο EBITDA· στις τράπεζες το EBITDA είναι παντού κενό, οπότε η μεταβολή
  // έβγαινε null και η γραμμή PPI εμφανιζόταν χωρίς κανένα ποσοστό ανά έτος.
  eb.forEach((v,i)=>{ if(v==null)return; let place='above';
    if(rev[i]!=null){ const ye=yOf(v),yr=yOf(rev[i]); if(Math.abs(yr-ye)<CLOSE && ye>yr && ye+33<yearY-(MOB?12:2)) place='below'; }
    svg.appendChild(ptLabel(xOf(i),yOf(v),v,yoy(secF,s+i),place)); });
  host.appendChild(svg);
}
draw();
(function(){ var lastW=Math.round(host.clientWidth||0), tmr=null;
  window.addEventListener('resize',function(){ clearTimeout(tmr); tmr=setTimeout(function(){
    var cw=Math.round(host.clientWidth||0); if(cw===lastW) return;
    var wasMob=MOB; lastW=cw; if(wasMob||cw<560) draw(); },150); });
})();

const ownership=(AX&&AX.ownership)||[];;
const SIZE_RAMP=['#c2410c','#e2590e','#f0791f','#f5a04c','#f0c07e','#5ea9b4','#8dc8d1','#bce0e6'];
(function(){
  const named=ownership.filter(h=>h.type!=='ευρύ επενδυτικό κοινό').slice().sort((a,b)=>b.pct-a.pct);
  named.forEach((h,i)=> h._c = SIZE_RAMP[Math.min(i,SIZE_RAMP.length-1)]);
  ownership.filter(h=>h.type==='ευρύ επενδυτικό κοινό').forEach(h=> h._c='#c3d3e3');
})();
const escA=t=>String(t).replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
// §185 — compact «Μέτοχοι»: μία λεπτή μπάρα 100% + μία γραμμή ανά μέτοχο (το free float τελευταίο, αχνό)
(function(){
  const el=document.getElementById('own-viz'); if(!el) return;
  const ffObj=ownership.find(h=>h.type==='ευρύ επενδυτικό κοινό');
  const rest=ownership.filter(h=>h!==ffObj).sort((a,b)=>b.pct-a.pct);
  const ord=ffObj?[...rest,ffObj]:rest.slice();
  if(!ord.length){ el.innerHTML=''; return; }
  const fp=p=>(p==null?0:p).toLocaleString(LOC(),{minimumFractionDigits:1,maximumFractionDigits:1})+'%';
  const bar=ord.map(h=>`<i style="width:${Math.max(0,h.pct||0)}%;background:${h._c}"></i>`).join('');
  const rows=ord.map(h=>`<div class="rw${h===ffObj?' ff':''}"><span class="sw" style="background:${h._c}"></span><span class="n">${h===ffObj?L('co.ff'):h.name}</span><span class="p">${fp(h.pct)}</span></div>`).join('');
  el.innerHTML=`<div class="own2"><div class="bar2" role="img" aria-label="${escA(L('co.ph.holders'))}">${bar}</div>${rows}</div>`;
})();

const subs=(AX&&AX.subs)||{total:0,countries:0,full:0,equity:0,listed:[],byCountry:[]};;
/* §126 — ΚΕΝΗ ΚΑΤΑΣΤΑΣΗ «Θυγατρικές & συμμετοχές»: όταν δεν υπάρχει καμία οντότητα, το ντόνατ
   έδειχνε «0 οντότητες» με άδειο υπόμνημα και άδεια λίστα. Κρύβουμε γράφημα/κουμπί/φίλτρο και
   βάζουμε μία γραμμή κειμένου. Η γραμμή φτιάχνεται ΕΔΩ (όχι στο κέλυφος) ώστε η αλλαγή να μην
   απαιτεί ξαναψήσιμο και των 139 στατικών σελίδων. Η διατύπωση λέει ΤΙ βρέθηκε στις καταστάσεις,
   δεν βεβαιώνει ότι η εταιρεία δεν έχει θυγατρικές. */
// §185 — compact «Θυγατρικές & συμμετοχές»: σύνοψη, λεπτή μπάρα, μία γραμμή ανά χώρα (5 + «Λοιπές»).
// Η πλήρης λίστα (με αναζήτηση) ανοίγει από το «Όλες οι οντότητες». Χωρίς ντόνατ/Chart.js.
const geoShort={'Ηνωμένο Βασίλειο':'Ην. Βασίλειο'};
const GEO_TOP=5, GEO_REST_COL='#c3d3e3';
const geoData=(function(){
  const all=subs.byCountry||[];
  const out=all.slice(0,GEO_TOP).map((g,i)=>({c:g.country,label:geoShort[g.country]||g.country,n:g.count,col:SIZE_RAMP[Math.min(i,SIZE_RAMP.length-1)]}));
  if(all.length>GEO_TOP){
    const rest=all.slice(GEO_TOP), rn=rest.reduce((s,g)=>s+(g.count||0),0);
    out.push({c:`${L('co.geo.other')} (${rest.length})`,label:`${L('co.geo.other')} (${rest.length})`,n:rn,col:GEO_REST_COL,rest:true});
  }
  return out;
})();
const geoPct=n=>Math.round(n/subs.total*100);
(function(){
  const s2=document.getElementById('subs2'), all=document.getElementById('subs-all');
  if(!s2) return;
  if(!subs.total){
    s2.innerHTML=`<p class="subs-none" id="subs-none" data-i18n="co.subs.none">${L('co.subs.none')}</p>`;
    if(all) all.hidden=true;
    return;
  }
  const cty=subs.countries===1?L('co.geo.country'):L('co.geo.countries');
  s2.innerHTML=`<div class="sum"><b>${subs.total}</b> ${subs.total===1?L('co.geo.entity'):L('co.geo.entities')}${L('co.geo.in')}<b>${subs.countries}</b> ${cty}</div>`
    +`<div class="bar2">${geoData.map(g=>`<i style="width:${g.n/subs.total*100}%;background:${g.col}"></i>`).join('')}</div>`
    +geoData.map(g=>`<div class="rw${g.rest?' rest':''}"><span class="sw" style="background:${g.col}"></span><span class="n">${g.label}</span><span class="t">${g.n}</span><span class="p">${geoPct(g.n)}%</span></div>`).join('');
})();
// §185 — εισηγμένες θυγατρικές: ένα μικρό μπλοκ με μία γραμμή ανά εταιρεία (όνομα · αγορά · ποσοστό)
document.getElementById('listed-wrap').innerHTML=subs.listed.length?`<div class="lst"><div class="lst-h">${L('co.geo.listedh')}</div>`+subs.listed.map(l=>`<div class="lst-r"><span class="ln">${l.name}</span><span class="lx">${l.exch||''}</span><span class="lp">${(l.stake==null?0:l.stake).toLocaleString(LOC(),{minimumFractionDigits:1,maximumFractionDigits:1})}%</span></div>`).join('')+'</div>':'';

const acc=document.getElementById('acc');
acc.innerHTML=subs.byCountry.map(g=>{
  const named=g.named.map(e=>`<div class="ent" data-name="${e.name.toLowerCase()}"><span class="en">${e.name}${e.listed?`<span class="mini-listed">${L('co.geo.listed')}</span>`:''}<span class="meth">${e.method}</span></span><span class="est">${(e.stake==null?0:e.stake).toLocaleString(LOC(),{minimumFractionDigits:1,maximumFractionDigits:1})}%</span></div>`).join('');
  const clusters=g.clusters.map(c=>`<div class="ent cluster" data-name="${c.label.toLowerCase()}"><span class="en">+ ${c.n} ${c.label}</span><span class="est">—</span></div>`).join('');
  return `<div class="acc-group" data-country="${g.country.toLowerCase()}"><div class="acc-head"><span class="cn">${g.country}</span><span><span class="cc">${g.count} ${L('co.geo.entities_n')}</span><span class="arr">›</span></span></div><div class="acc-body">${named}${clusters}</div></div>`;
}).join('');
acc.querySelectorAll('.acc-head').forEach(h=>h.onclick=()=>h.parentElement.classList.toggle('open'));

(function(){ const sb=document.getElementById('show-all');
  if(sb) sb.innerHTML=`${L('co.geo.all')} (${subs.total}) <span class="arw">▸</span>`; })();
document.getElementById('subs-filter').oninput=e=>{
  const q=e.target.value.trim().toLowerCase();
  acc.querySelectorAll('.acc-group').forEach(g=>{
    const country=g.dataset.country,countryMatch=!q||country.includes(q);let any=false;
    g.querySelectorAll('.ent').forEach(en=>{const m=!q||countryMatch||en.dataset.name.includes(q);en.style.display=m?'':'none';if(m&&q&&!countryMatch)any=true;});
    g.style.display=(!q||countryMatch||any)?'':'none';
    if(q&&(countryMatch||any))g.classList.add('open');else if(!q)g.classList.remove('open');
  });
};

const RATIOS=[
 {cat:'Κερδοφορία',items:[
   {label:'ROA',en:'Return on Assets',unit:'%',series:[6,7.5,10,9,9.2,9.0],sector:7.2,desc:'Πόσα κερδίζει η εταιρεία από κάθε ευρώ περιουσίας που έχει στα χέρια της.',den:'How much the company earns from every euro of assets it holds.',dir:'hi'},
   {label:'ROE',en:'Return on Equity',unit:'%',series:[18,22,30,26,25,24],sector:18.5,desc:'Πόσα κερδίζει από κάθε ευρώ που έχουν βάλει οι μέτοχοι.',den:'How much it earns on every euro shareholders have put in.',dir:'hi'},
   {label:'Απόδ. επενδεδ. κεφαλαίων',en:'Return on Invested Capital (ROIC)',unit:'%',series:[12,15,20,18,17.5,17],sector:13,desc:'Απόδοση σε όλα τα κεφάλαια που δουλεύουν στην επιχείρηση, δικά της και δανεικά.',den:'The return on all capital working in the business, its own and borrowed.',dir:'hi'},
   {label:'Μικτό περιθώριο',en:'Gross Profit Margin',unit:'%',series:[42,44,46,45,44.5,44],sector:40,desc:'Τι μένει από κάθε 100 ευρώ πωλήσεων αφού πληρωθεί το κόστος παραγωγής.',den:'What is left of every 100 euros of sales after production cost is paid.',dir:'hi'},
   {label:'Καθαρό περιθώριο',en:'Net Profit Margin',unit:'%',series:[12,15,22,19,20.5,20.1],sector:14,desc:'Τι μένει τελικά ως κέρδος από κάθε 100 ευρώ πωλήσεων, μετά από όλα.',den:'What finally remains as profit out of every 100 euros of sales, after everything.',dir:'hi'},
   {label:'Περιθώριο EBITDA',en:'EBITDA Margin',unit:'%',series:[30,33,36,35,34.5,34.2],sector:30.5,desc:'Πόσο κερδοφόρα είναι η ίδια η λειτουργία, πριν από τόκους, φόρους και αποσβέσεις.',den:'How profitable the operation itself is, before interest, tax and depreciation.',dir:'hi'},
 ]},
 {cat:'Ρευστότητα',items:[
   {label:'Γενική ρευστότητα',en:'Current Ratio',unit:'x',series:[1.1,1.2,1.3,1.25,1.4,1.5],sector:1.3,desc:'Αν φτάνουν τα βραχυπρόθεσμα περιουσιακά της για όσα χρωστά μέσα στον χρόνο. Πολύ υψηλό δείχνει και αδρανή κεφάλαια.',den:'Whether its short-term assets cover what it owes within the year. Very high also points to idle capital.',dir:'dep'},
   {label:'Άμεση ρευστότητα',en:'Quick Ratio',unit:'x',series:[0.8,0.9,1.0,0.95,1.05,1.1],sector:0.9,desc:'Το ίδιο, αγνοώντας τα αποθέματα — που δεν πουλιούνται πάντα γρήγορα.',den:'The same, ignoring inventory, which does not always sell quickly.',dir:'dep'},
   {label:'Ταμειακή ρευστότητα',en:'Cash Ratio',unit:'x',series:[0.3,0.4,0.5,0.45,0.5,0.55],sector:0.35,desc:'Πόσο από τα άμεσα χρέη της μπορεί να πληρώσει με μετρητά, τώρα. Υπερβολικά μετρητά όμως μένουν ανεκμετάλλευτα.',den:'How much of its immediate debts it can pay in cash, right now. Excess cash, though, sits unused.',dir:'dep'},
 ]},
 {cat:'Φερεγγυότητα',items:[
   {label:'Χρέος / Ίδια κεφάλαια',en:'Debt-to-Equity',unit:'x',series:[1.2,1.0,0.8,0.9,0.75,0.7],sector:1.1,desc:'Πόσο στηρίζεται σε δανεικά έναντι δικών της κεφαλαίων. Υψηλό σημαίνει μεγαλύτερο ρίσκο σε δύσκολη χρονιά.',den:'How much it leans on borrowed money versus its own. High means greater risk in a bad year.',dir:'lo'},
   {label:'Κάλυψη τόκων',en:'Interest Coverage',unit:'x',series:[4,6,9,7.5,8.5,9.2],sector:5.5,desc:'Πόσες φορές τα λειτουργικά κέρδη καλύπτουν τους τόκους των δανείων.',den:'How many times operating profit covers the interest on its loans.',dir:'hi'},
 ]},
 {cat:'Δραστηριότητα',items:[
   {label:'Ημέρες αποθεμάτων',en:'Days Inventory Outstanding',unit:'d',series:[55,50,45,48,44,42],sector:50,desc:'Πόσο καιρό μένει το εμπόρευμα στην αποθήκη πριν πουληθεί.',den:'How long goods sit in the warehouse before they are sold.',dir:'lo'},
   {label:'Ταχύτητα ενεργητικού',en:'Asset Turnover',unit:'x',series:[0.42,0.48,0.55,0.52,0.56,0.58],sector:0.5,desc:'Πόσο τζίρο βγάζει από την περιουσία της. Κρίνεται μόνο έναντι του κλάδου.',den:'How much revenue it generates from its assets. Only meaningful against the sector.',dir:'dep'},
   {label:'Ταχύτητα ιδίων κεφαλαίων',en:'Equity Turnover',unit:'x',series:[0.9,1.0,1.1,1.05,1.12,1.15],sector:0.95,desc:'Πόσο τζίρο βγάζει από τα κεφάλαια των μετόχων. Υψηλό μπορεί να σημαίνει και υψηλή μόχλευση.',den:'How much revenue it generates from shareholders’ capital. High can also mean high leverage.',dir:'dep'},
 ]},
 {cat:'Αποτίμηση',items:[
   {label:'EPS',en:'Earnings Per Share',unit:'€',series:[0.65,0.79,1.85,1.28,1.52,1.51],sector:1.1,desc:'Τα κέρδη της χρονιάς μοιρασμένα σε κάθε μετοχή.',den:'The year’s profit divided across each share.'},
   {label:'P/E',en:'Price-to-Earnings',unit:'x',series:[15,18,22,16,12,8.9],sector:10.8,desc:'Πόσα χρόνια κερδών πληρώνει η αγορά για τη μετοχή. Χαμηλό μπορεί να σημαίνει ευκαιρία ή δυσπιστία.',den:'How many years of earnings the market pays for the share. Low can mean opportunity or distrust.',dir:'dep'},
   {label:'EV/EBITDA',en:'Enterprise Value / EBITDA',unit:'x',series:[8,9,10,7.5,6.5,6.1],sector:7.4,desc:'Πόσο κοστίζει όλη η επιχείρηση, μαζί με τα χρέη της, σε σχέση με τα λειτουργικά της κέρδη.',den:'What the whole business costs, debt included, relative to its operating profit.',dir:'dep'},
   {label:'DPS',en:'Dividend Per Share',unit:'€',series:[0.3,0.55,0.7,0.61,0.6,0.8],sector:0.45,desc:'Πόσα ευρώ μερίσματος αναλογούν σε κάθε μετοχή.',den:'How many euros of dividend fall to each share.'},
   {label:'BVPS',en:'Book Value Per Share',unit:'€',series:[3.6,4.1,4.85,5.2,5.6,5.95],sector:4.5,desc:'Η λογιστική αξία της εταιρείας μοιρασμένη σε κάθε μετοχή.',den:'The company’s book value divided across each share.'},
   {label:'P/BV',en:'Price-to-Book',unit:'x',series:[1.8,2.1,2.4,1.9,1.7,1.6],sector:2.2,desc:'Πόσες φορές τη λογιστική της αξία πληρώνει η αγορά. Κάτω από 1 δεν σημαίνει αυτόματα φθηνό.',den:'How many times its book value the market pays. Below 1 does not automatically mean cheap.',dir:'dep'},
   {label:'Ποσοστό διανομής',en:'Dividend Payout Ratio',unit:'%',series:[40,45,50,48,46,53],sector:45,desc:'Τι ποσοστό των κερδών μοιράζεται ως μέρισμα. Πολύ υψηλό μπορεί να μην είναι βιώσιμο.',den:'What share of profit is handed out as dividend. Very high may not be sustainable.',dir:'dep'},
   {label:'Μερισματική απόδοση',en:'Dividend Yield',unit:'%',series:[3.0,4.0,5.5,4.2,4.5,4.8],sector:3.8,desc:'Τι αποδίδει το μέρισμα σε σχέση με την τιμή. Πολύ υψηλή συχνά σημαίνει πεσμένη μετοχή.',den:'What the dividend returns relative to the price. Very high often signals a fallen share price.',dir:'dep'},
 ]},
 {cat:'Λειτουργικού κόστους',items:[
   {label:'Κόστος πωλήσεων / πωλήσεις',en:'COGS-to-Sales',unit:'%',series:[58,56,54,55,55.5,56],sector:60,desc:'Πόσο από κάθε ευρώ πωλήσεων το τρώει το κόστος παραγωγής.',den:'How much of every euro of sales is eaten by production cost.',dir:'lo'},
   {label:'Έξοδα διοίκησης / πωλήσεις',en:'Administrative Expenses Ratio',unit:'%',series:[8,7.5,7,7.2,7,6.8],sector:8,desc:'Πόσο βαραίνουν τα έξοδα διοίκησης πάνω στον τζίρο.',den:'How heavily administrative costs weigh on turnover.',dir:'lo'},
   {label:'Έξοδα διάθεσης / πωλήσεις',en:'Selling / Distribution Expenses',unit:'%',series:[10,9.5,9,9.3,9,8.8],sector:10,desc:'Πόσο βαραίνουν τα έξοδα πωλήσεων και διανομής πάνω στον τζίρο.',den:'How heavily selling and distribution costs weigh on turnover.',dir:'lo'},
 ]},
 {cat:'Χρηματοοικονομικής διάρθρωσης',items:[
   {label:'Δείκτης ιδίων κεφαλαίων',en:'Equity Ratio',unit:'%',series:[40,43,48,46,50,52],sector:45,desc:'Τι μέρος της περιουσίας της είναι πραγματικά δικό της και όχι δανεικό.',den:'What part of its assets is genuinely its own rather than borrowed.',dir:'hi'},
 ]},
];
const fmtU=(v,u)=>{
  if(v==null||(typeof v==='number'&&isNaN(v))) return '—';
  if(u==='€') return v.toLocaleString(LOC(),{minimumFractionDigits:2,maximumFractionDigits:2})+' €';
  if(u==='d') return Math.round(v).toLocaleString(LOC())+L('unit.days');
  return v.toLocaleString(LOC(),{minimumFractionDigits:1,maximumFractionDigits:1})+(u==='%'?'%':'');
};
const _RLI=(company.latest&&company.latest.idx!=null)?company.latest.idx:company.years.length-1;
const YEARS=company.years.slice(0,_RLI+1);   // πίνακας δεικτών: μόνο πραγματικά έτη (κόψε την κενή στήλη «μόνο-γεγονότων» CURRENT_YEAR)
const ratiosEl=document.getElementById('ratios');
(function(){var S=['roa','roe','roic','gm','nm','ebitdam','current','quick','cash','de','icov','dio','atr','etr','eps','pe','evebitda','dps','bvps','pbv','payout','dy','cogs','admin','selling','equityr'],i=0;
 RATIOS.forEach(function(cat){cat.items.forEach(function(it){it.slug=S[i];
   var r=AX&&AX.ratios&&AX.ratios[S[i]]; if(r){it.series=r.series;it.sector=r.sector;it.secna=r.secna;}
   i++;});});})();
// Τράπεζες: η γραμμή «Έξοδα διοίκησης/πωλήσεις» ΕΙΝΑΙ ο δείκτης κόστους/εσόδων
// (RAW off21 σύνολο λειτ. εξόδων / off18 σύνολο λειτ. εσόδων) — αλλάζει μόνο η ετικέτα.
const RATIO_BANK={admin:{
  el:'Δείκτης κόστους / εσόδων', en:'Cost-to-Income Ratio',
  desc:'Πόσο από κάθε 100 ευρώ εσόδων το τρώνε τα λειτουργικά έξοδα της τράπεζας.',
  den:'How much of every 100 euros of income the bank\u2019s operating costs consume.',
  dir:'lo'}};
// δείκτες με παρονομαστή τον κύκλο εργασιών — δέχονται υποσημείωση όταν το μέγεθος λείπει σκόπιμα
const REV_DEP=new Set(['gm','nm','atr','etr','cogs','admin','selling']);
const FIGN=((company.figNotes||{}).revenue)||{};
// §29.3 «κατά είδος» (ΔΛΠ 1): οι γραμμές κόστους/μικτού/διοίκησης/διάθεσης δεν υπάρχουν στην
// κατάσταση αποτελεσμάτων. Οι παύλες παίρνουν αστερίσκο με επεξήγηση, ώστε να μη διαβάζονται
// ως «δεν το μετρήσαμε».
const BYN=company.byNature||null;
const BYN_SL=new Set(BYN?(BYN.slugs||[]):[]);
// §66 — Η ΣΗΜΕΙΩΣΗ ΕΙΝΑΙ ΑΝΑ ΕΤΟΣ. Η μορφή της κατάστασης αλλάζει μέσα στη σειρά: η
// 20 DIMAND συντάσσει «κατά λειτουργία» 2020-2021 και «κατά είδος» 2022-2025. Το `cells`
// δίνει πίνακα boolean ανά δείκτη, ευθυγραμμισμένο με τα έτη· το `slugs` μένει ως εφεδρεία
// για παλιό data.js (εκεί ίσχυε αδιακρίτως για όλες τις χρήσεις).
const BYN_CE=(BYN&&BYN.cells)||null;
function bynAt(slug,i){ return BYN_CE ? !!((BYN_CE[slug]||[])[i]) : BYN_SL.has(slug); }
function bynText(){ return BYN?(EN()?(BYN.en||BYN.el):(BYN.el||BYN.en)):''; }
// §29.4: η διάμεσος κλάδου λείπει επειδή ΚΑΝΕΝΑΣ στον κλάδο δεν δημοσιεύει το μέγεθος
// (π.χ. μικτό περιθώριο στα Ακίνητα, 0/12 — όλες οι ΑΕΕΑΠ συντάσσουν κατά είδος· ή γενική
// ρευστότητα στις τράπεζες). Σκέτη παύλα θα διαβαζόταν ως «δεν το υπολογίσαμε».
function secNaText(n){
  return EN()
    ? ('No sector median: this figure is not reported by any of the '+n+' listed companies in the sector.')
    : ('Δεν υπάρχει διάμεσος κλάδου: το μέγεθος δεν δημοσιεύεται από καμία από τις '+n+' εισηγμένες του κλάδου.');
}
const esc=t=>String(t).replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const CATEN={'Κερδοφορία':'Profitability','Ρευστότητα':'Liquidity','Φερεγγυότητα':'Solvency','Δραστηριότητα':'Operation','Αποτίμηση':'Value','Λειτουργικού κόστους':'Operating Cost','Χρηματοοικονομικής διάρθρωσης':'Financial Structure'};
/* ══ §185 — ΑΡΙΘΜΟΔΕΙΚΤΕΣ ══════════════════════════════════════════════════════════
   Ένας πίνακας για όλες τις κατηγορίες (κάθε κατηγορία ανοίγει/κλείνει· ανοιχτές στην αρχή
   Κερδοφορία και Αποτίμηση). Στήλες: [συρτάρι ιστορικού] · Ετήσια <τελευταία> · Κλάδος ·
   6Μ <έτος> · Κλάδος (6Μ μόνο με HAS6). Οι ροές του 6μήνου (ROA/ROE/ROIC/EPS, ταχύτητες)
   ΔΕΝ ετησιοποιούνται (απόφαση user) και σημαίνονται με «½». Διανομές (DPS, απόδοση, ποσοστό
   διανομής) είναι μεγέθη ΧΡΗΣΗΣ: στη στήλη 6Μ μένουν «—». Ίδιες υποσημειώσεις με πριν
   («κατά είδος», δεν δημοσιεύεται τζίρος, καμία διάμεσος κλάδου). */
(function(){
  const nY=YEARS.length, HI=YEARS.slice(0,nY-1), yl=YEARS[nY-1];
  const i6=HAS6?AXI.latest.idx:null, y6=HAS6?AXI.latest.period:null;
  const HALF=new Set(['roa','roe','roic','eps','atr','etr']);
  const OPEN0=new Set(['Κερδοφορία']);
  const note=(t)=>`<span class="na" title="${esc(t)}">—<sup class="ast">*</sup></span>`;
  const dash='<span class="na">—</span>';
  function aCell(it,i){
    const v=it.series[i];
    if(v==null&&REV_DEP.has(it.slug)&&FIGN[String(YEARS[i])]) return note(EN()?FIGN[String(YEARS[i])].en:FIGN[String(YEARS[i])].el);
    if(v==null&&bynAt(it.slug,i)) return note(bynText());
    return v==null?dash:fmtU(v,it.unit);
  }
  const secCell=(s,na,u)=>(s==null&&na)?note(secNaText(na)):(s==null?dash:fmtU(s,u));
  const btn=HI.length?`<button class="drw" type="button" aria-expanded="false" aria-controls="rt"><span class="ar">▸</span><span class="tx">${HI[0]}–${HI[HI.length-1]}</span></button>`:'';
  const ncols=1+HI.length+2+(HAS6?2:0);
  let head=`<tr><th class="l"><div class="lh"><span>${L('co.rt.ratio')}</span>${btn}</div></th>`
    +HI.map(y=>`<th class="hx"><div class="hw">${y}</div></th>`).join('')
    +`<th class="ya"><span class="yl">${L('co.per.annual').replace('{y}',yl)}</span></th><th class="kl">${L('co.rt.sector')}</th>`
    +(HAS6?`<th class="h1">${L('co.per.h1').replace('{y}',y6)}</th><th class="kl h1">${L('co.rt.sector')}</th>`:'')+'</tr>';
  const bodies=RATIOS.map(c=>{
    const cn=EN()?(CATEN[c.cat]||c.cat):c.cat, cn2=EN()?c.cat:(CATEN[c.cat]||'');
    const nShow=c.items.length, open=OPEN0.has(c.cat);
    const rows=c.items.map(it=>{
      const bo=IS_BANK?RATIO_BANK[it.slug]:null;
      const nm=bo?(EN()?bo.en:bo.el):(EN()?it.en:it.label);
      if(IS_BANK&&NA_RATIO.has(it.slug))
        return `<tr><td class="l"><b>${nm}</b></td><td class="c-na" colspan="${ncols-1}">${L('co.na.banks')}</td></tr>`;
      const hx=HI.map((y,i)=>`<td class="hx"><div class="hw">${aCell(it,i)}</div></td>`).join('');
      let six='';
      if(HAS6){
        const r6=(AXI.ratios&&AXI.ratios[it.slug])||{};
        const isDiv=DIV_SLUGS_UI.indexOf(it.slug)>-1;
        const v6=isDiv?null:(r6.series||[])[i6];
        let c6=v6==null?(isDiv?dash:(bynAt(it.slug,nY-1)?note(bynText()):dash)):fmtU(v6,it.unit);
        if(v6!=null&&HALF.has(it.slug)) c6+=` <sup class="hf" title="${esc(L('co.rt.half'))}">½</sup>`;
        six=`<td class="h1"><b class="v">${c6}</b></td><td class="kl h1">${isDiv?dash:secCell(r6.sector,r6.secna,it.unit)}</td>`;
      }
      return `<tr><td class="l"><b>${nm}</b></td>${hx}<td class="ya"><b class="v">${aCell(it,nY-1)}</b></td><td class="kl">${secCell(it.sector,it.secna,it.unit)}</td>${six}</tr>`;
    }).join('');
    return `<tbody class="${open?'':'shut'}"><tr class="cat" tabindex="0" role="button" aria-expanded="${open}"><td colspan="${ncols}"><span class="ct"><span class="ca">▸</span>${cn} <span>(${cn2})</span><em class="cn">${nShow} ${nShow===1?L('co.rt.n1'):L('co.rt.nn')}</em></span></td></tr>${rows}</tbody>`;
  }).join('');
  ratiosEl.innerHTML=`<table class="rt" id="rt"><thead>${head}</thead>${bodies}</table>`;
  const T=document.getElementById('rt');
  const b=T.querySelector('.drw');
  if(b) b.addEventListener('click',function(){ const o=T.classList.toggle('open'); b.setAttribute('aria-expanded',o);
    b.querySelector('.tx').textContent=o?L('co.rt.close'):`${HI[0]}–${HI[HI.length-1]}`; });
  T.querySelectorAll('tr.cat').forEach(function(r){
    function t(){ const s=r.parentElement.classList.toggle('shut'); r.setAttribute('aria-expanded',!s); }
    r.addEventListener('click',t);
    r.addEventListener('keydown',function(e){ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); t(); } });
  });
})();


// «Με μια ματιά» — χαρακτηρισμοί με ΑΠΟΛΥΤΑ ΟΡΙΑ (κλάδος μόνο ως αναφορά)· 3ετία μ.ο. Κερδοφορία/Ανάπτυξη, περιόδου Μόχλευση/Ρευστότητα + Χρηματικές διανομές
(function(){
  const G=(AX&&AX.glance)||null;
  const scEl=document.getElementById('scorecard'), dvEl=document.getElementById('distcard');
  const nf=(v,d)=>(v==null||(typeof v==='number'&&isNaN(v)))?'—':v.toLocaleString(LOC(),{minimumFractionDigits:d===undefined?1:d,maximumFractionDigits:d===undefined?1:d});
  const sgn=v=>(v==null?'':(v>=0?'+':''));
  if(!G){ if(scEl)scEl.innerHTML=''; if(dvEl)dvEl.innerHTML=''; return; }
  const cards=[];
  // §31 — ετικέτα βάσης. Στο 6μηνο δεν υπάρχουν ποτέ 3 περίοδοι (102/133 έχουν μία,
  //        25 έχουν δύο), οπότε το «μ.ο. 3ετίας» θα ήταν ψευδές: λέμε τι μπήκε πραγματικά.
  const basisAvg=()=>L('co.gl.b3'), basisGrowth=()=>L('co.gl.b3'), basisPer=()=>L('co.gl.bp');
  // Κερδοφορία — ROE μ.ο. 3ετίας (απόλυτα όρια· κλάδος μόνο ως αναφορά)
  (function(){
    const co=G.profit.co, sec=G.profit.sec;   // co/sec = μ.ο. 3ετίας κερδών προ φόρων (απόλυτο €)
    let t,r;
    if(co==null){t='mid';r='—';}
    else if(co<0){t='bad';r=L('co.gl.r.lossmk');}
    else {t='good';r=L('co.gl.r.profit');}
    const eurM=v=>(v==null?'—':fMil(v)+EURSUF());
    cards.push({cat:L('co.gl.profit'),basis:basisAvg(G.profit),bc:'b3',tone:t,rating:r,metric:L('co.gl.met.ebt'),main:eurM(co),sub:L('co.gl.sector')+eurM(sec)});
  })();
  // Ανάπτυξη — μ.ο. 3ετίας ανάπτυξης εσόδων (απόλυτα όρια· κλάδος μόνο ως αναφορά)
  (function(){
    const co=G.growth.co, sec=G.growth.sec;
    let t,r;
    if(co==null){t='mid';r='—';}
    else if(co<0){t='bad';r=L('co.gl.r.shrink');}
    else if(co<3){t='mid';r=L('co.gl.r.stag');}
    else if(co<8){t='good';r=L('co.gl.r.steady');}
    else {t='good';r=L('co.gl.r.strong');}
    cards.push({cat:L('co.gl.growth'),basis:basisGrowth(G.growth),bc:'b3',tone:t,rating:r,metric:L('co.gl.met.rev'),main:co==null?'—':sgn(co)+nf(co)+'%',
      sub:L('co.gl.sector')+(sec==null?'—':sgn(sec)+nf(sec)+'%')});
  })();
  // Μόχλευση — Χρέος/Ίδια περιόδου (απόλυτα όρια· κλάδος μόνο ως αναφορά)
  (function(){
    const co=G.lev.co, sec=G.lev.sec;
    let t,r;
    if(co==null){t='mid';r='—';}
    else if(co<0){t='bad';r=L('co.gl.r.negeq');}
    else if(co<=1){t='good';r=L('co.gl.r.low');}
    else if(co<=2){t='mid';r=L('co.gl.r.mod');}
    else {t='bad';r=L('co.gl.r.high');}
    cards.push({cat:L('co.gl.lev'),basis:basisPer(G.lev),bc:'bp',tone:t,rating:r,metric:L('co.gl.met.de'),main:co==null?'—':nf(co)+'×',sub:L('co.gl.sector')+(sec==null?'—':nf(sec)+'×')});
  })();
  // Ρευστότητα — Γενική περιόδου· ΤΡΑΠΕΖΕΣ: Δείκτης ΜΕΑ (kind='npe') αντί γενικής ρευστότητας (απόλυτα όρια· κλάδος μόνο ως αναφορά)
  (function(){
    let co=G.liq.co, sec=G.liq.sec;
    let t,r;
    if(G.liq.kind==='npe'){
      // ίδια πηγή/ακρίβεια με την τροχιά (AX.ratios.npe) — αποφυγή διπλής στρογγυλοποίησης (3,75→3,8 vs 3,7)
      if(AX&&AX.ratios&&AX.ratios.npe&&AX.ratios.npe.series){ const s=AX.ratios.npe.series; const _i=(AX.latest&&AX.latest.idx!=null)?AX.latest.idx:s.length-1; co=s[_i]; if(AX.ratios.npe.sector!=null) sec=AX.ratios.npe.sector; }
      // Δείκτης ΜΕΑ (%): <3% χαμηλός/υγιής, 3–5% μέτριος, >5% υψηλός (κατώφλι ECB «high NPL» = 5%)
      if(co==null){t='mid';r='—';}
      else if(co<3){t='good';r=L('co.gl.r.npeLow');}
      else if(co<5){t='mid';r=L('co.gl.r.npeMod');}
      else {t='bad';r=L('co.gl.r.npeHigh');}
      cards.push({cat:L('co.gl.liqNpe'),basis:basisPer(G.liq),bc:'bp',tone:t,rating:r,metric:L('co.gl.met.npe'),main:co==null?'—':nf(co)+'%',sub:L('co.gl.sector')+(sec==null?'—':nf(sec)+'%')});
    } else {
      if(co==null){t='mid';r='—';}
      else if(co>=1.5){t='good';r=L('co.gl.r.adeq');}
      else if(co>=1){t='mid';r=L('co.gl.r.marg');}
      else {t='bad';r=L('co.gl.r.strained');}
      cards.push({cat:L('co.gl.liq'),basis:basisPer(G.liq),bc:'bp',tone:t,rating:r,metric:L('co.gl.met.cur'),main:co==null?'—':nf(co)+'×',sub:L('co.gl.sector')+(sec==null?'—':nf(sec)+'×')});
    }
  })();
  scEl.innerHTML=cards.map(c=>`<div class="sc-item sc-${c.tone}"><div class="sc-cat">${c.cat}</div><div class="sc-basis ${c.bc}">${c.basis}</div><div class="sc-box"><span class="sc-badge">${c.rating}</span><div class="sc-val"><span class="sc-metric">${c.metric}</span><span class="sc-main">${c.main}</span></div><span class="sc-sub">${c.sub}</span></div></div>`).join('');
  // Χρηματικές διανομές — ενοποιημένος πίνακας: Μερίσματα (ανά χρήση) + Επιστροφές κεφ. (ανά έτος πληρωμής)
  const D=(G&&G.dist)||{distributes:false,rows:[]};
  // Μερίσματα ανά χρήση (dps δείκτης) — dividend-only στο νέο μοντέλο
  const divBy={}, dyBy={};
  (D.rows||[]).forEach(r=>{ if(r&&r.dps!=null&&r.dps>1e-9){ divBy[r.y]=r.dps; dyBy[r.y]=(r.dy==null?null:r.dy); } });
  // Επιστροφές κεφαλαίου ανά ΕΤΟΣ ΠΛΗΡΩΜΗΣ — από τα εταιρικά γεγονότα (fam='capital', ποσό e.amt)
  const capBy={};
  (typeof EVENTS!=='undefined'?EVENTS:[]).forEach(e=>{ if(e&&e.fam==='capital'&&e.amt!=null&&e.year!=null){ capBy[e.year]=(capBy[e.year]||0)+e.amt; } });
  // ένωση ετών (μέρισμα ή επιστροφή), φθίνουσα, τελευταία 3ετία
  const yrs=Array.from(new Set(Object.keys(divBy).concat(Object.keys(capBy)).map(Number))).sort((a,b)=>b-a).slice(0,3);
  if(yrs.length){
    const head=`<div class="hdr"><span>${L('co.dist.yr')}</span><span class="r">${L('co.dist.divsh')}</span><span class="r">${L('co.dist.yield')}</span><span class="r">${L('co.dist.capsh')}</span></div>`;
    const body=yrs.map(y=>`<div class="rw"><span class="y">${y}</span><span class="e">${divBy[y]==null?'—':nf(divBy[y],3)}</span><span class="v">${dyBy[y]==null?'—':nf(dyBy[y])+'%'}</span><span class="c">${capBy[y]==null?'—':nf(capBy[y],3)}</span></div>`).join('');
    dvEl.innerHTML=`<div class="dv2">${head}${body}<p class="nt">${L('co.dist.note')}</p></div>`;
  } else {
    dvEl.innerHTML=`<div class="dv2 empty"><b>${L('co.dist.none')}</b><p class="nt">${L('co.dist.none.s')}</p></div>`;
  }
})();

/* ── §125 «Πορεία της εταιρείας» ─────────────────────────────────────────────
   Πηγή: window.AXION.stories[ticker] (φύλλο «ΠΟΡΕΙΑ ΕΤΑΙΡΕΙΩΝ» του master).
   Το κείμενο ΔΕΝ αλλάζει με την όψη Ετήσια/Εξάμηνο — γι' αυτό το block στέκεται
   πάνω από τον διακόπτη. Αν λείπει κείμενο, το block μένει κρυφό. */
(function(){
  var box=document.getElementById('co-story'); if(!box) return;
  var S=(window.AXION&&window.AXION.stories&&AX&&window.AXION.stories[AX.tk])||null;
  if(!S||!S.par) return;
  var lg=curLang(), en=EN();
  var esc2=function(t){return String(t==null?'':t).replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;').replace(/>/g,'&gt;');};
  var md=function(t){return esc2(t).replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>');};
  var pick=function(o){return o?(o[lg]||o.el||''):'';};
  if(en){
    var h2=box.querySelector('.phead h2'); if(h2) h2.textContent='Company trajectory';
    var hn=box.querySelector('.phead .hint'); if(hn) hn.textContent='what management chose and how it shows in the figures';
  }
  var tg=pick(S.tag), te=document.getElementById('story-tag');
  if(te&&tg){ te.textContent=tg; te.hidden=false; }
  var pe=document.getElementById('story-par'); if(pe) pe.innerHTML=md(pick(S.par));
  var w=S.warn?pick(S.warn):'';
  if(w){
    var wb=document.getElementById('story-warn'), wl=wb&&wb.querySelector('.wl'), wt=document.getElementById('story-warn-t');
    if(wl&&en) wl.textContent='Mind the comparison';
    if(wt) wt.innerHTML=md(w);
    if(wb) wb.hidden=false;
  }
  var sv=pick(S.src), sb=document.getElementById('story-src');
  if(sb&&sv){ sb.textContent=(en?'Source: ':'Πηγή: ')+sv; sb.hidden=false; }
  box.hidden=false;
})();

/* ── §128 «Short θέσεις» ─────────────────────────────────────────────────────
   Πηγή: window.AXION_SHORTS (assets/shorts.js), που το παράγει το GitHub Action
   .github/scripts/shorts.py από το αρχείο ανοιχτών πωλήσεων της Επιτροπής
   Κεφαλαιαγοράς. ΑΝΕΞΑΡΤΗΤΟ από το data.js και από το master — γι' αυτό φορτώνεται
   ΕΔΩ δυναμικά και όχι από το κέλυφος: έτσι μια ενημέρωση short ΔΕΝ απαιτεί
   ξαναψήσιμο των 139 στατικών σελίδων.
   Θέση: μέσα στη σκούρα κεφαλίδα, ΑΜΕΣΩΣ ΚΑΤΩ από τη ζώνη «Τρέχοντα Μεγέθη» — το μόνο
   άλλο «τρέχον» δεδομένο της σελίδας. Χωρίς γνωστοποιήσεις → δεν εμφανίζεται τίποτα. */
(function(){
  if(typeof AX==='undefined' || !AX || !AX.tk) return;
  var ph=document.getElementById('co-shorts-host'); if(!ph) return;

  function esc(t){return String(t==null?'':t).replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
  /* δεκαδικό χωριστικό κατά γλώσσα: κόμμα στα ελληνικά, τελεία στα αγγλικά */
  function dec(x){ return EN()?String(x):String(x).replace('.',','); }
  /* 3 δεκαδικά: το αρχείο της Επιτροπής δημοσιεύει έως 5 (π.χ. 1,05351) — με 2 δεκαδικά
     διαφορετικές γνωστοποιήσεις έδειχναν την ίδια τιμή. Ίδια σύμβαση με το /short-positions/. */
  /* `k` = δεκαδικά. Επιτροπή: 3 (βλ. παραπάνω). FCA (§143): 2 — η FCA δημοσιεύει ΜΟΝΟ
     2 δεκαδικά, και το 6,470 θα υπονοούσε ακρίβεια που δεν υπάρχει. */
  function pc(v,k){k=k||3; return (v==null?'—':dec(Number(v).toFixed(k)));}
  function dl(v,k){ k=k||3; if(v==null) return '—'; if(Math.abs(v)<0.5*Math.pow(10,-k)) return dec((0).toFixed(k));
    return (v>0?'+':'−')+dec(Math.abs(v).toFixed(k)); }
  /* Η μεταβολή ΔΕΝ διαβάζεται από το αποθηκευμένο `c`: εκείνο είναι η αληθινή διαφορά στα 5
     δεκαδικά της πηγής και, στρογγυλεμένο στα 3, δεν βγαίνει πάντα από την αφαίρεση των δύο
     ποσοστών που βλέπει ο αναγνώστης. Υπολογίζεται εδώ από τα εμφανιζόμενα νούμερα (απόκλιση
     έως 0,001). Ίδια σύμβαση με το /short-positions/. */
  function rD(v){return v==null?null:Math.round(v*1000)/1000;}
  function chg(rows,i){
    if(!rows||i+1>=rows.length) return null;
    return Math.round((rD(rows[i].p)-rD(rows[i+1].p))*1000)/1000;
  }
  function gd(iso){ var m=/^(\d{4})-(\d{2})-(\d{2})$/.exec(iso||''); return m?(m[3]+'/'+m[2]+'/'+m[1]):(iso||''); }

  function render(){
    var D=window.AXION_SHORTS; if(!D||!D.by) return;
    var rec=D.by[AX.tk];
    var hasRec=!!(rec&&rec.funds&&rec.funds.length);
    /* §142.1 — 11 COCA-COLA HBC: καμία γνωστοποίηση στην Επιτροπή, αλλά υπάρχει
       ανώνυμο άθροισμα FCA. Το block βγαίνει κανονικά, με την αριστερή στήλη να
       λέει ρητά «χωρίς θέση ≥0,5%» αντί να λείπει — η απουσία είναι η πληροφορία. */
    var F=D.fca && D.fca.rows && D.fca.rows[AX.tk];
    /* §143 — ιστορικό FCA: σειρά του ανώνυμου αθροίσματος + ονομαστικές θέσεις ≤10/07/2026 */
    var FH=(D.fca && D.fca.hist && D.fca.hist[AX.tk]) || [];
    var FL=(D.fca && D.fca.legacy && D.fca.legacy[AX.tk]) || null;
    if(!F && (FH.length || (FL && FL.funds && FL.funds.length)))
      F=FH.length?{p:FH[0][1],d:FH[0][0]}:null;
    if(!hasRec && !F) return;
    /* §142.2 — ΕΞΑΙΡΟΥΜΕΝΕΣ ΜΕΤΟΧΕΣ (Άρθρο 16 Καν. 236/2012). Όταν η κύρια αγορά
       διαπραγμάτευσης είναι σε τρίτη χώρα, τα άρθρα 5 και 6 δεν εφαρμόζονται: η Επιτροπή
       Κεφαλαιαγοράς δεν λαμβάνει και δεν δημοσιεύει τίποτα, σε κανένα μέγεθος. ΔΕΝ
       σημαίνει «καμία θέση δεν έφτασε το 0,5%» — άλλο πράγμα.
       Πηγή: ESMA, κατάλογος εξαιρούμενων μετοχών (registers.esma.europa.eu, esma_registers_mifid_shsexs),
       ελεγμένος 21/10/2026: μόνη εν ισχύι εγγραφή με αρμόδια αρχή την Επιτροπή
       Κεφαλαιαγοράς είναι η 11 COCA-COLA HBC. Η ESMA επαναπροσδιορίζει κάθε διετία —
       το .github/scripts/shorts.py τον διαβάζει σε κάθε εκτέλεση και ανοίγει Issue σε μεταβολή.
       ΕΔΩ δεν υπάρχει λίστα: έρχεται έτοιμη στο κλειδί `exempt` του shorts.js. */
    var EX=(!hasRec && D.exempt && D.exempt[AX.tk])?D.exempt[AX.tk]:null;
    var en=EN();
    var T=en?{t:'Short positions',s:'Hellenic Capital Market Commission · disclosures ≥0.5% of share capital',fund:'Fund',st:'Status',
              open:'open',closed:'closed',date:'Date',pos:'Position',chg:'Change',dis:'disclosures',
              twoS:'two independent sources — they are not added together',
              nodH:'No position ≥0.5%',
              exH:'Outside the Greek regime',
              exT:'The share is exempt from Articles 5 and 6 of Regulation (EU) 236/2012 because its principal trading venue is the London Stock Exchange. No short position is disclosed in Greece — at any size, neither by holder name nor as a total. Positions are published in the United Kingdom.',
              exA:function(i,d){return 'ESMA, list of exempted shares · ISIN '+i+' · exempt since '+d;},
              nodT:'No position has been disclosed by name. The threshold is 0.5% of share capital — anything below it is not published at all, neither by holder nor as a total. An empty column therefore does not mean there are no short positions; it means none reached 0.5%.',
              fcaF:function(a,d,n){return 'Source: Financial Conduct Authority'+(a?' · '+a:'')+' · file '+d+' ('+n+' positions)';},
              aggN:'Anonymised aggregate', aggCur:'current', pubs:'publications',
              noopen:'No open short position', lastk:'last known',
              hist:'Short position history', hn:function(n){return n+' fund'+(n===1?'':'s');}, grH:'Greece (Hellenic Capital Market Commission ≥0.5%)', ukH:'United Kingdom (FCA ≥0.2%)',}
             :{t:'Short θέσεις',s:'Επιτροπή Κεφαλαιαγοράς · δημοσιοποιήσεις ≥0,5% του μετοχικού κεφαλαίου',fund:'Fund',st:'Κατάσταση',
              open:'ανοιχτή',closed:'κλειστή',date:'Ημερομηνία',pos:'Θέση',chg:'Μεταβολή',dis:'γνωστοπ.',
              twoS:'δύο ανεξάρτητες πηγές — δεν αθροίζονται',
              exH:'Εκτός ελληνικού καθεστώτος',
              exT:'Η μετοχή εξαιρείται από τα άρθρα 5 και 6 του Κανονισμού (ΕΕ) 236/2012, επειδή κύρια αγορά διαπραγμάτευσής της είναι το Χρηματιστήριο του Λονδίνου. Στην Ελλάδα δεν γνωστοποιείται καμία short θέση — σε κανένα μέγεθος, ούτε ονομαστικά ούτε ως άθροισμα. Οι θέσεις δημοσιεύονται στο Ηνωμένο Βασίλειο.',
              exA:function(i,d){return 'ESMA, κατάλογος εξαιρούμενων μετοχών · ISIN '+i+' · εξαίρεση από '+d;},
              nodH:'Χωρίς θέση ≥0,5%',
              nodT:'Καμία θέση δεν έχει γνωστοποιηθεί ονομαστικά. Το κατώφλι είναι 0,5% του μετοχικού κεφαλαίου — ό,τι είναι κάτω από αυτό δεν δημοσιεύεται καθόλου, ούτε με όνομα ούτε ως σύνολο. Η άδεια στήλη δεν σημαίνει επομένως ότι δεν υπάρχουν short θέσεις· σημαίνει ότι καμία δεν έφτασε το 0,5%.',
              fcaF:function(a,d,n){return 'Πηγή: Financial Conduct Authority'+(a?' · '+a:'')+' · αρχείο '+d+' ('+n+' θέσεις)';},
              aggN:'Ανώνυμο άθροισμα', aggCur:'τρέχον', pubs:'δημοσιεύσεις',
              noopen:'Καμία ανοικτή short θέση', lastk:'τελευταία γνωστή',
              hist:'Ιστορικό short θέσεων', hn:function(n){return n+' fund'+(n===1?'':'s');}, grH:'Ελλάδα (Επιτροπή Κεφαλαιαγοράς ≥0,5%)', ukH:'Ην. Βασίλειο (FCA ≥0,2%)',};

    /* Μία λίστα funds — ΙΔΙΟ markup για Επιτροπή και FCA (§143). `k` δεκαδικά, `opT` η
       ετικέτα της ανοιχτής θέσης (στο αρχείο της FCA: «ανοιχτή στη λήξη», όχι «ανοιχτή»). */
    function fundList(funds,k,opT,inHist){ return funds.map(function(g){
      var rows=g.rows.map(function(r,i){
        var cv=chg(g.rows,i);
        var c=(cv==null||Math.abs(cv)<0.5*Math.pow(10,-k))?'nw':(cv>0?'up':'dn');
        return '<tr><td>'+gd(r.d)+'</td><td>'+pc(r.p,k)+'%'+(r.x?' <span class="chip cl">'+T.closed+'</span>':'')+'</td>'
          +'<td class="'+c+'">'+dl(cv,k)+'</td></tr>';
      }).join('');
      /* §173 — «τελευταία γνωστή» / «κλειστή» δίπλα στο όνομα, όπως πριν. */
      var tag=g.wasOpen?'<span class="chip lk">'+T.lastk+'</span>':(g.open?'':(inHist?'':'<span class="chip cl">'+T.closed+'</span>'));
      return '<details class="'+(g.open?'op':'')+'">'
        +'<summary><span class="arw">▶</span>'
        +'<span class="nm"><b title="'+esc(g.f)+'">'+esc(g.f)+'</b>'+tag+'</span>'
        +'<span class="p">'+pc(g.lp,k)+'%</span>'
        +'<span class="s">'+(g.open?'<span class="chip op">'+opT+'</span>':'')+'</span>'
        +'<span class="d">'+gd(g.ld)+'</span></summary>'
        +'<div class="rows"><table><thead><tr><th>'+T.date+'</th><th>'+T.pos+'</th><th>'+T.chg+'</th></tr></thead><tbody>'
        +rows+'</tbody></table></div></details>';
    }).join(''); }

    /* §144 — ΑΝΟΙΧΤΕΣ ΠΑΝΩ, ΚΛΕΙΣΤΕΣ ΣΤΟ «ΙΣΤΟΡΙΚΟ». Όσες θέσεις δεν είναι ανοιχτές μπαίνουν
       σε πτυσσόμενο μενού «Ιστορικό short θέσεων» κάτω από τις ανοιχτές. Μέσα στο μενού
       η ετικέτα «κλειστή» δίπλα στο όνομα παραλείπεται — το μενού το λέει ήδη.
       `allHist`: όλα στο ιστορικό (ονομαστικές θέσεις FCA ≤10/07/2026 — δεν ξέρουμε αν
       κάποια παραμένει ανοιχτή, άρα δεν τη δείχνουμε ως ανοιχτή). */
    function block(funds,k,opT,allHist,lead){
      var op=[],cl=[];
      (funds||[]).forEach(function(g){ if(g.open && !allHist) op.push(g); else cl.push(g); });
      var h=(lead||'')+fundList(op,k,opT);
      /* §173 — ΤΟ ΚΕΝΟ ΔΕΝ ΕΙΝΑΙ ΠΛΗΡΟΦΟΡΙΑ. Χωρίς ανοιχτή θέση γραφόταν ΤΙΠΟΤΑ και
         ο αναγνώστης πήγαινε κατευθείαν στο «Ιστορικό» χωρίς να ξέρει τι σημαίνει.
         ⚠ ΜΟΝΟ στην ελληνική στήλη (allHist=false): η βρετανική δείχνει ανώνυμο
         άθροισμα που μπορεί να είναι ανοιχτό — εκεί «καμία ανοιχτή» θα ήταν ψέμα. */
      if(!op.length && !allHist) h+='<div class="noopen">'+T.noopen+'</div>';
      if(cl.length)
        h+='<details class="hist"><summary><span class="arw">▶</span>'
          +'<span class="hl">'+T.hist+'</span><span class="hn">'+T.hn(cl.length)+'</span></summary>'
          +'<div class="hb">'+fundList(cl.map(function(g){var o={};for(var q in g)o[q]=g[q];o.wasOpen=!!g.open;o.open=false;return o;}),k,opT,true)+'</div></details>';
      return h;
    }
    function wrap(h){ return h?'<div class="hdr"><span></span><span>'+T.fund+'</span><span class="r">'+T.pos+'</span><span>'+T.st+'</span><span class="r">'+T.date+'</span></div>'+h:''; }

    var box=document.getElementById('co-shorts');
    if(!box){ box=document.createElement('div'); box.className='shl'; box.id='co-shorts'; ph.appendChild(box); }
    var pnl=document.getElementById('p-shorts'); if(pnl) pnl.hidden=false;
    var listHtml=wrap(hasRec?block(rec.funds,3,T.open,false):'');

    if(!F){  /* ΜΙΑ ΠΗΓΗ (139 από τις 141): μονόστηλο, χωρίς ζώνη σύγκρισης. */
      box.innerHTML=listHtml+'<p class="src">'+T.s+'</p>';
      return;
    }

    /* ΔΥΟ ΠΗΓΕΣ (§144–§145, 22/10/2026). ΧΩΡΙΣ ζώνη σύγκρισης πάνω (καταργήθηκε στο §145).
       Δύο στήλες, καθεμία με τίτλο «Ελλάδα (…)» / «Ην. Βασίλειο (…)» — η ΜΟΝΗ αναφορά πηγής
       και κατωφλίου. Ελλάδα: κάθε ανοιχτή θέση ως ξεχωριστή κάρτα. Ην. Βασίλειο: το
       άθροισμα. Από κάτω το «Ιστορικό short θέσεων» και οι διευκρινίσεις. */
    var leftHtml = hasRec ? listHtml
      : (EX ? '<div class="nocard"><div class="h">'+T.exH+'</div><div class="w">'+T.exT+'</div>'
              +'<div class="a">'+T.exA(EX.isin, gd(EX.since))+'</div></div>'
            : '<div class="nocard"><div class="h">'+T.nodH+'</div><div class="w">'+T.nodT+'</div></div>');

    /* Δεξιά: το ανώνυμο άθροισμα ως κάρτα (γραμμές = κάθε δημοσίευση) και, στο ιστορικό,
       οι ονομαστικές θέσεις του παλιού βρετανικού καθεστώτος. */
    var agg='';
    if(FH.length){
      agg=fundList([{f:T.aggN, open:!!(D.fca.rows&&D.fca.rows[AX.tk]), n:FH.length, u:T.pubs,
               lp:FH[0][1], ld:FH[0][0],
               rows:FH.map(function(h){return {d:h[0],p:h[1],x:false};})}],2,T.aggCur);
    }
    var rightHtml=wrap(block(FL?FL.funds:[],2,T.open,true,agg));
    /* §147 — σημαίες πριν από τους τίτλους των στηλών. Inline SVG και ΟΧΙ emoji: στα Windows
       τα emoji σημαιών δεν σχεδιάζονται (βγαίνουν «GR»/«GB»). Αναλογία 3:2 για ομοιομορφία·
       του Ην. Βασιλείου (2:1) κόβεται συμμετρικά (slice). */
    var FLAG_GR='<span class="flag" aria-hidden="true"><svg viewBox="0 0 27 18" preserveAspectRatio="xMidYMid slice">'
      +'<rect width="27" height="18" fill="#0D5EAF"/>'
      +'<path fill="#fff" d="M0 2h27v2H0zM0 6h27v2H0zM0 10h27v2H0zM0 14h27v2H0z"/>'
      +'<rect width="10" height="10" fill="#0D5EAF"/><path fill="#fff" d="M4 0h2v10H4zM0 4h10v2H0z"/></svg></span>';
    var FLAG_UK='<span class="flag" aria-hidden="true"><svg viewBox="0 0 60 30" preserveAspectRatio="xMidYMid slice">'
      +'<clipPath id="axfl-uk"><path d="M30,15h30v15zv15h-30zh-30v-15zv-15h30z"/></clipPath>'
      +'<path d="M0,0v30h60v-30z" fill="#012169"/>'
      +'<path d="M0,0L60,30M60,0L0,30" stroke="#fff" stroke-width="6"/>'
      +'<path d="M0,0L60,30M60,0L0,30" clip-path="url(#axfl-uk)" stroke="#C8102E" stroke-width="4"/>'
      +'<path d="M30,0v30M0,15h60" stroke="#fff" stroke-width="10"/>'
      +'<path d="M30,0v30M0,15h60" stroke="#C8102E" stroke-width="6"/></svg></span>';

    box.innerHTML='<div class="two">'
        +'<div class="col"><div class="lb">'+FLAG_GR+'<span>'+T.grH+'</span></div>'
        +leftHtml+'</div>'
        +'<div class="col"><div class="lb">'+FLAG_UK+'<span>'+T.ukH+'</span></div>'
        +rightHtml
        +'<div class="foot src">'+T.fcaF(D.fca.attr?esc(D.fca.attr):'', gd(D.fca.pub||F.d), D.fca.n||0)+'</div></div>'
      +'</div>';
  }

  function boot(){ render(); try{ document.addEventListener('axion:langchange', render); }catch(e){} }

  if(window.AXION_SHORTS) boot();
  else{
    var sc=document.createElement('script');
    sc.src='/assets/shorts.js'; sc.async=true;
    sc.onload=boot; sc.onerror=function(){};   /* δεν υπάρχει ακόμη → το block απλώς λείπει */
    document.head.appendChild(sc);
  }
})();

