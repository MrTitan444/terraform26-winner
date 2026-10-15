/* =========================================================
   TERRAFORM — crop guide (PLACEHOLDER CONTENT)
   Plain words only. Sizes are hand measures:
     finger-length · hand's span · hand's depth · knee-high · pace
   Time is in weeks, with "moons" (about 4 weeks) shown beside it.
   The back end can replace window.TF_CROPS with real data later.
   ========================================================= */
const ic=(p)=>'<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">'+p+'</svg>';
window.TF_ICONS = {
  pod:   ic('<path d="M10 44C14 22 34 10 54 12 52 34 34 52 10 44z"/><circle cx="24" cy="34" r="3"/><circle cx="33" cy="28" r="3"/><circle cx="42" cy="22" r="3"/><path d="M10 44L4 52"/>'),
  gourd: ic('<path d="M32 16c-14 0-24 8-24 20s10 18 24 18 24-6 24-18-10-20-24-20z"/><path d="M32 16c-8 4-10 12-10 20s2 14 10 18M32 16c8 4 10 12 10 20s-2 14-10 18"/><path d="M32 16c0-4 2-8 6-10"/>'),
  corn:  ic('<path d="M32 8c-8 8-10 20-8 32 2 8 6 14 8 16 2-2 6-8 8-16 2-12 0-24-8-32z"/><path d="M26 22h12M25 30h14M25 38h14M27 46h10M32 8v48"/><path d="M24 54c-8-4-12-12-12-22M40 54c8-4 12-12 12-22"/>'),
  tomato:ic('<circle cx="32" cy="36" r="20"/><path d="M32 16l-6-6M32 16l6-6M32 16l-10 2M32 16l10 2M32 16v-8"/>'),
  cabbage:ic('<circle cx="32" cy="34" r="22"/><path d="M32 12c-10 8-10 36 0 44M32 12c10 8 10 36 0 44M12 34c10-8 30-8 40 0"/>'),
  leaf:  ic('<path d="M12 52C10 28 26 10 54 10 54 38 38 54 12 52z"/><path d="M12 52L40 24M26 38l-2-12M34 30l-10-4M36 40l12-2"/>'),
  root:  ic('<path d="M22 8c4 4 6 8 10 8s6-4 10-8M32 16c-9 0-14 7-12 16 2 9 8 20 12 26 4-6 10-17 12-26 2-9-3-16-12-16z"/><path d="M26 30l-6 4M38 38l6 3M30 46l-4 4"/>'),
  grass: ic('<path d="M32 58V20M32 58C30 44 24 34 14 24M32 58c2-14 8-24 18-34M32 58C28 48 18 42 8 40M32 58c4-10 14-16 24-18"/><path d="M32 20c-3-5-2-9 0-12 2 3 3 7 0 12z"/>')
};
window.TF_PHASE_COLORS = ['#0c1670','#7a7fb8','#f2563a','#5aa83a','#2f7d32','#ff7a3d','#1a2bd0'];

/* the four jobs in the planting cycle */
window.TF_STAGES = {
  1:['Hungry plants','Take a lot from the soil. Go first, in a fresh, rich bed.'],
  2:['Gentle plants','Take less. Grow them next, on what is left.'],
  3:['Soil builders','The bean family. They give goodness back to the soil.'],
  4:['Rest-season plants','Chopped and left in place to feed the bed before the cycle starts again.']
};
window.TF_ROLE = {hungry:'Hungry plant',gentle:'Gentle plant',soil:'Soil builder',rest:'Rest-season plant'};

window.TF_CROPS = [
 {
  slug:'bush-beans', name:'Bush Beans', icon:'pod', hue:['#c4e04a','#5aa83a'], role:'soil', stage:3, grows:'above',
  tagline:'Quick, filling food that also feeds the soil while it grows.',
  tags:['Beginner friendly','Easy to save seed'],
  weeks:{sprout:1,grow:5,ripen:3,harvest:3}, sowWhen:'When the nights stop being cold',
  where:'Raised bed or deep container. Sun most of the day.',
  seeds:'Two seeds in each hole', depth:2, depthLabel:'2 finger-lengths deep', apart:1, apartLabel:'1 hand’s span apart', extra:'No support needed.',
  steps:[['Wet the bed','Water the bed the evening before. The top should be damp, not muddy.'],['Poke the holes','Make holes two finger-lengths deep, one hand’s span apart.'],['Drop in two seeds','Cover the hole and press down gently with your palm.'],['Water softly','Use a cup or a can with holes so the seeds don’t wash out.'],['Thin if needed','If both seeds come up, pinch off the weaker one.']],
  care:[['Days 1–7','Water','Keep the top damp. About a cupful per hole every 2 days.'],['Weeks 2–5','Weeds','Pull weeds by hand. Spread dry grass around the plants to keep water in.'],['Weeks 5–8','Watch for bugs','Look under the leaves each morning for chewed holes.'],['Weeks 6–9','Flowering','Water at the base only. Never splash the flowers.']],
  harvest:{signs:'Pods are plump and snap cleanly when you bend them.',how:'Pick every 2–3 days. Hold the stem with one hand and pull the pod with the other. The more you pick, the more they make.',keep:'Leave a few pods on the plant until they are dry and rattle. Those seeds are next season’s crop.',value:'Filling food that dries and stores for many moons.'}
 },
 {
  slug:'peas', name:'Peas', icon:'pod', hue:['#5aa83a','#0c1670'], role:'soil', stage:3, grows:'above',
  tagline:'Love cool weather, climb on sticks, and leave the soil richer.',
  tags:['Cool weather','Feeds the soil'],
  weeks:{sprout:1,grow:6,ripen:4,harvest:3}, sowWhen:'In cool weather, as soon as the ground can be worked',
  where:'Raised bed with sticks to climb. Half to most of the day in sun.',
  seeds:'One seed per hole', depth:2, depthLabel:'2 finger-lengths deep', apart:0.5, apartLabel:'Half a hand’s span apart', extra:'Push waist-high sticks in beside them.',
  steps:[['Set the climbing sticks','Push branchy sticks, waist-high, along the row.'],['Poke the holes','Two finger-lengths deep, half a hand’s span apart.'],['Drop in one seed each','Cover and press down.'],['Water softly','Keep the top damp until they sprout.'],['Guide the shoots','When they are a hand tall, tuck them toward the sticks.']],
  care:[['Weeks 1–2','Water','Keep the top damp, never soggy.'],['Weeks 3–6','Weeds & support','Weed by hand. Tie loose shoots to the sticks with grass.'],['Weeks 6–9','Watch for white powder','If you see it, use the milk wash on the Care page.'],['Weeks 8–11','Water at flowering','Water the base in the morning.']],
  harvest:{signs:'Pods are fat and shiny but still bright green.',how:'Pick with two hands so you don’t pull the plant. Pick every day or two once they start.',keep:'Let the last pods dry on the plant for seed.',value:'Sweet, quick food. Eat fresh or dry for later.'}
 },
 {
  slug:'pumpkin-squash', name:'Pumpkin & Squash', icon:'gourd', hue:['#ff7a3d','#f2563a'], role:'hungry', stage:1, grows:'above',
  tagline:'One plant can fill a shelf. Needs room and a rich bed.',
  tags:['Stores for moons','Big harvest'],
  weeks:{sprout:1,grow:8,ripen:7,harvest:4}, sowWhen:'When nights are warm',
  where:'Big raised bed or a clean mound. Full sun, with room to sprawl.',
  seeds:'Three seeds on a small hump', depth:2, depthLabel:'2 finger-lengths deep', apart:10, apartLabel:'2 paces between plants', extra:'Let the vines spread, or guide them over a fence.',
  steps:[['Make a hump','Pile the growing mix into a hump about a hand’s depth high.'],['Plant three seeds','Push each in two finger-lengths deep, a thumb’s width apart.'],['Water well','Soak the hump, then let the top dry a little between waterings.'],['Keep the strongest','When two real leaves show, pinch off all but the strongest.'],['Give it room','Leave two paces to the next plant.']],
  care:[['Weeks 1–3','Water','Water the base every 2 days. Keep leaves dry.'],['Weeks 3–8','Weeds & mulch','Pull weeds. Lay dry grass around the hump.'],['Weeks 8–12','Feed','Give weed tea every 10 suns (see the Care page).'],['Weeks 12–16','Ripening','Turn fruit gently so it ripens evenly. Slide a flat stone under it.']],
  harvest:{signs:'The skin is hard (your thumbnail can’t dent it) and the stem is dry and woody.',how:'Cut the stem with a sharp blade, leaving a hand’s length of stem on the fruit.',keep:'Store in a cool dry place. They keep for many moons. Seeds are good to eat and to replant.',value:'Very filling. The most food for the least work.'}
 },
 {
  slug:'dwarf-corn', name:'Dwarf Corn', icon:'corn', hue:['#ff7a3d','#c4e04a'], role:'hungry', stage:1, grows:'above',
  tagline:'Short corn that fits a raised bed and stores well when dried.',
  tags:['Dries for storage','Grows in blocks'],
  weeks:{sprout:1,grow:6,ripen:6,harvest:2}, sowWhen:'When nights are warm',
  where:'Raised bed in a small square. Full sun.',
  seeds:'Two seeds per hole', depth:2, depthLabel:'2 finger-lengths deep', apart:1, apartLabel:'1 hand’s span apart', extra:'Plant in a small square, not one long line, so the ears fill out.',
  steps:[['Mark a square','Plant at least four rows by four plants.'],['Poke the holes','Two finger-lengths deep, one hand’s span apart.'],['Drop in two seeds','Cover and press down.'],['Water well','Keep it damp until they come up.'],['Thin and hill up','Keep the strongest. Pile a little mix around each stem when knee-high.']],
  care:[['Weeks 1–3','Water','Keep damp. Water the base.'],['Weeks 3–8','Feed','Weed tea every 10 suns. Corn is hungry.'],['Weeks 6–10','Watch for bugs','Pick caterpillars by hand in the morning.'],['Weeks 10–13','Ripening','Stop watering when the husks go papery.']],
  harvest:{signs:'Silk at the top has turned dry and brown. A kernel squirts milky juice when pressed.',how:'Bend the ear down and twist it off. For storing, leave it on the stalk until the husk is dry and the kernels are hard.',keep:'Hang dried ears in a dry, airy place. Keep a few of the best ears for seed.',value:'Filling, long-keeping food.'}
 },
 {
  slug:'tomatoes', name:'Tomatoes', icon:'tomato', hue:['#f2563a','#ff7a3d'], role:'hungry', stage:1, grows:'above',
  tagline:'Worth the wait. Start as seedlings and keep them tied up.',
  tags:['Vitamin rich','Needs sticks'],
  weeks:{sprout:2,grow:8,ripen:8,harvest:6}, sowWhen:'Start seedlings in a warm, sheltered spot. Move out when nights are mild',
  where:'Deep raised bed or large container. Sun most of the day.',
  seeds:'One seedling per hole', depth:4, depthLabel:'Bury up to the first leaves', apart:5, apartLabel:'1 pace apart', extra:'Tie to a waist-high stick or more.',
  steps:[['Start seedlings','Sow seeds in a cup of clean mix. Keep it warm and bright.'],['Dig a deep hole','Make it deep enough to bury the stem up to the first leaves.'],['Plant and firm','Set the seedling in, cover, press down.'],['Add a stick','Push a tall stick in beside it and tie loosely with grass.'],['Water at the base','Morning is best. Keep leaves dry.']],
  care:[['Weeks 1–3 after planting','Shock watch','If it stalls, cover with a cut plastic jug for a few days.'],['Weeks 3–8','Tie up','Tie new growth to the stick each week.'],['Weeks 6–12','Feed','Weed tea every 10 suns.'],['Weeks 10–16','Water evenly','Don’t let the bed dry out then flood it. It splits fruit.']],
  harvest:{signs:'Fully coloured all the way round and slightly soft when pressed.',how:'Hold the stem and tip the fruit up until it snaps off.',keep:'Scoop seeds from your best fruit, rinse, and dry on paper.',value:'Vitamin-rich fruit that you can eat fresh or dry.'}
 },
 {
  slug:'cabbage', name:'Cabbage', icon:'cabbage', hue:['#2f7d32','#c4e04a'], role:'hungry', stage:1, grows:'above',
  tagline:'A solid, filling head that handles cool weather.',
  tags:['Cool weather','Keeps well'],
  weeks:{sprout:1,grow:9,ripen:5,harvest:2}, sowWhen:'In cool weather',
  where:'Rich raised bed. Sun most of the day.',
  seeds:'Two seeds per hole', depth:1, depthLabel:'1 finger-length deep', apart:2, apartLabel:'2 hand’s spans apart', extra:'Needs steady water.',
  steps:[['Make rich soil','Mix extra compost into the top of the bed.'],['Poke the holes','One finger-length deep, two hand’s spans apart.'],['Drop in two seeds','Cover and press down.'],['Thin to one','Keep the strongest plant per hole.'],['Water steadily','Keep the top damp.']],
  care:[['Weeks 1–4','Water','Keep the top damp.'],['Weeks 4–10','Caterpillars','Pick them off by hand every morning. Dust with dry wood ash.'],['Weeks 6–12','Feed','Weed tea every 10 suns.'],['Weeks 12–15','Heads','Stop watering if heads start to split.']],
  harvest:{signs:'The head feels firm when you squeeze it.',how:'Cut the head at the base with a sharp knife. Leave the stump. It may grow small heads.',keep:'Store in a cool place for a few moons.',value:'Big, filling, long-lasting.'}
 },
 {
  slug:'chard', name:'Chard', icon:'leaf', hue:['#5aa83a','#f2563a'], role:'gentle', stage:2, grows:'leaf',
  tagline:'Keeps giving leaves for moons. Forgiving and tough.',
  tags:['Beginner friendly','Picks all season'],
  weeks:{sprout:2,grow:6,ripen:0,harvest:10}, sowWhen:'Cool to warm weather',
  where:'Raised bed or container. Works in half-shade.',
  seeds:'Three seeds per hole', depth:1, depthLabel:'1 finger-length deep', apart:1, apartLabel:'1 hand’s span apart', extra:'No support needed.',
  steps:[['Soak the seeds','Leave seeds in water for a night to help them sprout.'],['Poke the holes','One finger-length deep, one hand’s span apart.'],['Drop in three seeds','Cover and press down.'],['Thin to the strongest','Keep the best one when they are a hand tall.'],['Water softly','Keep damp until they come up.']],
  care:[['Weeks 1–3','Water','Keep damp.'],['Weeks 3–8','Weeds','Weed by hand. Dry grass around the base.'],['Weeks 8+','Pick often','Picking makes it grow more leaves.'],['Any time','Watch for bugs','Pick off holes-makers by hand.']],
  harvest:{signs:'Outer leaves are as long as your hand.',how:'Pick the outer leaves. Leave the middle to keep growing.',keep:'Let one plant flower and dry for seed.',value:'Leaves rich in vitamins. Comes back again and again.'}
 },
 {
  slug:'kale', name:'Kale', icon:'leaf', hue:['#0c1670','#5aa83a'], role:'gentle', stage:2, grows:'leaf',
  tagline:'Hardy leaves that stand through the cold.',
  tags:['Cold hardy','Vitamin rich'],
  weeks:{sprout:2,grow:7,ripen:0,harvest:12}, sowWhen:'Cool weather',
  where:'Raised bed. Sun or half-shade.',
  seeds:'Two seeds per hole', depth:1, depthLabel:'1 finger-length deep', apart:2, apartLabel:'2 hand’s spans apart', extra:'Watch for caterpillars.',
  steps:[['Poke the holes','One finger-length deep, two hand’s spans apart.'],['Drop in two seeds','Cover and press down.'],['Thin to one','Keep the strongest.'],['Water softly','Keep damp.'],['Mulch','Lay dry grass around each plant.']],
  care:[['Weeks 1–3','Water','Keep damp.'],['Weeks 3–9','Caterpillars','Pick them off in the morning.'],['Weeks 9+','Pick lower leaves','Take from the bottom up.'],['Cold nights','Cover','Throw dry grass over on the coldest nights.']],
  harvest:{signs:'Leaves are as big as your hand.',how:'Pick the lowest leaves first and leave the top to keep growing.',keep:'Leave one plant to flower for seed.',value:'A steady supply of vitamin-rich leaves.'}
 },
 {
  slug:'sweet-potato', name:'Sweet Potato', icon:'root', hue:['#ff7a3d','#0c1670'], role:'gentle', stage:2, grows:'under',
  tagline:'Filling, long-keeping food. Grows underground, so clean beds only.',
  tags:['Grows underground','Clean mound only'],
  weeks:{sprout:2,grow:10,ripen:6,harvest:2}, sowWhen:'When nights are warm',
  where:'A clean, knee-high mound or deep container filled with outside soil. Full sun.',
  seeds:'One slip per hole', depth:3, depthLabel:'Bury half of the slip', apart:3, apartLabel:'3 hand’s spans apart', extra:'Never plant in the site ground.',
  steps:[['Make slips','Rest a sweet potato in a jar of water. When shoots grow, twist them off.'],['Build a clean mound','Fill it knee-high with outside soil and compost.'],['Plant the slips','Bury half of each slip. Firm the soil.'],['Water in','Water well for the first week.'],['Let it trail','Let the vines spread.']],
  care:[['Week 1','Water','Water daily.'],['Weeks 2–8','Weeds','Pull weeds. Lay dry grass around the plants.'],['Weeks 8–14','Water','Water less once vines cover the mound.'],['Weeks 14–18','Wait','Leaves start to yellow when ready.']],
  harvest:{signs:'Leaves yellow and the mound cracks a little.',how:'Dig gently with your hands, a hand’s span out from the stem.',keep:'Let them sit in a warm, dry place for a few suns, then store in a cool place.',value:'Heavy, filling, keeps for many moons.'}
 },
 {
  slug:'buckwheat', name:'Buckwheat', icon:'grass', hue:['#7a7fb8','#c4e04a'], role:'rest', stage:4, grows:'above',
  tagline:'A quick rest crop. Chop it in place to feed the bed.',
  tags:['Rest-season','Heals the bed'],
  weeks:{sprout:1,grow:5,ripen:2,harvest:0}, harvestLabel:'Chop and leave in place', sowWhen:'Any warm time between crops',
  where:'Any bed between harvests. Sun or half-shade.',
  seeds:'Scatter by the handful', depth:1, depthLabel:'Rake in a finger-length deep', apart:0, apartLabel:'No spacing, scatter thickly', extra:'Chop before the seeds fall.',
  steps:[['Clear the bed','Pull out old plants and shake the roots over the bed.'],['Scatter by the handful','Spread seeds thickly over the top.'],['Rake lightly','Rake the seeds in one finger-length deep.'],['Water','Keep it damp until it sprouts.'],['Chop and drop','When it flowers, chop it and leave it on the bed.']],
  care:[['Week 1','Water','Keep damp until it sprouts.'],['Weeks 2–6','Leave it','It needs almost nothing.'],['Weeks 6–7','Chop time','Chop when most plants are in flower.'],['Week 8','Rest','Leave the chopped plants on the bed for a week before the next crop.']],
  harvest:{signs:'Most plants are covered in white flowers.',how:'Cut the plants at the base and leave them lying on the bed.',keep:'Let a few go to seed if you want to replant.',value:'Feeds the bed and prepares it for the next crop.'}
 }
];
