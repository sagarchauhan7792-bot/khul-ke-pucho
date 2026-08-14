/* Khul Ke Pucho — shared site engine (cart, quiz, modals, i18n). Loaded by index + wing/category pages. */
(function(){
  'use strict';
  var WA_NUMBER = '919999999999'; // TODO: real WhatsApp business number

  var CATALOG = {
    urja:{name:'Shukra',price:3938,mark:'ऊ'}, shilajit:{name:'Shilajit',price:2400,mark:'शि'},
    oil:{name:'Paurush Oil',price:960,mark:'तै'}, kit:{name:'Complete Care Kit',price:6088,mark:'पू'},
    pme:{name:'PME Course',price:1499,mark:'का'}, ed:{name:'ED Course',price:1499,mark:'ब'},
    yoga:{name:'Yoga for Vitality Course',price:999,mark:'यो'}, consult:{name:'Private Doctor Consultation',price:99,mark:'वै'},
    yugal:{name:'Yugal Couples Massager',price:4999,mark:'यु'}, tarang:{name:'Tarang Personal Wand',price:3499,mark:'त'},
    bindu:{name:'Bindu Bullet',price:1499,mark:'बि'}, bandhan:{name:'Bandhan Couples Ring',price:1299,mark:'ब'},
    snigdha:{name:'Snigdha Intimate Gel',price:699,mark:'स्'}, sparsh:{name:'Sparsh Massage Oil',price:899,mark:'स्प'},
    jyoti:{name:'Jyoti Massage Candle',price:999,mark:'ज्यो'}, milan:{name:'Milan Couples Kit',price:4999,mark:'मि'},
    khulibaat:{name:'Khuli Baat Card Game',price:799,mark:'ख'}
  };
  var FILES = {
    urja:'shukra.html', shilajit:'shilajit.html', oil:'paurush-oil.html', kit:'complete-care-kit.html',
    pme:'pme-course.html', ed:'ed-course.html', yoga:'yoga-course.html', consult:'consultation.html',
    yugal:'yugal.html', tarang:'tarang.html', bindu:'bindu.html', bandhan:'bandhan.html',
    snigdha:'snigdha.html', sparsh:'sparsh.html', jyoti:'jyoti.html', milan:'milan-kit.html', khulibaat:'khuli-baat.html'
  };
  window.KKP = { CATALOG: CATALOG, FILES: FILES, WA_NUMBER: WA_NUMBER };

  function $(id){ return document.getElementById(id); }

  /* age gate */
  var gate = $('ageGate');
  if (gate) {
    try { if (localStorage.getItem('kkp_age_ok') === '1') gate.classList.add('hidden'); } catch(e){}
    $('ageYes').addEventListener('click', function(){ try{localStorage.setItem('kkp_age_ok','1');}catch(e){} gate.classList.add('hidden'); });
    $('ageNo').addEventListener('click', function(){ location.href = 'https://www.google.com'; });
  }

  var cart = {};
  try { cart = JSON.parse(localStorage.getItem('kkp_cart') || '{}'); } catch (e) { cart = {}; }
  for (var ck in cart) { if (!CATALOG[ck]) delete cart[ck]; }

  var drawer=$('drawer'), overlay=$('overlay'), dbody=$('dbody'), dtot=$('dtot'), toast=$('toast'), toastTimer=null;

  function inr(n){return '₹'+n.toLocaleString('en-IN');}
  function save(){localStorage.setItem('kkp_cart',JSON.stringify(cart));}
  function count(){var c=0;for(var k in cart)c+=cart[k];return c;}
  function total(){var t=0;for(var k in cart)t+=CATALOG[k].price*cart[k];return t;}
  function renderBadges(){var a=$('cartN'),b=$('cartN2');if(a)a.textContent=count();if(b)b.textContent=count();}
  var BUNDLE_EX={consult:1,kit:1,milan:1}; // combos & consult don't count toward bundle tiers
  function bundleInfo(){
    var n=0,base=0;
    for(var k in cart){if(!BUNDLE_EX[k]){n++;base+=CATALOG[k].price*cart[k];}}
    var pct=n>=4?20:n===3?15:n===2?10:0;
    return {n:n,pct:pct,off:Math.round(base*pct/100)};
  }
  function renderDrawer(){
    if(!dbody)return;
    var keys=Object.keys(cart);
    if(!keys.length){dbody.innerHTML='<div class="dempty"><div class="sanskrit" style="font-size:30px;color:var(--kanchan)">॥</div><p>Your cart is empty.<br>Every plan starts with one honest step.</p></div>';}
    else{dbody.innerHTML=keys.map(function(k){var i=CATALOG[k];return '<div class="ditem"><div class="dth">'+i.mark+'</div><div class="dinfo"><b>'+i.name+'</b><span>'+inr(i.price)+'</span></div><div class="dqty"><button data-dec="'+k+'" aria-label="Decrease">−</button><span>'+cart[k]+'</span><button data-inc="'+k+'" aria-label="Increase">+</button></div></div>';}).join('');}
    var b=bundleInfo(),bund=$('dbund'),payable=total()-b.off;
    if(bund){
      if(b.off>0){bund.style.display='flex';$('dbundl').textContent='Bundle savings ('+b.n+' items · '+b.pct+'%)';$('dbundv').textContent='−'+inr(b.off);}
      else bund.style.display='none';
    }
    dtot.textContent=inr(payable);
    var lines=keys.map(function(k){return '- '+CATALOG[k].name+' x'+cart[k]+' ('+inr(CATALOG[k].price*cart[k])+')';});
    if(b.off>0)lines.push('Bundle savings: -'+inr(b.off)+' ('+b.pct+'% off)');
    var msg='Namaste! I would like to order:\n'+lines.join('\n')+'\nTotal: '+inr(payable)+'\n(COD preferred / plain packaging please)';
    var wa=$('waCheckout');if(wa)wa.href='https://wa.me/'+WA_NUMBER+'?text='+encodeURIComponent(msg);
  }
  function render(){renderBadges();renderDrawer();save();}
  function openCart(){if(drawer){drawer.classList.add('on');overlay.classList.add('on');}}
  function closeCart(){if(drawer){drawer.classList.remove('on');overlay.classList.remove('on');}}
  function showToast(t){if(!toast)return;toast.textContent=t;toast.classList.add('on');clearTimeout(toastTimer);toastTimer=setTimeout(function(){toast.classList.remove('on');},1800);}

  /* quiz */
  var qmodal=$('qmodal'), qbox=$('qbox'), qAnswers={};
  var QUIZ_START={id:'concern',q:'What describes your main concern best?',opts:[['timing','Finishing earlier than I want'],['erection','Erection strength or consistency'],['energy','Low energy, stamina or desire'],['couple','We want more from intimacy — together']]};
  var QUIZ_WELL=[
    {id:'duration',q:'How long has this been on your mind?',opts:[['recent','A few weeks'],['months','A few months'],['years','A year or more']]},
    {id:'health',q:'Do any of these apply?',opts:[['metabolic','Diabetes / BP / heart condition'],['stress','High stress or poor sleep'],['none','None of these']]},
    {id:'sleep',q:'How is your sleep, honestly?',opts:[['low','Under 6 hours, often broken'],['mid','6–7 hours'],['good','7+ hours, mostly restful']]},
    {id:'partner',q:'Is a partner part of this journey right now?',opts:[['together','Yes — we want to work on it together'],['private','Yes, but I want to sort this privately first'],['single','No partner right now']]},
    {id:'age',q:'Your age band?',opts:[['a1','Under 30'],['a2','30–45'],['a3','45+']]},
    {id:'style',q:'What suits you best?',opts:[['course','A structured self-paced course'],['formulation','Classical formulations'],['doctor','Let a doctor decide my plan']]}
  ];
  var QUIZ_COUPLE=[
    {id:'stage',q:'Where are you two on this journey?',opts:[['new','Completely new to all this'],['some','We have explored a little'],['open','Comfortable and curious']]},
    {id:'goal',q:'What would you like more of?',opts:[['talk','Openness — we barely talk about it'],['her','More arousal and comfort for her'],['shared','Something we can enjoy together']]},
    {id:'budget',q:'A comfortable budget to start?',opts:[['b1','Under ₹1,500'],['b2','₹1,500–3,500'],['b3','₹3,500+']]}
  ];
  function quizFlow(){return [QUIZ_START].concat(qAnswers.concern==='couple'?QUIZ_COUPLE:QUIZ_WELL);}
  function quizRecommend(){
    var a=qAnswers,rec=[];
    function add(key,why){if(!rec.some(function(r){return r.key===key;}))rec.push({key:key,why:why});}
    if(a.concern==='couple'){
      if(a.goal==='talk'){add('khulibaat','Openness first — 100 questions that make the conversation easy.');add('sparsh','A slow shared massage is the gentlest next step after talking.');}
      else if(a.goal==='her'){add('snigdha','Comfort is the foundation — water-based, pH-balanced, condom-safe.');
        if(a.budget==='b1')add('bindu','Most women respond best to external stimulation — this is the easiest, most discreet start.');
        else add('tarang','Most women respond best to external stimulation — the wand is the gold standard for it.');
        if(a.stage==='new')add('jyoti','Warmth and time matter: arousal takes 15–20 minutes. Set the stage first.');}
      else{if(a.budget==='b3')add(a.stage==='new'?'milan':'yugal',a.stage==='new'?'Everything a couple needs to begin, in one tasteful box.':'Designed to be worn and enjoyed together.');
        else if(a.budget==='b2'){add('bindu','Small, quiet and shared easily — the classic first device.');add('khulibaat','Pair it with the game — anticipation is half the fun.');}
        else{add('bandhan','A shared ring — the most affordable way to explore together.');add('snigdha','Always the right companion product.');}}
      return rec;
    }
    var doctorFirst = a.health==='metabolic' || a.age==='a3' || a.style==='doctor' || a.duration==='years';
    if(doctorFirst){
      var dwhy = a.health==='metabolic' ? 'With BP/sugar in the picture, a doctor must design your plan — non-negotiable with us.'
        : a.duration==='years' ? 'A year or more deserves a real diagnosis, not another guess. Start here.'
        : 'A registered doctor reads your whole picture and writes the plan — the honest first step.';
      add('consult',dwhy);
    }
    if(a.concern==='timing'){add('pme','PE responds to structured technique and weekly practice.');if(!doctorFirst)add('consult','Add the ₹99 consult so a doctor personalises the program.');}
    else if(a.concern==='erection'){add('ed','Cause-first program for circulation, stress and sleep.');
      if(a.sleep==='low'||a.health==='stress')add('shilajit','With stress and short sleep in your answers, classical rasayana support helps the foundation.');
      if(!doctorFirst)add('consult','Add the ₹99 consult so a doctor personalises the program.');}
    else{add('urja','The flagship 60-day vitality course.');add('shilajit','Classical rasayana foundation, lab-standardised.');}
    if(a.partner==='together'&&rec.length<3)add('khulibaat','You said you are in this together — openness measurably helps outcomes.');
    return rec.slice(0,3);
  }
  function quizRender(i){
    var flow=quizFlow();
    if(i<flow.length){var s=flow[i];
      qbox.innerHTML='<button class="qx" data-quiz-close aria-label="Close">&times;</button><div class="qstep">Self-check · '+(i+1)+' of '+flow.length+'</div><div class="qq">'+s.q+'</div>'+s.opts.map(function(o){return '<button class="qopt" data-qa="'+s.id+':'+o[0]+':'+i+'">'+o[1]+'</button>';}).join('')+'<p style="font-size:11.5px;color:#7A5C46;margin-top:12px">Private. Nothing is stored or sent anywhere.</p>';
    }else{var recs=quizRecommend();
      var planTotal=recs.reduce(function(t,r){return t+CATALOG[r.key].price;},0);
      var allKeys=recs.map(function(r){return r.key;}).join(',');
      qbox.innerHTML='<button class="qx" data-quiz-close aria-label="Close">&times;</button><div class="qstep">Your suggested plan</div><div class="qq">Here is the honest starting point</div>'+recs.map(function(r){var it=CATALOG[r.key];return '<div class="qres"><b>'+it.name+' · '+inr(it.price)+'</b><span>'+r.why+'</span><div style="margin-top:10px"><button class="btn btn-gold btn-sm" data-add="'+r.key+'">Add to cart</button></div></div>';}).join('')+'<button class="btn btn-dark" style="width:100%;margin-top:8px" data-addall="'+allKeys+'">Add full plan — '+inr(planTotal)+'</button><p style="font-size:12px;color:#7A5C46;margin-top:10px">Guidance, not a diagnosis. Your doctor confirms the plan on the consult.</p><button class="btn btn-outline" style="width:100%;margin-top:6px" data-quiz-close>Close</button>';
    }
  }
  function quizOpen(){if(!qmodal)return;qAnswers={};quizRender(0);qmodal.classList.add('on');overlay.classList.add('on');}
  function quizClose(){if(!qmodal)return;qmodal.classList.remove('on');if(drawer&&!drawer.classList.contains('on'))overlay.classList.remove('on');}

  /* nav */
  var navTgl=$('navTgl'), catnav=$('catnav');
  function closeMenus(except){document.querySelectorAll('.menu.open').forEach(function(m){if(m!==except){m.classList.remove('open');var b=m.querySelector('button');if(b)b.setAttribute('aria-expanded','false');}});}

  document.addEventListener('click',function(e){
    var add=e.target.closest('[data-add]');
    if(add){var k=add.getAttribute('data-add');cart[k]=(cart[k]||0)+1;render();showToast(CATALOG[k].name+' added');
      if(add.classList.contains('addbtn')){var orig=add.textContent;add.textContent='Added ✓';add.style.background='var(--vana)';add.style.color='#fff';setTimeout(function(){add.textContent=orig;add.style.background='';add.style.color='';},1400);}return;}
    var addAll=e.target.closest('[data-addall]');
    if(addAll){addAll.getAttribute('data-addall').split(',').forEach(function(k){if(CATALOG[k])cart[k]=(cart[k]||0)+1;});render();showToast('Full plan added to cart');openCart();return;}
    var inc=e.target.closest('[data-inc]');if(inc){cart[inc.getAttribute('data-inc')]++;render();return;}
    var dec=e.target.closest('[data-dec]');if(dec){var dk=dec.getAttribute('data-dec');cart[dk]--;if(cart[dk]<=0)delete cart[dk];render();return;}
    if(e.target.closest('[data-quiz-open]')){e.preventDefault();quizOpen();return;}
    if(e.target.closest('[data-quiz-close]')){quizClose();return;}
    var qa=e.target.closest('[data-qa]');if(qa){var p=qa.getAttribute('data-qa').split(':');qAnswers[p[0]]=p[1];quizRender(parseInt(p[2],10)+1);return;}
    var mb=e.target.closest('.menu>button');
    if(mb){var menu=mb.parentElement,willOpen=!menu.classList.contains('open');closeMenus(menu);menu.classList.toggle('open',willOpen);mb.setAttribute('aria-expanded',willOpen?'true':'false');return;}
    if(!e.target.closest('.menu'))closeMenus(null);
    if(e.target.closest('.dd a')){closeMenus(null);if(catnav)catnav.classList.remove('open');}
    var card=e.target.closest('.pcard');
    if(card&&!e.target.closest('button')&&!e.target.closest('a')){var cb=card.querySelector('[data-add]');if(cb){location.href=FILES[cb.getAttribute('data-add')];return;}}
  });

  if($('cartOpen'))$('cartOpen').addEventListener('click',openCart);
  if($('mCart'))$('mCart').addEventListener('click',openCart);
  if($('cartClose'))$('cartClose').addEventListener('click',closeCart);
  if($('cartClose2'))$('cartClose2').addEventListener('click',closeCart);
  if(overlay)overlay.addEventListener('click',function(){closeCart();quizClose();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'){closeCart();quizClose();closeMenus(null);}});
  if(navTgl)navTgl.addEventListener('click',function(){var o=catnav.classList.toggle('open');navTgl.setAttribute('aria-expanded',o?'true':'false');});

  /* ===== bundle builder (present on home only) ===== */
  var BKEYS=['urja','shilajit','oil','pme','ed','tarang','bindu','bandhan','yugal','snigdha','sparsh','jyoti','khulibaat'];
  var bSel={};
  var bchips=$('bchips');
  if(bchips){
    bchips.innerHTML=BKEYS.map(function(k){var i=CATALOG[k];return '<span class="bchip" data-bk="'+k+'" role="checkbox" aria-checked="false" tabindex="0">'+i.name+' <span class="bp">'+inr(i.price)+'</span></span>';}).join('');
    var bUpdate=function(){
      var keys=Object.keys(bSel),n=keys.length,sub=keys.reduce(function(t,k){return t+CATALOG[k].price;},0);
      var pct=n>=4?20:n===3?15:n===2?10:0,off=Math.round(sub*pct/100);
      document.querySelectorAll('#btier span').forEach(function(s){var t=parseInt(s.getAttribute('data-t'),10);s.classList.toggle('on',pct>0&&(t===4?n>=4:n===t));});
      var bline=$('bline'),badd=$('bundleAdd');
      if(!n){bline.textContent='Select products above to build your bundle';badd.disabled=true;}
      else if(pct===0){bline.innerHTML=inr(sub)+' — add 1 more to unlock <b class="bsave">10% off</b>';badd.disabled=false;}
      else{bline.innerHTML='<s style="color:#9A7B60;font-weight:500">'+inr(sub)+'</s> '+inr(sub-off)+' <span class="bsave">you save '+inr(off)+' ('+pct+'%)</span>';badd.disabled=false;}
      badd.textContent=n?'Add '+n+' item'+(n>1?'s':'')+' to cart':'Add bundle to cart';
    };
    bchips.addEventListener('click',function(e){
      var c=e.target.closest('[data-bk]');if(!c)return;
      var k=c.getAttribute('data-bk');
      if(bSel[k])delete bSel[k];else bSel[k]=1;
      c.classList.toggle('sel',!!bSel[k]);c.setAttribute('aria-checked',bSel[k]?'true':'false');
      bUpdate();
    });
    bchips.addEventListener('keydown',function(e){if(e.key===' '||e.key==='Enter'){var c=e.target.closest('[data-bk]');if(c){e.preventDefault();c.click();}}});
    $('bundleAdd').addEventListener('click',function(){
      for(var k in bSel)cart[k]=(cart[k]||0)+1;
      bSel={};document.querySelectorAll('.bchip.sel').forEach(function(c){c.classList.remove('sel');c.setAttribute('aria-checked','false');});
      bUpdate();render();showToast('Bundle added — discount applied in cart');openCart();
    });
    bUpdate();
  }

  /* ===== doctor slot picker ===== */
  var slotModal=$('slotModal'),slotDay=null,slotTime=null;
  if(slotModal){
    var SLOT_TIMES=['10:00 am','12:00 pm','3:00 pm','6:00 pm','8:00 pm','10:00 pm'];
    var slotOpen=function(){
      var days=$('slotDays'),names=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
      var html='';
      for(var d=1;d<=7;d++){var dt=new Date();dt.setDate(dt.getDate()+d);
        var label=d===1?'Tomorrow':names[dt.getDay()];
        html+='<button class="slotc" data-slot-day="'+label+', '+dt.getDate()+' '+months[dt.getMonth()]+'">'+label+'<small>'+dt.getDate()+' '+months[dt.getMonth()]+'</small></button>';}
      days.innerHTML=html;
      $('slotTimes').innerHTML=SLOT_TIMES.map(function(t){return '<button class="slotc" data-slot-time="'+t+'">'+t+'</button>';}).join('');
      slotDay=null;slotTime=null;$('slotConfirm').disabled=true;
      slotModal.classList.add('on');overlay.classList.add('on');
    };
    var slotClose=function(){slotModal.classList.remove('on');if(drawer&&!drawer.classList.contains('on'))overlay.classList.remove('on');};
    slotModal.addEventListener('click',function(e){
      var d=e.target.closest('[data-slot-day]'),t=e.target.closest('[data-slot-time]');
      if(d){slotDay=d.getAttribute('data-slot-day');slotModal.querySelectorAll('[data-slot-day]').forEach(function(x){x.classList.toggle('sel',x===d);});}
      if(t){slotTime=t.getAttribute('data-slot-time');slotModal.querySelectorAll('[data-slot-time]').forEach(function(x){x.classList.toggle('sel',x===t);});}
      $('slotConfirm').disabled=!(slotDay&&slotTime);
    });
    $('slotConfirm').addEventListener('click',function(){
      var msg='Namaste! I would like to book the ₹99 private doctor consultation.\nPreferred slot: '+slotDay+' at '+slotTime+'\nPhone or video is fine. Please confirm.';
      window.open('https://wa.me/'+WA_NUMBER+'?text='+encodeURIComponent(msg),'_blank','noopener');
      cart.consult=(cart.consult||0)+1;render();slotClose();showToast('Slot request sent — consult added to cart');
    });
    $('slotClose').addEventListener('click',slotClose);
    document.addEventListener('click',function(e){if(e.target.closest('[data-slot-open]')){e.preventDefault();slotOpen();}});
  }

  /* ===== exit-intent popup (desktop, once per session) ===== */
  var exitModal=$('exitModal');
  if(exitModal){
    var exitShow=function(){
      if(gate&&gate.classList.contains('hidden')===false)return;
      if((qmodal&&qmodal.classList.contains('on'))||(drawer&&drawer.classList.contains('on'))||(slotModal&&slotModal.classList.contains('on')))return;
      try{if(sessionStorage.getItem('kkp_exit')==='1')return;sessionStorage.setItem('kkp_exit','1');}catch(e){}
      exitModal.classList.add('on');overlay.classList.add('on');
    };
    var exitHide=function(){exitModal.classList.remove('on');if(drawer&&!drawer.classList.contains('on'))overlay.classList.remove('on');};
    document.addEventListener('mouseout',function(e){if(!e.relatedTarget&&e.clientY<=8)exitShow();});
    $('exitClose').addEventListener('click',exitHide);
    $('exitNo').addEventListener('click',exitHide);
    $('exitCta').addEventListener('click',exitHide);
  }

  /* ===== social proof toasts (TODO: replace seed list with real order feed) ===== */
  var sproofEl=$('sproof');
  if(sproofEl){
    var SPROOF=[
      ['R.K. from Kanpur','ordered a wellness plan'],['S. & P. from Indore','ordered the Milan Kit'],
      ['M.T. from Nagpur','booked the ₹99 consult'],['A.V. from Patna','ordered Shilajit'],
      ['K.D. from Jaipur','ordered discreetly'],['V.S. from Lucknow','booked a couples consult'],
      ['N.B. from Bhopal','ordered the PME Course'],['T.R. from Surat','ordered intimate care']
    ];
    var spIdx=Math.floor(Date.now()/60000)%SPROOF.length,spShown=0,spOff=false,spTimer=null;
    var spNext=function(){
      if(spOff||spShown>=4)return;
      var s=SPROOF[spIdx%SPROOF.length];spIdx++;spShown++;
      $('sproofTxt').innerHTML='<b>'+s[0]+'</b> '+s[1]+' recently';
      sproofEl.classList.add('on');
      setTimeout(function(){sproofEl.classList.remove('on');},6000);
      spTimer=setTimeout(spNext,32000);
    };
    $('spx').addEventListener('click',function(){spOff=true;clearTimeout(spTimer);sproofEl.classList.remove('on');});
    if(!(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches))spTimer=setTimeout(spNext,12000);
  }

  /* ===== quick exit ===== */
  if($('qexit'))$('qexit').addEventListener('click',function(){
    try{localStorage.removeItem('kkp_cart');}catch(e){}
    location.replace('https://www.google.com/search?q=weather+today');
  });

  /* ===== Hindi toggle (base map + optional per-page window.KKP_I18N_PAGE) ===== */
  var I18N=[
    ['.announce','<b>KKP99</b> — पहला डॉक्टर परामर्श ₹99 में · ₹999 से ऊपर मुफ़्त गुप्त डिलीवरी · <b>पूरे भारत में COD</b>'],
    ['.hd-consult','डॉक्टर से पूछें · ₹99'],
    ['#worlds .aarogya h2','आयुर्वेदिक स्वास्थ्य'],
    ['#worlds .aarogya p','कारणों का इलाज — समय, शक्ति, ऊर्जा — शास्त्रीय औषधियों, पंजीकृत डॉक्टरों और कोर्स के साथ।'],
    ['#worlds .aarogya .go','आरोग्य में प्रवेश करें →'],
    ['#worlds .aanand h2','आधुनिक अंतरंगता'],
    ['#worlds .aanand p','गरिमा के साथ आनंद — शरीर-सुरक्षित उत्पाद, प्राकृतिक देखभाल और जोड़ों के लिए।'],
    ['#worlds .aanand .go','आनन्द में प्रवेश करें →'],
    ['#consult .consult h2','निजी डॉक्टर परामर्श, सिर्फ़ ₹99'],
    ['#consult .consult p','फ़ोन या वीडियो — अकेले या जीवनसाथी के साथ। पंजीकृत डॉक्टर कारण समझकर 24 घंटे में आपका प्लान लिखते हैं। आपकी बात कॉल से बाहर नहीं जाती।'],
    ['#science .intro h2','उनका आनंद विज्ञान है, रहस्य नहीं'],
    ['#science .intro p','आधुनिक यौन-स्वास्थ्य विज्ञान उत्तेजना को समझने-समझाने की चीज़ मानता है — खुलकर, साथ मिलकर।'],
    ['#bundleH2','कोई भी 2, 3 या 4 चुनें — 20% तक बचत'],
    ['#bundleSub','जो आप दोनों को ठीक लगे वही चुनें। 2 चीज़ें — 10% छूट · 3 चीज़ें — 15% · 4 या अधिक — 20%। छूट कार्ट में अपने आप दिखती है।'],
    ['#quiz span','उलझन में हैं? कुछ सवालों के जवाब दें — अपना प्लान पाएं।'],
    ['#quiz button','सेल्फ़-चेक शुरू करें →'],
    ['#faq .intro h2','जो सवाल सब पूछते हैं'],
    ['.final h2','खुल के इलाज कराइए। खुल के प्यार कीजिए।'],
    ['.final p','दोनों के लिए एक भरोसेमंद घर — आयुर्वेदिक स्वास्थ्य और आधुनिक अंतरंगता, हमेशा निजी, कभी शर्म नहीं।']
  ];
  if(window.KKP_I18N_PAGE)I18N=I18N.concat(window.KKP_I18N_PAGE);
  var stepsHi=[['निजी तौर पर पूछें','₹99 का परामर्श बुक करें। न क्लिनिक, न लाइन, न किसी की नज़र।'],['सही निदान पाएं','पंजीकृत डॉक्टर कारण देखते हैं — सिर्फ़ लक्षण नहीं।'],['अपना प्लान पाएं','आपके मामले के अनुसार औषधियाँ, अभ्यास और कोर्स।'],['फ़ॉलो-अप से सुधारें','तय फ़ॉलो-अप से प्लान तब तक बदलता है जब तक असर न दिखे।']];
  var lang='en';
  try{lang=localStorage.getItem('kkp_lang')||'en';}catch(e){}
  var langBtn=$('langTgl');
  function applyLang(){
    I18N.forEach(function(pair){
      var el=document.querySelector(pair[0]);if(!el)return;
      if(el.__en===undefined)el.__en=el.innerHTML;
      el.innerHTML=lang==='hi'?pair[1]:el.__en;
    });
    document.querySelectorAll('.steps .step').forEach(function(st,i){
      if(i>=stepsHi.length)return;
      var h=st.querySelector('h4'),p=st.querySelector('p');
      if(h.__en===undefined){h.__en=h.innerHTML;p.__en=p.innerHTML;}
      h.innerHTML=lang==='hi'?stepsHi[i][0]:h.__en;p.innerHTML=lang==='hi'?stepsHi[i][1]:p.__en;
    });
    document.querySelectorAll('.addbtn').forEach(function(b){
      if(b.__en===undefined)b.__en=b.textContent;
      b.textContent=lang==='hi'?(b.__en.indexOf('consult')>-1||b.__en.indexOf('Book')>-1?'परामर्श बुक करें':'कार्ट में डालें'):b.__en;
    });
    if(langBtn)langBtn.textContent=lang==='hi'?'English':'हिंदी';
    document.documentElement.lang=lang==='hi'?'hi':'en';
    try{localStorage.setItem('kkp_lang',lang);}catch(e){}
    window.dispatchEvent(new CustomEvent('kkp:lang',{detail:lang}));
  }
  if(langBtn)langBtn.addEventListener('click',function(){lang=lang==='hi'?'en':'hi';applyLang();});
  if(lang==='hi')applyLang();

  /* ===== reveal on scroll ===== */
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var targets = document.querySelectorAll('.catrow, .band, .aan-hero, .consult, .cmp, .faq, .herbs .intro, .steps, .worlds, .science .intro');
  if (!reduce && 'IntersectionObserver' in window && targets.length) {
    targets.forEach(function(el){ el.classList.add('reveal'); });
    var obs = new IntersectionObserver(function(entries){
      entries.forEach(function(e){ if (e.isIntersecting){ e.target.classList.add('in'); obs.unobserve(e.target); } });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    targets.forEach(function(el){ obs.observe(el); });
  }

  render();
})();
