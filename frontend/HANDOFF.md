# TERRAFORM — Handoff Capsule

Paste the **"Starter prompt"** (bottom of this file) into a new Claude conversation and attach this whole zip (or at least `site/`, `source/build.py`, `references/`).

## 1. What this project is
A 9-page, **front-end only** website called **Terraform** for recovering damaged post-industrial land (originally framed as "contamination + compaction"; now rewritten for ordinary people with **no scientific terms**). The back end will be built later on a different device. No web knowledge was to be used. Only design and front-end.

## 2. The user's requests, in order
1. 9-page site, topic: degraded post-industrial land (contamination & compaction). Front-end design only. Pages must include: **login page, input screen (problems entered), missing analysis, protocol (problem solving), next action, types of crops (10 boxes), each box leading to its own pages: timeframe, planting method, ongoing care, harvest.**
2. Theme and typography taken from the reference screenshot ("elsewhere." travel site): bold electric blue, cream, sunset orange, halftone dots, pill buttons, high-contrast display serif + tracked uppercase sans. **"terraform." wordmark top-left** in the same style as "elsewhere.". Do NOT use the mountain image anywhere. **Use the single-tree sunset photo as the background** (it was uploaded sideways; rotated upright).
3. "Run it locally" (twice). The session could not reach their computer, so a hosted preview artifact and a downloadable zip were provided instead.
4. **Remove the sign-in page**: no password or login ID. Just simple text and a button to open the site. Add **quotes about not giving up (hope)** on every page.
5. Optimise the whole site using the attached knowledge base (`references/knowledge-base.txt`): **no scientific terms**, easy for normal humans; hand-based measurements only.
6. This capsule: export everything for transfer to a different Claude conversation.

## 3. Current state (all done and working)
- Welcome page replaces login: "Heal Ground. Grow Again." + "Open Terraform" button + 4 ground-rule cards.
- 9 pages (files in `site/`):
  1. `index.html` Welcome
  2. `input.html` Describe your land (what you see/smell/feel + 8 hand checks; "Not checked yet" default)
  3. `analysis.html` What's missing (repeats user's words back, land type from 5 kinds, Danger/Careful verdict, unchecked checks with how-to, "what these checks can't tell you")
  4. `protocol.html` Step-by-step fix (Raised bed / Deep containers; barrier, knee-high walls, log core, growing mix recipe, rest; cross-section drawing; tick-off progress)
  5. `next-action.html` Next action (recommended step, 3 readiness checks: puddle/warmth/sprout, Today / This week / This moon board)
  6. `crops.html` 10 crop boxes with filter (Feed the soil / Hungry / Gentle / Rest-season) and safety banner
  7. `timeframe.html?crop=slug` How long it takes (weeks + moons, chart)
  8. `planting.html?crop=slug` How to plant (finger-lengths, hand's spans, soil-profile drawing, steps)
  9. `care-harvest.html?crop=slug` Care & harvest (week-by-week care, "something looks wrong?" fix table, harvest signs, rotation cycle)
- Hope quote card on every page ("Keep going"), all original unattributed lines (list is `QUOTES` in `source/build.py`).
- 10 crops: Bush Beans, Peas, Pumpkin & Squash, Dwarf Corn, Tomatoes, Cabbage, Chard, Kale, Sweet Potato (clean mound only), Buckwheat (rest crop).
- Hand-guide overlay (finger-length, hand's span ≈20 cm, hand's depth, knee-high ≈45–50 cm, pace ≈1 m, bucketful ≈10 L, sun = day, moon ≈4 weeks).
- Verified: no console errors, all links resolve, login→input→analysis→crops flow works, no leftover jargon.

## 4. Design system (keep consistent)
- Colours: blue `#1a2bd0`, deep blue `#0c1670`, ink `#080f4d`, cream `#fdf0dc`, orange `#ff7a3d`, coral `#f2563a`, lime `#c4e04a`, leaf `#5aa83a`.
- Fonts: **Fraunces** (display, weight 700, tight tracking) + **Inter** (uppercase tracked labels), via Google Fonts link (needs internet; falls back to Georgia).
- Background: `assets/img/tree.jpg` (rotated upright single-tree sunset) under a blue wash + halftone dot layer. Never use the mountain image.
- Pill buttons, cream cards, sticky header with `terraform.` wordmark, burger menu overlay, bottom bar with step counter (01/06 …) and prev/next arrows.

## 5. How it is built
- `source/build.py` generates the 9 HTML files: `python3 source/build.py site/` (writes into the output folder you pass).
- `site/assets/css/style.css`, `site/assets/js/app.js` (behaviour + knowledge: hand checks, land types, signs, protocol, fixes), `site/assets/js/crops-data.js` (all crop content; replace with API data later).
- Persistence is `localStorage` only (keys: `tf_site`, `tf_protocol`, `tf_ready`, `tf_tasks`). Back-end hook points are marked `// BACKEND:` in `app.js`.
- Preview hosting: the site was also published as a private claude.ai artifact (multi-file). The welcome page there has its `<html>/<head>/<body>` wrapper stripped and sets `document.body.className="bright"` and `data-page="welcome"` by script. Re-create that if republishing.

## 6. Non-negotiable rules from the knowledge base (never break these)
1. **No scientific readings or terms**: never ask for pH, nutrient numbers, conductivity, moisture %, spore counts, "bulk density", etc.
2. Only everyday human measures: handful, two cupped palms, bucketful, wheelbarrow-load; finger-length, hand's span, hand's depth, knee-high, waist-high, pace; suns, moons.
3. Safety first: unknown stains, rust, chemical smells, rubble = assume hazardous. No ground crops (carrots, potatoes, radishes, leafy greens) in suspect soil. Default remedy = physical barrier + knee-high raised beds or deep containers filled with outside material.
4. Faithfully restate what the person observed; explicitly list what has **not** been checked; state that the checks cannot detect hidden poisons (lead, arsenic, cadmium, odourless old sprays).

## 7. Known limits / possible next steps
- Fonts need internet on first load (could be bundled locally; npm was blocked in the session, so they were not).
- Crop text and timings are placeholder copy to be replaced by real data from the back end.
- The knowledge base also describes a back end (JSON data files, rule engine, optional offline AI, REST endpoints `/diagnose`, `/recommend-crops`, `/remedy-plan`, `/readiness`, `/troubleshoot`). That is **not built**; the front end could be wired to it later.
- Not yet done (optional): offline-ready font files, print view, translations, back-end hookup.

## 8. Starter prompt (paste this into the new chat)
> I'm continuing a project called **Terraform**: a 9-page, front-end-only website that guides people from bare, damaged post-industrial land to a safe first harvest, in plain language with no scientific terms and only hand measurements (finger-lengths, hand's spans, paces, buckets, suns, moons). I've attached a handoff capsule. Please read `HANDOFF.md` first, then `references/knowledge-base.txt`. The working site is in `site/` and its generator is `source/build.py`. Keep the existing design (blue, cream, orange, halftone dots, Fraunces + Inter, single-tree background, "terraform." wordmark top-left, hope quote on every page) and keep all safety rules in section 6. Don't use web knowledge. Don't add a login. Next I want you to: **[write your next request here]**
