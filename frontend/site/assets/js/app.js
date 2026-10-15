/* =========================================================
   TERRAFORM — front-end behaviour (no back end)
   Plain-language edition: no lab numbers anywhere.
   All saving goes through TF.store (localStorage, guarded).
   Back-end hook points are marked  // BACKEND:
   ========================================================= */
(function(){
'use strict';

/* ---------- tiny helpers ---------- */
const $  = (s,r=document)=>r.querySelector(s);
const $$ = (s,r=document)=>Array.from(r.querySelectorAll(s));
const esc = s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const mem = {};
const store = {
  get(k,d){try{const v=localStorage.getItem(k);return v==null?(k in mem?mem[k]:d):JSON.parse(v)}catch(e){return k in mem?mem[k]:d}},
  set(k,v){mem[k]=v;try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}},
  del(k){delete mem[k];try{localStorage.removeItem(k)}catch(e){}}
};
const TF = window.TF = {store};
const page = document.body.dataset.page;
const filled = v => Array.isArray(v) ? v.length>0 : (v!==undefined && v!==null && String(v).trim()!=='');

/* ---------- overlays: menu + hand guide ---------- */
(function(){
  const show=id=>{const m=$('#'+id);if(m){m.classList.add('open');document.body.style.overflow='hidden'}};
  const hide=()=>{$$('.menu.open').forEach(m=>m.classList.remove('open'));document.body.style.overflow=''};
  const b=$('#burger'); if(b)b.addEventListener('click',()=>show('menu'));
  document.addEventListener('click',e=>{
    const o=e.target.closest('[data-open]'); if(o){e.preventDefault();hide();show(o.dataset.open);return}
    if(e.target.closest('[data-close]'))hide();
  });
  document.addEventListener('keydown',e=>{if(e.key==='Escape')hide()});
})();

/* =========================================================
   KNOWLEDGE: hand checks, land types, signs
   ========================================================= */
const CHECKS=[
 {k:'dig',label:'Dig a hand’s depth down',how:'Dig a small hole as deep as your hand. Look at what is under the top layer. Is it the same soil all the way, rubble, stained soil, or a hard layer?',opts:{same:'Same soil all the way',rubble:'Rubble or junk underneath',stained:'Smelly or stained soil underneath',hard:'A hard layer I couldn’t dig through'}},
 {k:'rainSmell',label:'Smell the ground after rain',how:'After the next rain, crouch down and smell the wet ground. Earthy is good. Sour, rotten-egg or fuel smells are warnings.',opts:{earthy:'Earthy',sour:'Sour or rotten',fuel:'Fuel or chemical',none:'No smell'}},
 {k:'drain',label:'Watch where rain water goes',how:'After rain, watch the puddles. Does the water soak in quickly, soak in slowly, or sit for days?',opts:{fast:'Soaks in quickly',slow:'Soaks in slowly',stands:'Sits for days'}},
 {k:'squeeze',label:'The squeeze test',how:'Squeeze a damp handful in your palm, then open your hand. Crumbles like breadcrumbs is good. A sticky strip longer than two thumb-joints is heavy clay. If it runs through your fingers it is loose sand.',opts:{crumbly:'Crumbles like breadcrumbs',ribbon:'Sticky strip (heavy clay)',runs:'Runs through my fingers (loose sand)'}},
 {k:'squish',label:'The squish test',how:'Squeeze a wet handful hard. Springing back like a sponge is healthy. Rock hard means worn out. Slimy means no air gets in.',opts:{sponge:'Springs back like a sponge',hard:'Rock hard',slimy:'Slimy'}},
 {k:'stick',label:'The stick push test',how:'Push a thumb-thick green stick straight down with your full body weight. Measure how far it went in using your hand. If it goes in less than a hand-width, the ground is packed too hard for roots.',opts:{deep:'More than a hand-width',shallow:'Less than a hand-width'}},
 {k:'jar',label:'The jar test',how:'Shake a handful of soil in a clear jar of rainwater. Let it settle for 100 breaths. Look at the top for a rainbow shine and smell it for fuel or chemicals.',opts:{clear:'Clear, no shine, no smell',sheen:'Rainbow shine or fuel smell'}},
 {k:'sprout',label:'The sprout test',how:'Fill one cup with soil from your site and one with clean rotted leaves or boiled soil. Plant the same fast-sprouting beans or wild seeds in both. After a few days, compare. Do the site seeds sprout worse, or have curled, blackened tips?',opts:{ok:'Both sprouted fine',poor:'Site cup is worse'}}
];
const LOOKS=[
 {k:'stains',label:'Look for stains on the ground',how:'Walk the ground slowly. Look for black, rainbow-shiny, rust-orange or white crusty patches.'},
 {k:'smells',label:'Smell the ground',how:'Crouch down and smell. Sour, rotten-egg, metallic or fuel smells are warnings.'},
 {k:'junk',label:'Look for junk on and in the ground',how:'Check for broken concrete or brick, rusty metal, glass, cinders, wires and pipes.'},
 {k:'plants',label:'Note what grows there',how:'Thistles or clumpy weeds, lush dark-green weeds, pale stunted weeds, moss, or nothing at all? Each tells a story.'}
];
const L={
 pastUse:{factory:'Factory or workshop',road:'Rail yard or road',rubble:'Knocked-down building',farm:'Old farm field',dump:'Rubbish tip',unknown:'I don’t know'},
 sun:{most:'Most of the day',half:'About half the day',shade:'Mostly shade'},
 water:{tap:'Tap or well close by',rain:'Rain barrel',stream:'Stream or pond',carry:'I carry it in buckets',none:'None yet'},
 stains:{black:'Black',rainbow:'Rainbow or oily shine',rust:'Rust-orange',white:'White crust',none:'None seen'},
 smells:{sour:'Sour',egg:'Rotten egg',metal:'Metallic',fuel:'Fuel or chemical',earthy:'Earthy, like after rain',none:'No smell'},
 junk:{rubble:'Concrete or brick pieces',metal:'Rusty metal',glass:'Broken glass',cinder:'Cinders or ash-like crumbs',pipes:'Wires or pipes',plastic:'Plastic or rubbish',none:'None'},
 plants:{thistle:'Thistles or clumpy weeds',lush:'Dark green, lush weeds',pale:'Pale, yellow, stunted weeds',moss:'Moss',bare:'Bare patches',nothing:'Nothing grows'}
};
const LAND={
 packed:{name:'Packed-down city ground',blurb:'Trodden on or driven over for years. Hard, with little air, and rain runs off it.',danger:'Roots can’t push through it.',fix:'Don’t try to dig it loose. Build a bed on top of it.'},
 rubble:{name:'Rubble and cinder ground',blurb:'Crushed concrete, brick or cinders. Very chalky, drains oddly, and may hide lead or old building dust.',danger:'Hidden poisons and dust.',fix:'Wet it before you touch it so no dust flies. Lay the barrier thick. Never burn or sweep the rubble.'},
 unknown:{name:'Ground of unknown safety',blurb:'Stains, strange smells, scrap metal or patchy weeds. We can’t tell what is in it.',danger:'Assume it is poisoned.',fix:'Seal it under the barrier. Grow only in raised beds or containers filled from outside.'},
 farm:{name:'Worn-out farm ground',blurb:'Crusted over, washed away, and tired from too many crops.',danger:'Very little food left in it.',fix:'Build a bed on top and fill it with rotted leaves and compost. Rest it with buckwheat between crops.'},
 sand:{name:'Sandy, gravelly washout',blurb:'Water and food drain straight through.',danger:'Nothing stays in it long enough to feed plants.',fix:'Build a bed with plenty of rotted leaves and compost so it holds water.'}
};
const FLAGS={
 dig:{rubble:['Junk underneath','Rubble below the top can hide poisons. Don’t dig it up. Cover it.','care'],stained:['Stained ground underneath','Poison may be in the soil. Seal it under the barrier.','danger'],hard:['A hard layer below','Roots can’t get through it. Build up, don’t dig down.','care'],same:['Same soil all the way','Easier to understand, but still not proven safe.','ok']},
 rainSmell:{sour:['Sour smell after rain','This is a warning sign. Treat the ground as unsafe.','danger'],fuel:['Fuel or chemical smell','This is a warning sign. Treat the ground as unsafe.','danger'],earthy:['Earthy smell after rain','A good sign, but not proof of safety.','ok'],none:['No smell after rain','A good sign, but not proof of safety.','ok']},
 drain:{stands:['Water sits for days','Roots would drown. Make sure your bed passes the puddle check.','care'],slow:['Water soaks in slowly','Build the bed with a log layer at the bottom to help it drain.','care'],fast:['Water soaks in quickly','Good drainage.','ok']},
 squeeze:{ribbon:['Heavy, sticky clay','Water won’t drain. Add lots of rotted leaves to your bed mix. Never work it when wet.','care'],runs:['Loose sand','Water and food drain away. Add rotted leaves and compost to your bed mix.','care'],crumbly:['Crumbly, healthy texture','This is the best kind.','ok']},
 squish:{hard:['Worn out and hard','Little life left in it. Don’t rely on it for growing.','care'],slimy:['Slimy, with no air','Roots would suffocate. Build above it.','care'],sponge:['Springy, like a sponge','A sign of rich soil.','ok']},
 stick:{shallow:['Packed too hard for roots','The stick went in less than a hand-width. Build a bed above it.','care'],deep:['Roots can push in','The stick went in more than a hand-width.','ok']},
 jar:{sheen:['Oil or fuel in the soil','A rainbow shine or fuel smell means pollution. Do not grow food in it.','danger'],clear:['No shine in the jar','A good sign, but it can’t see hidden poisons.','ok']},
 sprout:{poor:['Seeds struggle in the site soil','Black or curled tips are a warning. Don’t grow in it.','danger'],ok:['Seeds sprout fine in both cups','A good sign, but not proof of safety.','ok']}
};
const FIXES=[
 ['Growth stalls after moving the plant','Root shock or cold ground','Cover it with a cut plastic jug as a dome, or ring the stem with dry grass.'],
 ['Sudden wilting, but the soil is damp','The roots are drowning','Poke holes at the bed edge with a stick to let air in. Pull any mulch back from the stem.'],
 ['Tall, thin seedlings that flop over','Not enough light','Stand a white sheet or foil beside them to bounce light back.'],
 ['Holes chewed in leaves','Beetles or caterpillars','Pick them off by hand each morning. Dust the leaves with dry wood ash.'],
 ['Fine webbing under leaves, bronze speckles','Tiny mites','Crush garlic or wild onion in a jar of water. Flick it on with a leafy branch.'],
 ['White powder on leaves','A mould that spreads in damp air','Wash with 1 cup of milk or whey in a bucket of water, or a pinch of baking soda in a bucket.'],
 ['Yellow blotchy patterns on leaves','A sickness that spreads','Pull the plant out and burn it away from the garden. Never put it in the compost.'],
 ['Lower leaves go yellow first','The plant is hungry','Give it weed tea: nettles or weeds steeped 10 suns in a bucket of water, then diluted.'],
 ['Purple or red tint on stems and under leaves','Needs a boost from bone ash','Scatter a pinch of crushed bone from campfire-burnt bones.'],
 ['Scorched, curled leaf edges','Needs a boost from ash','Give it ash tea: a little cold hardwood ash soaked in water.'],
 ['Dark rot at the bottom of fruit, or dying tips','Needs a boost from eggshell','Water with crushed eggshells steeped in vinegar or rainwater.']
];
TF.CHECKS=CHECKS; TF.LAND=LAND;

/* ---------- reading what the person told us ---------- */
function classify(s){
  s=s||{};
  const stains=(s.stains||[]).filter(x=>x!=='none');
  const smells=(s.smells||[]).filter(x=>['egg','metal','fuel','sour'].includes(x));
  const junk=s.junk||[];
  const danger=!!(stains.length||smells.length||['sour','fuel'].includes(s.rainSmell)||s.jar==='sheen'||s.dig==='stained'||s.sprout==='poor'||junk.includes('metal')||junk.includes('pipes'));
  let type;
  if(danger)type='unknown';
  else if(junk.some(j=>['rubble','cinder','glass'].includes(j))||s.dig==='rubble'||s.pastUse==='rubble')type='rubble';
  else if(s.squeeze==='runs'||(s.drain==='fast'&&s.squeeze!=='ribbon'&&s.squeeze))type='sand';
  else if(s.pastUse==='farm')type='farm';
  else type='packed';
  return {type,danger};
}
function unchecked(s){
  s=s||{};
  return LOOKS.filter(x=>!filled(s[x.k])).map(x=>Object.assign({look:true},x)).concat(CHECKS.filter(x=>!filled(s[x.k])));
}
TF.classify=classify; TF.unchecked=unchecked;

/* =========================================================
   02 INPUT
   ========================================================= */
const SAMPLE = {
  siteName:'Old workshop yard',pastUse:'factory',paceLong:'24',paceWide:'12',sun:'most',water:'carry',
  stains:['rust','rainbow'],smells:['metal'],junk:['rubble','metal'],plants:['thistle','bare'],
  dig:'rubble',rainSmell:'',drain:'stands',squeeze:'ribbon',squish:'',stick:'shallow',jar:'',sprout:'',
  problems:'Bare, crusted ground with patches of dead weeds. Water sits for days after rain. Rust-coloured stains near the old furnace wall.'
};
TF.SAMPLE=SAMPLE;

if(page==='input'){
  const form=$('#site-form');
  const GROUPS=['stains','smells','junk','plants'];
  const setVal=(k,v)=>{
    if(GROUPS.includes(k)){$$('input[name="'+k+'"]',form).forEach(c=>c.checked=(v||[]).includes(c.value));return}
    const el=form.elements[k]; if(!el||el.type==='file')return; el.value=v;
  };
  const saved=store.get('tf_site',null);
  if(saved)Object.keys(saved).forEach(k=>setVal(k,saved[k]));
  const read=()=>{
    const d={};
    Array.from(form.elements).forEach(el=>{
      if(!el.name||el.type==='file'||el.type==='submit'||el.type==='button'||GROUPS.includes(el.name))return;
      d[el.name]=el.value;
    });
    GROUPS.forEach(g=>d[g]=$$('input[name="'+g+'"]:checked',form).map(c=>c.value));
    return d;
  };
  const toast=$('#save-msg');
  const say=t=>{toast.textContent=t;toast.style.opacity=1;clearTimeout(say.t);say.t=setTimeout(()=>toast.style.opacity=0,2400)};
  $('#btn-save').addEventListener('click',()=>{store.set('tf_site',read());say('Saved on this device')}); // BACKEND: PUT /patches/:id
  $('#btn-sample').addEventListener('click',()=>{Object.keys(SAMPLE).forEach(k=>setVal(k,SAMPLE[k]));say('Example filled in')});
  $('#btn-clear').addEventListener('click',()=>{form.reset();store.del('tf_site');say('Cleared')});
  form.addEventListener('submit',e=>{
    e.preventDefault();
    let ok=true,first=null;
    ['siteName','pastUse','problems'].forEach(n=>{
      const el=form.elements[n],bad=!el.value.trim();
      el.closest('.field').classList.toggle('bad',bad);
      if(bad&&!first)first=el; if(bad)ok=false;
    });
    if(!ok){first.focus();say('Please fill in the starred boxes');return}
    store.set('tf_site',read());
    location.href='analysis.html';
  });
}

/* =========================================================
   03 WHAT'S MISSING
   ========================================================= */
if(page==='analysis'){
  const s=store.get('tf_site',null);
  const empty=$('#empty'), body=$('#analysis-body');
  if(!s){empty.hidden=false;body.hidden=true}
  else{
    const list=(arr,map)=>(arr||[]).map(x=>map[x]||x).join(', ');
    const miss=unchecked(s), total=CHECKS.length+LOOKS.length, done=total-miss.length;
    $('#site-title').textContent=s.siteName||'Your patch';
    $('#ring').style.setProperty('--p',Math.round(done/total*100));
    $('#ring b').textContent=done+'/'+total;
    $('#readout').textContent = miss.length ? miss.length+' still to check. You can carry on, but the plan stays careful until you do them.' : 'Everything has been checked.';

    // verdict
    const c=classify(s), v=$('#verdict');
    v.classList.add(c.danger?'danger':'careful');
    $('#v-title').textContent=c.danger?'Danger: treat it as poisoned.':'Careful: treat it as unsafe.';
    $('#v-text').textContent=c.danger
      ?'Stains, smells, scrap metal or a bad check result point to poison in the ground. Do not plant in it, touch it bare-handed, or let children play on it. Seal it and grow above it.'
      :'Nothing you described looks poisoned, but our checks can’t see hidden poisons such as lead. Do not plant straight into it. Build a raised bed or use containers.';

    // restate (faithful, only what they said)
    const rows=[];
    const add=(k,v)=>rows.push('<dt>'+esc(k)+'</dt><dd>'+(v?esc(v):'<i>Not said</i>')+'</dd>');
    add('Used for before',L.pastUse[s.pastUse]);
    add('Size',(s.paceLong||s.paceWide)?[s.paceLong&&s.paceLong+' paces long',s.paceWide&&s.paceWide+' paces wide'].filter(Boolean).join(', '):'');
    add('Sun',L.sun[s.sun]); add('Water',L.water[s.water]);
    add('Stains',list(s.stains,L.stains)); add('Smells',list(s.smells,L.smells));
    add('Junk',list(s.junk,L.junk)); add('What grows',list(s.plants,L.plants));
    CHECKS.filter(x=>filled(s[x.k])).forEach(x=>add(x.label,x.opts[s[x.k]]));
    add('In your words',s.problems);
    $('#restate').innerHTML=rows.join('');

    // land type
    const t=LAND[c.type];
    $('#land-name').textContent=t.name; $('#land-blurb').textContent=t.blurb;
    $('#land-danger').textContent=t.danger; $('#land-fix').textContent=t.fix;

    // signs from checks done
    const LV={danger:['Danger','crit','var(--coral)'],care:['Careful','rec','var(--orange)'],ok:['Good sign','ok','var(--leaf)']};
    const flags=CHECKS.filter(x=>filled(s[x.k])&&FLAGS[x.k]&&FLAGS[x.k][s[x.k]]).map(x=>FLAGS[x.k][s[x.k]]);
    $('#flags').innerHTML=flags.length?flags.map(f=>'<li class="gap"><div class="ico" style="background:'+LV[f[2]][2]+'">'+(f[2]==='ok'?'✓':'!')+'</div><div><h4>'+esc(f[0])+'</h4><p>'+esc(f[1])+'</p></div><span class="tag '+LV[f[2]][1]+'">'+LV[f[2]][0]+'</span></li>').join('')
      :'<li class="gap"><div class="ico">–</div><div><h4>No checks done yet</h4><p>Do a few of the hand checks and the signs will show here.</p></div><span></span></li>';

    // not checked yet
    $('#unchecked').innerHTML=miss.length?miss.map(x=>'<details class="how" id="how-'+x.k+'"><summary>'+esc(x.label)+'</summary><p>'+esc(x.how)+'</p>'+(x.look?'<a class="link-u" href="input.html#f-'+x.k+'">Add it on the input page →</a>':'<a class="link-u" href="input.html#f-'+x.k+'">Record the result →</a>')+'</details>').join('')
      :'<p>Every check is done. Well done.</p>';
    const h=location.hash.slice(1); if(h){const d=document.getElementById(h);if(d&&d.tagName==='DETAILS'){d.open=true;d.scrollIntoView({block:'center'})}}
  }
}
/* how-to links from the input page land on the same details */
if(page==='analysis'&&!store.get('tf_site',null)){/* nothing to open */}

/* =========================================================
   04 STEP-BY-STEP FIX
   ========================================================= */
const PROTO={
 bed:[
  ['Walk the ground and clear it','Days 1–3',['Wear gloves and sturdy shoes.','Pick up big junk by hand and pile it to one side. Never put it in the bed.','Don’t dig or turn over the soil.'],'The patch is clear of big junk and you haven’t dug anything up.'],
  ['Lay the barrier','Days 3–5',['Wet three layers of cardboard, burlap or woven canvas.','Cover the whole patch, overlapping the edges by a hand’s span.','Weigh the edges down with stones.'],'No bare soil shows through.'],
  ['Build the walls knee-high','Week 1',['Stack salvaged stones or bricks until the wall reaches your knee.','Make the bed no wider than your arm can reach from either side, so you never have to step in it.','Fit the stones tightly so the mix can’t spill out.'],'The wall is knee-high all the way round with no big gaps.'],
  ['Fill the bottom with logs and branches','Week 1',['Fill the bottom half with rotting logs, thumb-thick branches and dry leaves.','Skip painted or treated wood.','Press it down with your feet.'],'The bottom half is full and firm, with no big hollows.'],
  ['Add the growing mix','Weeks 1–2',['For every pace of bed length: 2 buckets of rotted forest leaves, 1 bucket of crushed charcoal or cold campfire ash, and 2 buckets of compost.','Mix it with your hands or a spade and spread it to the top.','Use only clean material from outside. Never use soil from the damaged ground.'],'The mix is crumbly, dark, and smells like a forest floor.'],
  ['Let it rest','Week 2',['Leave the bed alone for 5 to 7 suns.','Then do the three readiness checks on the next page.'],'The back of your hand doesn’t feel hot when you press it into the mix.']
 ],
 box:[
  ['Find deep containers','Days 1–3',['Barrels, buckets or old tires all work.','Choose only ones that never held fuel, paint or chemicals.','Wash them out.'],'You have enough containers and they smell of nothing.'],
  ['Line them with canvas','Days 3–5',['Line the inside of each with woven canvas.','Make a few drain holes in the bottom so water can get out.'],'The canvas covers every side and the bottom still drains.'],
  ['Set them on a barrier','Week 1',['Stand them on wet cardboard or flat stones, not bare ground.','Put them where they get sun.'],'Containers are steady and don’t touch the bare ground.'],
  ['Fill the bottom half','Week 1',['Half-fill each container with rotting wood, thumb-thick branches and dry leaves.','Press it down.'],'The bottom half is full and firm.'],
  ['Add the growing mix','Weeks 1–2',['Fill the top with the same mix: about 2 parts rotted leaves, 1 part charcoal or cold ash, and 2 parts compost.','Use only clean material from outside.'],'The mix is crumbly, dark and smells like a forest floor.'],
  ['Let it rest','Week 2',['Leave the containers alone for 5 to 7 suns.','Then do the three readiness checks on the next page.'],'The back of your hand doesn’t feel hot when you press it into the mix.']
 ]
};
if(page==='protocol'){
  const s=store.get('tf_site',null);
  const done=store.get('tf_protocol',{});
  let track='bed';
  if(s){const t=LAND[classify(s).type];$('#land-tip').hidden=false;$('#tip-name').textContent=t.name;$('#tip-text').textContent=t.fix}
  const list=$('#steps');
  const check='<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5 9-10"/></svg>';
  function render(){
    $$('#seg button').forEach(b=>b.classList.toggle('on',b.dataset.t===track));
    const steps=PROTO[track];
    list.innerHTML=steps.map((st,i)=>{
      const key=track+'-'+i,d=!!done[key];
      return '<li class="step'+(d?' done':'')+'" data-k="'+key+'"><div class="no">'+String(i+1).padStart(2,'0')+'</div><div><h3>'+esc(st[0])+'</h3><div class="when">'+esc(st[1])+'</div><ul>'+st[2].map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul><div class="verify"><b>You’ll know it worked when</b>'+esc(st[3])+'</div></div><button class="done-btn" aria-label="Mark step '+(i+1)+' done" aria-pressed="'+d+'">'+check+'</button></li>';
    }).join('');
    const n=steps.filter((_,i)=>done[track+'-'+i]).length;
    $('#prog-bar').style.width=(n/steps.length*100)+'%';
    $('#prog-txt').textContent=n+' of '+steps.length+' steps done';
  }
  list.addEventListener('click',e=>{
    const li=e.target.closest('.step'); if(!li||!e.target.closest('.done-btn'))return;
    done[li.dataset.k]=!done[li.dataset.k]; store.set('tf_protocol',done); render();
  });
  $$('#seg button').forEach(b=>b.addEventListener('click',()=>{track=b.dataset.t;render()}));
  render();
}

/* =========================================================
   05 NEXT ACTION
   ========================================================= */
if(page==='next'){
  const s=store.get('tf_site',null);
  const pr=store.get('tf_protocol',{});
  const rd=store.get('tf_ready',{});
  const miss=s?unchecked(s):[];
  const cnt=t=>Object.keys(pr).filter(k=>k.indexOf(t+'-')===0&&pr[k]).length;
  const bed=Math.max(cnt('bed'),cnt('box'));
  const readyN=()=>['drain','heat','sprout'].filter(k=>rd[k]).length;

  function hero(){
    let title,text,href,cta;
    if(!s){title='Describe your land';text='Nothing has been entered yet. Tell us what you see so we can find the gaps.';href='input.html';cta='Describe your land'}
    else if(bed<6){title='Build your raised bed';text=bed?'You have done '+bed+' of 6 steps. Keep going.':'Cover the ground and build up from it. Start with step 1: walk the ground and clear it.';href='protocol.html';cta='Open the step-by-step fix'}
    else if(readyN()<3){title='Run the three readiness checks';text='Your bed is built. Before you plant, make sure it drains, isn’t hot, and sprouts seeds.';href='#ready-msg';cta='Jump to the checks'}
    else{title='Choose your first crop';text='Your bed is ready. Pick something quick and filling.';href='crops.html';cta='See the crops'}
    $('#ha-title').textContent=title; $('#ha-text').textContent=text; $('#ha-cta').href=href; $('#ha-cta-t').textContent=cta;
  }
  function stats(){
    $('#st-checks').textContent=miss.length; $('#st-bed').textContent=bed; $('#st-ready').textContent=readyN();
    const m=$('#ready-msg'),n=readyN();
    m.classList.toggle('good',n===3);
    m.innerHTML=n===3?'<div><b>Your bed is ready.</b> Go and choose a crop.</div>':'<div><b>Not yet.</b> '+(3-n)+' check'+(3-n>1?'s':'')+' left. Don’t plant until all three pass.</div>';
  }
  $$('.ready input').forEach(i=>{
    const k=i.id.slice(2); i.checked=!!rd[k]; i.closest('.ready').classList.toggle('on',i.checked);
    i.addEventListener('change',()=>{rd[k]=i.checked;store.set('tf_ready',rd);i.closest('.ready').classList.toggle('on',i.checked);hero();stats()});
  });
  hero(); stats();

  const first=miss.slice(0,2).map(x=>x.label.toLowerCase()).join(' and ');
  const T=[
    ['now','Do a hand check',first?'Next up: '+first:'All hand checks are done','Check'],
    ['now','Mark off the ground','Put up stakes or string. Keep children and animals out.','Safety'],
    ['now','Gather your materials','Cardboard, canvas, stones or bricks, rotting logs, dry leaves','Gather'],
    ['soon','Lay the barrier and build the bed','Steps 2 to 4 of the fix','Build'],
    ['soon','Fill the bed with the growing mix','Rotted leaves, charcoal or ash, compost','Build'],
    ['soon','Let the bed rest','5 to 7 suns. Leave it alone.','Wait'],
    ['later','Run the three readiness checks','Puddle, warmth and sprout checks','Check'],
    ['later','Choose a crop and sow','Pick from the 10 on the crops page','Plant'],
    ['later','Plan your next crop','Follow the rotation cycle so the bed stays rich','Plan']
  ];
  const ticks=store.get('tf_tasks',{});
  ['now','soon','later'].forEach(c=>{
    $('#col-'+c).innerHTML=T.map((t,i)=>[t,i]).filter(x=>x[0][0]===c).map(([t,i])=>
      '<label class="task'+(ticks[i]?' done':'')+'" data-i="'+i+'"><input type="checkbox"'+(ticks[i]?' checked':'')+'><div><h4>'+esc(t[1])+'</h4><p>'+esc(t[2])+'</p><div class="meta"><span class="tag opt">'+esc(t[3])+'</span></div></div></label>').join('');
  });
  $$('.col').forEach(col=>col.addEventListener('change',e=>{
    const l=e.target.closest('.task'); if(!l)return;
    ticks[l.dataset.i]=e.target.checked; l.classList.toggle('done',e.target.checked); store.set('tf_tasks',ticks);
  }));
}

/* =========================================================
   06 CROPS
   ========================================================= */
const moons=w=>{const m=Math.round(w/4*2)/2;return (m%1?m.toFixed(1):m)};
const crop1=c=>c.weeks.sprout+c.weeks.grow+c.weeks.ripen;
if(page==='crops'){
  const grid=$('#crops');
  grid.innerHTML=TF_CROPS.map((c,i)=>{
    const w=crop1(c)+2;
    return '<article class="crop" data-t="'+c.role+'">'+
      '<div class="art" style="background:linear-gradient(135deg,'+c.hue[0]+','+c.hue[1]+')"><span class="num">'+String(i+1).padStart(2,'0')+' / 10</span>'+TF_ICONS[c.icon]+'</div>'+
      '<div class="body"><h3><a href="timeframe.html?crop='+c.slug+'">'+esc(c.name)+'</a></h3><div class="sci">'+esc(TF_ROLE[c.role])+' · about '+moons(w)+' moons to first harvest</div><p>'+esc(c.tagline)+'</p>'+
      '<div class="tags">'+c.tags.map(t=>'<span class="tag">'+esc(t)+'</span>').join('')+'</div></div>'+
      '<nav class="quick" aria-label="'+esc(c.name)+' pages"><a href="timeframe.html?crop='+c.slug+'">How long</a><a href="planting.html?crop='+c.slug+'">Planting</a><a href="care-harvest.html?crop='+c.slug+'#care">Care</a><a href="care-harvest.html?crop='+c.slug+'#harvest">Harvest</a></nav></article>';
  }).join('');
  $$('.filters button').forEach(b=>b.addEventListener('click',()=>{
    $$('.filters button').forEach(x=>x.classList.toggle('on',x===b));
    const f=b.dataset.f;
    $$('.crop',grid).forEach(c=>c.classList.toggle('hide',f!=='all'&&c.dataset.t!==f));
  }));
}

/* =========================================================
   07–09 CROP PAGES
   ========================================================= */
if(['timeframe','planting','care'].includes(page)){
  const slug=new URLSearchParams(location.search).get('crop');
  const idx=Math.max(0,TF_CROPS.findIndex(c=>c.slug===slug));
  const c=TF_CROPS[idx], q='?crop='+c.slug, here=location.pathname.split('/').pop();
  document.title=c.name+' · '+({timeframe:'How long it takes',planting:'How to plant',care:'Care & harvest'}[page])+' · Terraform';
  $('#c-name').textContent=c.name;
  $('#c-sci').textContent=String(idx+1).padStart(2,'0')+' / 10';
  $('#c-tag').textContent=c.tagline;
  $('#c-role').textContent=TF_ROLE[c.role];
  if(c.grows==='under')$('#under-warn').hidden=false;
  $('#switch').innerHTML=TF_CROPS.map(x=>'<a href="'+here+'?crop='+x.slug+'"'+(x===c?' class="on"':'')+'>'+esc(x.name)+'</a>').join('');
  const sub=[['timeframe.html','How long','timeframe'],['planting.html','Planting','planting'],['care-harvest.html#care','Care','care'],['care-harvest.html#harvest','Harvest','harvest']];
  $('#subnav').innerHTML=sub.map(s=>{const [file,hash]=s[0].split('#');return '<a href="'+file+q+(hash?'#'+hash:'')+'"'+(page===s[2]||(page==='care'&&s[2]==='care')?' class="on"':'')+'>'+s[1]+'</a>'}).join('');
  const prev=TF_CROPS[(idx+9)%10], next=TF_CROPS[(idx+1)%10];
  $('#bar-prev').href=here+'?crop='+prev.slug; $('#bar-next').href=here+'?crop='+next.slug;
  $('#bar-count').textContent=String(idx+1).padStart(2,'0')+' / 10'; $('#bar-name').textContent=c.name;

  /* ----- how long ----- */
  if(page==='timeframe'){
    const w=c.weeks, cw=crop1(c);
    const ph=[['Clear the land and lay the barrier',1,2,'Pick junk by hand, lay the barrier'],['Build the bed and let it settle',1,2,'Fill it, then rest 5–7 suns'],['Seeds sprout',w.sprout,w.sprout,'First tiny leaves'],['Growing',w.grow,w.grow,'Leaves and stems fill out']];
    if(w.ripen)ph.push(['Filling out and ripening',w.ripen,w.ripen,'Fruit or pods form']);
    if(w.harvest)ph.push(['Harvest window',w.harvest,w.harvest,'Pick often']);
    else if(c.harvestLabel)ph.push([c.harvestLabel,1,1,'Chop at flowering']);
    ph.push(['Save seed and rest the bed',1,2,'Dry some seed, give the bed a break']);
    const total=ph.reduce((s,p)=>s+p[2],0);
    $('#f-total').textContent=(cw+2)+'–'+(cw+4)+' weeks';
    $('#f-moons').textContent=moons(cw+2)+'–'+moons(cw+4)+' moons';
    $('#f-sow').textContent=c.sowWhen;
    $('#f-first').textContent='About week '+cw+' after sowing';
    let at=0;
    $('#gantt').innerHTML=ph.map((p,i)=>{
      const left=at/total*100,wd=p[2]/total*100; at+=p[2];
      const lab=p[1]===p[2]?p[1]+(p[1]>1?' wks':' wk'):p[1]+'–'+p[2]+' wks';
      return '<div class="g-row"><div class="nm">'+esc(p[0])+'<small>'+esc(p[3])+'</small></div><div class="g-track"><div class="g-bar" style="left:'+left+'%;width:'+Math.max(wd,3.5)+'%;background:'+TF_PHASE_COLORS[i%7]+';animation-delay:'+(i*.08)+'s">'+(wd>14?lab:'')+'</div></div><div class="wk">'+lab+'</div></div>';
    }).join('');
    $('#g-axis').innerHTML='<div>Stage</div><div>'+[0,.25,.5,.75,1].map(f=>'<span>Wk '+Math.round(total*f)+'</span>').join('')+'</div><div style="text-align:right">Length</div>';
  }

  /* ----- how to plant ----- */
  if(page==='planting'){
    $('#sp-where').textContent=c.where; $('#sp-seeds').textContent=c.seeds; $('#sp-depth').textContent=c.depthLabel; $('#sp-space').textContent=c.apartLabel; $('#sp-extra').textContent=c.extra;
    $('#p-steps').innerHTML=c.steps.map(s=>'<li><div><b>'+esc(s[0])+'</b>'+esc(s[1])+'</div></li>').join('');
    const W=560,H=240,g=70,F=16, d=Math.min(c.depth,6)*F, sp=c.apart*2.5*F;
    let seeds='',span='';
    const n=c.apart===0?9:Math.max(2,Math.min(5,Math.floor((W-120)/Math.max(sp,1))+1));
    const startX=c.apart===0?70:(W-(n-1)*Math.min(sp,(W-120)/(n-1)))/2, stepX=c.apart===0?(W-140)/8:Math.min(sp,(W-120)/(n-1));
    for(let i=0;i<n;i++){const x=startX+i*stepX,y=g+(c.apart===0?(i%3)*8+10:d);seeds+='<line x1="'+x+'" y1="'+g+'" x2="'+x+'" y2="'+y+'" stroke="#fdf0dc" stroke-dasharray="3 4" opacity=".6"/><circle cx="'+x+'" cy="'+y+'" r="7" fill="#ff7a3d" stroke="#fdf0dc" stroke-width="2"/>'}
    if(c.apart>0){span='<path d="M'+startX+' '+(g-20)+'H'+(startX+stepX)+'M'+startX+' '+(g-26)+'v12M'+(startX+stepX)+' '+(g-26)+'v12" stroke="#fdf0dc" stroke-width="2" fill="none"/><text x="'+(startX+stepX/2)+'" y="'+(g-34)+'" fill="#fdf0dc" font-size="12" text-anchor="middle" font-family="Inter,sans-serif" font-weight="600">'+esc(c.apartLabel)+'</text>'}
    let ticks='';for(let i=0;i<=Math.min(c.depth,6);i++)ticks+='<line x1="18" y1="'+(g+i*F)+'" x2="34" y2="'+(g+i*F)+'" stroke="#fdf0dc" stroke-width="2"/>';
    $('#profile').innerHTML='<svg viewBox="0 0 '+W+' '+H+'" role="img" aria-label="Seeds planted '+esc(c.depthLabel)+', '+esc(c.apartLabel)+'"><rect width="'+W+'" height="'+g+'" fill="#1a2bd0"/><rect y="'+g+'" width="'+W+'" height="'+(H-g)+'" fill="#6b3f26"/><path d="M0 '+g+'H'+W+'" stroke="#c4e04a" stroke-width="5"/><line x1="26" y1="'+g+'" x2="26" y2="'+(g+Math.min(c.depth,6)*F)+'" stroke="#fdf0dc" stroke-width="2"/>'+ticks+seeds+span+'<text x="44" y="'+(g+d+30)+'" fill="#fdf0dc" font-size="12" font-family="Inter,sans-serif" font-weight="600">'+esc(c.depthLabel)+'</text></svg>';
  }

  /* ----- care & harvest ----- */
  if(page==='care'){
    $('#care-rows').innerHTML=c.care.map(r=>'<tr><td>'+esc(r[0])+'</td><td>'+esc(r[1])+'</td><td>'+esc(r[2])+'</td></tr>').join('');
    $('#fix-rows').innerHTML=FIXES.map(r=>'<tr><td>'+esc(r[0])+'</td><td>'+esc(r[1])+'</td><td>'+esc(r[2])+'</td></tr>').join('');
    const h=c.harvest;
    $('#h-signs').textContent=h.signs; $('#h-how').textContent=h.how; $('#h-keep').textContent=h.keep; $('#h-value').textContent=h.value;
    const nextStage=c.stage%4+1;
    $('#rot').innerHTML=[1,2,3,4].map(n=>'<li class="'+(n===c.stage?'on':'')+(n===nextStage?' next':'')+'"><b>'+n+'. '+esc(TF_STAGES[n][0])+'</b><span>'+esc(TF_STAGES[n][1])+'</span>'+(n===c.stage?'<em>This crop</em>':n===nextStage?'<em>Plant next</em>':'')+'</li>').join('');
  }
}

})();
