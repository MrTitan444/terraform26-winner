#!/usr/bin/env python3
"""Generates the 9 static HTML pages of the Terraform front end (plain-language edition).
Usage: python3 build.py <output_dir>"""
import sys, pathlib

OUT = pathlib.Path(sys.argv[1])

PAGES = [
    ("index.html", "Welcome"),
    ("input.html", "Describe your land"),
    ("analysis.html", "What’s missing"),
    ("protocol.html", "Step-by-step fix"),
    ("next-action.html", "Next action"),
    ("crops.html", "Choose a crop"),
    ("timeframe.html", "How long it takes"),
    ("planting.html", "How to plant"),
    ("care-harvest.html", "Care & harvest"),
]
NAV = [("input.html", "Your land."), ("analysis.html", "What’s missing."), ("protocol.html", "Step-by-step."),
       ("next-action.html", "Next action."), ("crops.html", "Crops.")]

PIN = '<svg width="20" height="26" viewBox="0 0 20 26" fill="#fdf0dc"><path d="M10 0C4.5 0 0 4.4 0 9.8 0 17 10 26 10 26s10-9 10-16.2C20 4.4 15.5 0 10 0zm0 13.5a3.7 3.7 0 110-7.4 3.7 3.7 0 010 7.4z"/></svg>'
CH_L = '<svg width="10" height="16" viewBox="0 0 10 16" fill="none" stroke="#fdf0dc" stroke-width="2"><path d="M8 1L2 8l6 7"/></svg>'
CH_R = '<svg width="10" height="16" viewBox="0 0 10 16" fill="none" stroke="#fdf0dc" stroke-width="2"><path d="M2 1l6 7-6 7"/></svg>'
WARN = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l10 18H2L12 3z"/><path d="M12 10v5M12 18v.01"/></svg>'

GUIDE = [
    ("A finger-length", "From the tip of your pointing finger to where it meets your hand."),
    ("A hand’s span", "Spread your hand wide, thumb tip to little-finger tip. About 20 cm."),
    ("A hand’s depth", "As deep as your hand is long. Used for digging."),
    ("Knee-high", "From the ground to your knee. About 45–50 cm."),
    ("Waist-high", "From the ground to your waist. Good for climbing sticks."),
    ("A pace", "One big step. About 1 metre."),
    ("A handful / two cupped palms", "What one hand holds / what two hands cupped together hold."),
    ("A bucketful", "A normal bucket, about 10 litres."),
    ("A wheelbarrow-load", "A full wheelbarrow."),
    ("A sun", "One day. “Ten suns” means ten days."),
    ("A moon", "One moon cycle, about 4 weeks."),
    ("100 breaths / 500 paces", "Used for short waits and walking times."),
]


def header(active):
    cur = ' aria-current="page"'
    nav = "".join(f'<a href="{h}"{cur if h == active else ""}>{t}</a>' for h, t in NAV)
    nav += '<a href="#" data-open="guide">Hand guide.</a>'
    menu = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in PAGES)
    guide = "".join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in GUIDE)
    return f'''
<div class="bg" aria-hidden="true"></div>
<header class="top">
  <a class="brand" href="index.html" aria-label="Terraform home">terraform.</a>
  <nav class="nav" aria-label="Primary">{nav}</nav>
  <div class="top-r">
    <a class="pill hide-s" href="input.html">Describe your land <span aria-hidden="true">↗</span></a>
    <button class="burger" id="burger" aria-label="Open menu"><i></i></button>
  </div>
</header>
<div class="menu" id="menu" role="dialog" aria-label="All pages">
  <div class="menu-top"><a class="brand" href="index.html">terraform.</a><button class="pill-ghost" data-close="menu">Close ✕</button></div>
  <ol>{menu}</ol>
  <p style="margin-top:30px"><a class="pill" href="#" data-open="guide">Open the hand guide ✋</a></p>
</div>
<div class="menu" id="guide" role="dialog" aria-label="Hand guide">
  <div class="menu-top"><a class="brand" href="index.html">terraform.</a><button class="pill-ghost" data-close="guide">Close ✕</button></div>
  <h2 class="display h-md" style="margin-bottom:10px">Your hands are the ruler.</h2>
  <p class="lede" style="margin-bottom:24px">This guide never asks for numbers from a machine. Every size is something you can measure with your body.</p>
  <ul class="guide-list">{guide}</ul>
</div>'''


def bar(left_top, left_bot, step=None, prev=None, nxt=None, ids=False):
    if ids:
        pager = (f'<a id="bar-prev" href="#" aria-label="Previous crop">{CH_L}</a>'
                 f'<span id="bar-count">01 / 10</span><a id="bar-next" href="#" aria-label="Next crop">{CH_R}</a>')
    else:
        p = f'<a href="{prev}" aria-label="Previous step">{CH_L}</a>' if prev else f'<a class="off" aria-hidden="true">{CH_L}</a>'
        n = f'<a href="{nxt}" aria-label="Next step">{CH_R}</a>' if nxt else f'<a class="off" aria-hidden="true">{CH_R}</a>'
        pager = f'{p}<span>{step}</span>{n}'
    return f'''
<footer class="bar">
  <div class="loc">{PIN}<div>{left_top}<b>{left_bot}</b></div><i></i><div>Fixing damaged land<b>Hard · Dirty · Bare</b></div></div>
  <div class="mid">Scroll to keep going ↓</div>
  <div class="pager">{pager}</div>
</footer>'''


QUOTES = {
 "index.html": "Ground that has been hurt can still heal. It only asks for patience.",
 "input.html": "Naming the problem is the first act of repair.",
 "analysis.html": "What you don’t know yet is not a failure. It’s simply the next thing to learn.",
 "protocol.html": "Small steps, taken again and again, move whole hillsides.",
 "next-action.html": "You don’t have to fix everything today. Just do the next right thing.",
 "crops.html": "Somewhere under the dust, the soil is still waiting to grow something.",
 "timeframe.html": "Slow is not stopped. Roots grow in the dark long before leaves ever show.",
 "planting.html": "Every forest you have ever loved began as a seed in hard ground.",
 "care-harvest.html": "Don’t give up now. The harvest belongs to those who keep tending.",
}


def quote(fname):
    q = QUOTES[fname]
    return f'''<aside class="hope" aria-label="A reminder">
  <span class="hope-mark" aria-hidden="true">“</span>
  <p>{q}</p>
  <span class="caps">Keep going</span>
</aside>'''


def doc(fname, title, page, body_cls, active, main, bar_html, crops=False):
    scripts = ('<script src="assets/js/crops-data.js"></script>\n' if crops else '') + '<script src="assets/js/app.js"></script>'
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · Terraform</title>
<meta name="description" content="Terraform: a plain-language guide from bare, damaged ground to a safe first harvest. No lab, no machines, no jargon.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300..800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body class="{body_cls}" data-page="{page}">
{header(active)}
<main>
{main}
{quote(fname)}
</main>
{bar_html}
{scripts}
</body>
</html>
'''
    (OUT / fname).write_text(html, encoding="utf-8")


def head(eyebrow, h1, lede, size="h-lg"):
    return f'''<div class="page-head">
  <div class="eyebrow rv">{eyebrow}</div>
  <h1 class="display {size} rv d1" style="margin-top:22px">{h1}</h1>
  <p class="lede rv d2">{lede}</p>
</div>'''


def cta(href, label, sec=None):
    s = f'<a class="link-u" href="{sec[0]}">{sec[1]} →</a>' if sec else ''
    return f'<div class="center" style="display:flex;gap:26px;justify-content:center;align-items:center;margin-top:38px;flex-wrap:wrap"><a class="pill" href="{href}">{label} <span aria-hidden="true">↗</span></a>{s}</div>'


# ------------------------------------------------------------------ 01 WELCOME
rules = [
    ("No lab numbers", "We never ask for readings from a machine. Only what you can see, smell and feel."),
    ("Your hands are the ruler", "Handfuls, finger-lengths, paces and moons. Open the hand guide any time."),
    ("Safety comes first", "Strange stains, rust or smells mean the ground is unsafe. We build above it, not in it."),
    ("We say what we don’t know", "Every page tells you what has not been checked yet, so nothing is hidden."),
]
rules_html = "".join(f'<div class="rule"><span class="caps">0{i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(rules))
welcome_main = f'''
<section class="hero solo">
  <div class="center">
    <div class="eyebrow rv">From bare ground to your first harvest</div>
    <h1 class="display h-xl rv d1">Heal Ground.<br>Grow Again.</h1>
    <p class="lede rv d2" style="margin:0 auto">Bare, damaged ground can feed you again. We walk you from rubble to harvest using only your eyes, nose and hands.</p>
    <div class="ctas rv d3" style="justify-content:center"><a class="pill" href="input.html">Open Terraform <span aria-hidden="true">↗</span></a><a class="link-u" href="crops.html">See the crops →</a></div>
  </div>
</section>
<section class="rules" aria-label="Ground rules">{rules_html}</section>'''
doc("index.html", "Welcome", "welcome", "bright", "", welcome_main,
    bar("Step 01 · Welcome", "Open to begin", "01 / 06", None, "input.html"))


# ------------------------------------------------------------------ 02 INPUT
def chip(name, v, label=None):
    return f'<label class="chip"><input type="checkbox" name="{name}" value="{v}"><span>{label or v}</span></label>'


def chips(name, items):
    return '<div class="chips">' + "".join(chip(name, v, l) for v, l in items) + '</div>'


def fld(i, label, ctl, hint="", full=False, req=False, how=None):
    h = f'<span class="hint">{hint}</span>' if hint else ''
    hw = f' <a class="how" href="analysis.html#how-{how}">How?</a>' if how else ''
    return f'<div class="field{" full" if full else ""}" id="f-{i}"><label for="{i}">{label}{" *" if req else ""}{hw}</label>{ctl}{h}<span class="err">Please fill this in.</span></div>'


def inp(i, ph="", t="text", extra=""):
    return f'<input class="in" id="{i}" name="{i}" type="{t}" placeholder="{ph}" {extra}>'


def sel(i, opts, first="Select…"):
    return f'<select class="in" id="{i}" name="{i}"><option value="">{first}</option>' + "".join(f'<option value="{v}">{l}</option>' for v, l in opts) + '</select>'


def chk(i, label, opts, how):
    return fld(i, label, sel(i, opts, "Not checked yet"), full=True, how=how)


input_main = head("Step 02 · Describe your land", "Tell us what<br>you see.", "Walk the ground. Look, smell, touch. Fill in what you know and leave the rest. The next page lists whatever you haven’t checked yet.", "h-lg") + f'''
<form id="site-form" novalidate>
<div class="grid g2" style="align-items:start">
  <div class="grid" style="gap:18px">
    <section class="card form-sec"><span class="sec-no">01 · The patch</span><h3>About this patch of ground</h3><p class="sub">Where it is and what it used to be.</p>
      <div class="f-grid">
        {fld("siteName","Give it a name",inp("siteName","e.g. Old workshop yard"),full=True,req=True)}
        {fld("pastUse","What was it used for before?",sel("pastUse",[("factory","Factory or workshop"),("road","Rail yard or road"),("rubble","Knocked-down building"),("farm","Old farm field"),("dump","Rubbish tip"),("unknown","I don’t know")]),full=True,req=True)}
        {fld("paceLong","How long? (paces)",inp("paceLong","e.g. 20","number",'min="0"'))}
        {fld("paceWide","How wide? (paces)",inp("paceWide","e.g. 10","number",'min="0"'))}
        {fld("sun","How much sun does it get?",sel("sun",[("most","Most of the day"),("half","About half the day"),("shade","Mostly shade")]))}
        {fld("water","Where can you get water?",sel("water",[("tap","Tap or well close by"),("rain","Rain barrel"),("stream","Stream or pond"),("carry","I carry it in buckets"),("none","None yet")]))}
      </div></section>
    <section class="card form-sec"><span class="sec-no">02 · What you can see and smell</span><h3>Look around</h3><p class="sub">Tick everything you notice.</p>
      <div class="f-grid">
        <div class="field full" id="f-stains"><span class="lab">Stains on the ground</span>{chips("stains",[("black","Black"),("rainbow","Rainbow or oily shine"),("rust","Rust-orange"),("white","White crust"),("none","None seen")])}</div>
        <div class="field full" id="f-smells"><span class="lab">Smells</span>{chips("smells",[("sour","Sour"),("egg","Rotten egg"),("metal","Metallic"),("fuel","Fuel or chemical"),("earthy","Earthy, like after rain"),("none","No smell")])}</div>
        <div class="field full" id="f-junk"><span class="lab">Junk on or in the ground</span>{chips("junk",[("rubble","Concrete or brick pieces"),("metal","Rusty metal"),("glass","Broken glass"),("cinder","Cinders or ash-like crumbs"),("pipes","Wires or pipes"),("plastic","Plastic or rubbish"),("none","None")])}</div>
        <div class="field full" id="f-plants"><span class="lab">What grows there</span>{chips("plants",[("thistle","Thistles or clumpy weeds"),("lush","Dark green, lush weeds (nettle, dock)"),("pale","Pale, yellow, stunted weeds"),("moss","Moss"),("bare","Bare patches"),("nothing","Nothing grows")])}</div>
      </div></section>
  </div>
  <div class="grid" style="gap:18px">
    <section class="card form-sec"><span class="sec-no">03 · Quick hand checks</span><h3>Try these, if you can</h3><p class="sub">Not done one yet? Leave it. We’ll list it for you. Tap “How?” for the steps.</p>
      <div class="f-grid">
        {chk("dig","Dig a hand’s depth down. What’s under the top?",[("same","Same soil all the way"),("rubble","Rubble or junk underneath"),("stained","Smelly or stained soil underneath"),("hard","A hard layer I couldn’t dig through")],"dig")}
        {chk("rainSmell","Smell the ground after rain",[("earthy","Earthy"),("sour","Sour or rotten"),("fuel","Fuel or chemical"),("none","No smell")],"rainSmell")}
        {chk("drain","Where does rain water go?",[("fast","Soaks in quickly"),("slow","Soaks in slowly"),("stands","Sits for days")],"drain")}
        {chk("squeeze","Squeeze a damp handful",[("crumbly","Crumbles like breadcrumbs"),("ribbon","Makes a sticky strip longer than two thumb-joints"),("runs","Runs through my fingers")],"squeeze")}
        {chk("squish","Squeeze a wet handful",[("sponge","Springs back like a sponge"),("hard","Rock hard"),("slimy","Slimy")],"squish")}
        {chk("stick","Push a thumb-thick green stick straight down",[("deep","Goes in more than a hand-width"),("shallow","Goes in less than a hand-width")],"stick")}
        {chk("jar","Shake a handful in a jar of rainwater and let it settle",[("clear","Clear, no shine, no smell"),("sheen","Rainbow shine or a fuel smell")],"jar")}
        {chk("sprout","Sprout test: site soil cup next to clean soil cup",[("ok","Both sprouted fine"),("poor","Site cup is poorer, or leaf tips turned black")],"sprout")}
      </div></section>
    <section class="card form-sec"><span class="sec-no">04 · In your own words</span><h3>Anything else?</h3><p class="sub">Say what you see in your own words. We repeat it back exactly.</p>
      <div class="f-grid">
        {fld("problems","What have you noticed?",'<textarea class="in" id="problems" name="problems" placeholder="e.g. Hard, bare ground. Water sits for days. Orange staining by the old wall."></textarea>',full=True,req=True)}
        <div class="field full"><label for="photo">Photos (optional)</label><input class="in" id="photo" name="photo" type="file" accept="image/*" multiple><span class="hint">Preview only. Photos will connect later.</span></div>
      </div></section>
  </div>
</div>
<div style="display:flex;gap:14px;align-items:center;justify-content:center;flex-wrap:wrap;margin-top:34px">
  <button type="submit" class="pill">See what’s missing <span aria-hidden="true">↗</span></button>
  <button type="button" class="pill-ghost" id="btn-save">Save for later</button>
  <button type="button" class="pill-ghost" id="btn-sample">Fill in an example</button>
  <button type="button" class="link-u" id="btn-clear">Start over</button>
</div>
<p id="save-msg" class="center caps" style="margin-top:16px;opacity:0;transition:opacity .3s" role="status"></p>
</form>'''
doc("input.html", "Describe your land", "input", "dim", "input.html", input_main,
    bar("Step 02 · Your land", "Say what you see", "02 / 06", "index.html", "analysis.html"))


# ------------------------------------------------------------------ 03 ANALYSIS
analysis_main = head("Step 03 · What’s missing", "What we know.<br>What we don’t.", "We repeat back what you told us, say what kind of ground it looks like, and list every check you haven’t done yet.", "h-lg") + '''
<section id="empty" class="card center" hidden style="max-width:640px;margin:0 auto"><h3>Nothing entered yet</h3><p class="sub" style="margin:8px auto 22px">Describe your land first, or fill in the example to see how this page works.</p><a class="pill" style="background:var(--blue);color:var(--cream)" href="input.html">Describe your land ↗</a></section>
<div id="analysis-body">
  <div class="grid" style="grid-template-columns:1fr 1.3fr;margin-bottom:18px;align-items:stretch">
    <div class="card" style="display:flex;gap:24px;align-items:center;flex-wrap:wrap">
      <div class="ring" id="ring"><b>0%</b></div>
      <div style="flex:1;min-width:160px"><span class="sec-no" style="margin:0 0 8px">Checks done</span><h3 id="site-title" style="font-size:28px">Your patch</h3><p class="sub" id="readout" style="margin:8px 0 0"></p></div>
    </div>
    <div class="card verdict" id="verdict"><span class="sec-no" style="color:inherit">Safety verdict</span><h3 id="v-title" style="font-size:clamp(30px,3.4vw,46px);line-height:.95">…</h3><p id="v-text" style="font-size:15px;margin-top:12px;max-width:56ch"></p></div>
  </div>
  <div class="grid" style="grid-template-columns:1fr 1fr;align-items:start">
    <div class="grid" style="gap:18px">
      <section class="card"><span class="sec-no">What you told us</span><h3>Your words, repeated back</h3><p class="sub">Nothing added. Nothing guessed.</p><dl class="kv" id="restate"></dl></section>
      <section class="card lime"><span class="sec-no">What it looks like</span><h3 id="land-name">…</h3><p id="land-blurb" style="font-size:14.5px;margin-top:8px"></p><div class="kv-row"><b>Main problem</b><span id="land-danger"></span></div><div class="kv-row"><b>What to do</b><span id="land-fix"></span></div></section>
      <section class="card"><span class="sec-no">What your checks say</span><h3>Signs from the checks you did</h3><ul class="gaps" id="flags"></ul></section>
    </div>
    <div class="grid" style="gap:18px">
      <section class="card"><span class="sec-no">Not checked yet</span><h3>Checks still to do</h3><p class="sub">Tap one to see how. Each takes a few minutes and needs no tools.</p><div id="unchecked"></div></section>
      <section class="card orange"><span class="sec-no" style="color:var(--blue-ink)">Be honest about limits</span><h3>What these checks can’t tell you</h3><p style="font-size:15px;margin-top:8px">They can’t see hidden poisons such as lead or arsenic, or old farm sprays that have no smell. <b>Never grow root crops straight in unchecked ground.</b> Always grow above it, in a raised bed or container.</p></section>
    </div>
  </div>
  ''' + cta("protocol.html", "Go to the step-by-step fix", ("input.html", "Change what I told you")) + '''
</div>'''
doc("analysis.html", "What’s missing", "analysis", "dim", "analysis.html", analysis_main,
    bar("Step 03 · What’s missing", "Spot the gaps", "03 / 06", "input.html", "protocol.html"))


# ------------------------------------------------------------------ 04 PROTOCOL
bed_svg = '''<svg viewBox="0 0 560 250" role="img" aria-label="Cross-section of a knee-high raised bed: barrier on the ground, logs and branches in the bottom half, growing mix on top" width="100%">
<rect x="0" y="0" width="560" height="250" fill="#1a2bd0"/>
<rect x="0" y="212" width="560" height="38" fill="#6b3f26"/>
<rect x="60" y="205" width="440" height="7" fill="#fdf0dc"/>
<rect x="60" y="205" width="440" height="7" fill="none" stroke="#0c1670" stroke-dasharray="6 5"/>
<rect x="60" y="30" width="26" height="175" fill="#9a8a7a"/><rect x="474" y="30" width="26" height="175" fill="#9a8a7a"/>
<rect x="86" y="30" width="388" height="88" fill="#3d2a1a"/>
<rect x="86" y="118" width="388" height="87" fill="#7a5a3a"/>
<g stroke="#4a3220" stroke-width="10" stroke-linecap="round"><path d="M110 150h90M240 170h120M130 185h60M300 140h110M370 185h90M210 135h40"/></g>
<g fill="#5aa83a"><circle cx="150" cy="22" r="8"/><circle cx="260" cy="20" r="8"/><circle cx="370" cy="22" r="8"/></g>
<g font-family="Inter,sans-serif" font-size="13" font-weight="600" fill="#fdf0dc">
<text x="96" y="72">Growing mix (top half)</text><text x="96" y="140" fill="#fdf0dc">Logs, branches, dry leaves (bottom half)</text>
<text x="96" y="234">Barrier: 3 layers of wet cardboard or canvas</text>
<text x="510" y="116" text-anchor="end" fill="#fdf0dc"> </text></g>
<path d="M530 30v175" stroke="#fdf0dc" stroke-width="2"/><path d="M524 36l6-6 6 6M524 199l6 6 6-6" fill="none" stroke="#fdf0dc" stroke-width="2"/>
<text x="548" y="124" fill="#fdf0dc" font-size="12" font-family="Inter,sans-serif" font-weight="600" transform="rotate(90 548 124)" text-anchor="middle">knee-high</text>
</svg>'''
protocol_main = head("Step 04 · Step-by-step fix", "Don’t fix the ground.<br>Grow above it.", "Poisoned or packed ground is slow to heal. So we cover it, build up from it, and fill the bed with clean material. Tick each step off as you go.", "h-lg") + f'''
<div class="center" style="margin-bottom:26px"><div class="seg" id="seg" role="tablist"><button data-t="bed">Raised bed</button><button data-t="box">Deep containers</button></div></div>
<div class="grid g2" style="margin-bottom:18px;align-items:stretch">
  <section class="card glass"><span class="sec-no">Picture it</span><h3>A knee-high bed, from the bottom up</h3><div style="border-radius:16px;overflow:hidden;margin-top:12px">{bed_svg}</div></section>
  <section class="card lime"><span class="sec-no">The growing mix</span><h3>For every pace of bed length</h3>
    <div class="recipe"><div><b>2</b><span>buckets of rotted forest leaves</span></div><div><b>1</b><span>bucket of crushed charcoal or cold campfire ash</span></div><div><b>2</b><span>buckets of compost</span></div></div>
    <p class="note" style="border-color:rgba(8,15,77,.3)">Use clean material from outside the site. Never mix in soil from the damaged ground.</p></section>
</div>
<section class="card" id="land-tip" hidden style="margin-bottom:18px"><span class="sec-no">For your kind of ground</span><h3 id="tip-name"></h3><p class="sub" id="tip-text" style="margin:6px 0 0;font-size:14.5px;opacity:1"></p></section>
<div style="max-width:900px;margin:0 auto">
  <div style="display:flex;justify-content:space-between;margin-bottom:10px" class="caps"><span>Your progress</span><span id="prog-txt"></span></div>
  <div class="progress" style="margin-bottom:26px"><i id="prog-bar"></i></div>
  <ol class="steps" id="steps"></ol>
  <div class="callout">{WARN}<div><b>Stay safe.</b> Wear gloves and sturdy shoes, wash before you eat, and keep children and animals off the ground. Never dig, burn or sweep suspect soil, because the dust can carry poison.</div></div>
  ''' + cta("next-action.html", "See the next action", ("analysis.html", "Back to what’s missing")) + '''
</div>'''
doc("protocol.html", "Step-by-step fix", "protocol", "dim", "protocol.html", protocol_main,
    bar("Step 04 · Step by step", "Build above it", "04 / 06", "analysis.html", "next-action.html"))


# ------------------------------------------------------------------ 05 NEXT ACTION
def ready(k, n, title, how, pass_):
    return f'''<label class="ready" data-k="{k}"><input type="checkbox" id="r-{k}"><div><span class="caps">Check {n}</span><h4>{title}</h4><p>{how}</p><p class="pass"><b>Pass:</b> {pass_}</p></div></label>'''


next_main = head("Step 05 · Next action", "What to do<br>next.", "One thing to do now, three checks to make sure the bed is ready, and everything else lined up behind it.", "h-lg") + '''
<div class="next-hero">
  <section class="card orange" style="display:flex;flex-direction:column;justify-content:space-between;min-height:260px">
    <div><span class="sec-no" style="color:var(--blue-ink)">Do this next</span><h3 id="ha-title" style="font-size:clamp(34px,4vw,58px);line-height:.95">…</h3><p id="ha-text" style="font-size:15px;margin-top:14px;max-width:52ch"></p></div>
    <div style="margin-top:24px"><a class="pill" id="ha-cta" href="#" style="background:var(--blue-ink);color:var(--cream)"><span id="ha-cta-t">Go</span> <span aria-hidden="true">↗</span></a></div>
  </section>
  <div class="grid" style="gap:14px;grid-template-columns:1fr 1fr">
    <div class="stat"><div class="n" id="st-checks">0</div><div class="l">Hand checks still open</div></div>
    <div class="stat"><div class="n"><span id="st-bed">0</span>/6</div><div class="l">Bed steps done</div></div>
    <div class="stat" style="grid-column:1/-1"><div class="n"><span id="st-ready">0</span>/3</div><div class="l">Readiness checks passed</div></div>
  </div>
</div>
<section class="card" style="margin-bottom:18px"><span class="sec-no">Is the bed ready?</span><h3>Three checks before you plant</h3><p class="sub">Do all three. Tick each one when it passes.</p>
  <div class="ready-grid">''' + ready("drain", 1, "The puddle check", "Dig a hole one hand’s depth deep. Fill it with a bucket of water.", "The water drains away in the time it takes to walk 500 paces.") + ready("heat", 2, "The warmth check", "Let the bed rest 5 to 7 suns. Then press the back of your hand into the mix.", "It does not feel hot. Hot means unfinished compost, which would burn young roots.") + ready("sprout", 3, "The sprout check", "Sprout a few seeds in a cup of the bed mix.", "They sprout with no curled or blackened leaf tips.") + '''</div>
  <div id="ready-msg" class="callout" style="margin-top:18px"></div>
</section>
<div class="kanban">
  <div class="col"><h3><span>Today</span><span>Right now</span></h3><div id="col-now"></div></div>
  <div class="col"><h3><span>This week</span><span>Next few suns</span></h3><div id="col-soon"></div></div>
  <div class="col"><h3><span>This moon</span><span>Next 4 weeks</span></h3><div id="col-later"></div></div>
</div>
''' + cta("crops.html", "Choose a crop", ("protocol.html", "Back to the fix"))
doc("next-action.html", "Next action", "next", "dim", "next-action.html", next_main,
    bar("Step 05 · Next action", "Is it ready?", "05 / 06", "protocol.html", "crops.html"))


# ------------------------------------------------------------------ 06 CROPS
crops_main = head("Step 06 · Choose a crop", "Ten safe crops<br>to start with.", "All ten grow above the ground in a clean bed or container. Each one opens its own pages: how long it takes, how to plant, care, and harvest.", "h-lg") + f'''
<div class="callout" style="margin:0 auto 26px;max-width:900px">{WARN}<div><b>Safety rule.</b> Never grow carrots, potatoes, radishes or leafy greens straight in suspect ground. Skip sunflowers there too: they pull poison up into the plant. Grow only in your clean raised bed or containers.</div></div>
<div class="filters" role="group" aria-label="Filter crops">
  <button class="on" data-f="all">All 10</button><button data-f="soil">Feed the soil</button><button data-f="hungry">Hungry plants</button><button data-f="gentle">Gentle plants</button><button data-f="rest">Rest-season</button>
</div>
<div class="crops" id="crops"></div>
<p class="foot">Hungry plants take a lot from the soil · Gentle plants take less · Soil builders give back · Rest-season plants heal the bed</p>'''
doc("crops.html", "Choose a crop", "crops", "dim", "crops.html", crops_main,
    bar("Step 06 · Crops", "Pick one", "06 / 06", "next-action.html", None), crops=True)


# ------------------------------------------------------------------ 07-09 CROP DETAIL
def crop_head(label):
    return f'''
<div class="crumb"><a href="crops.html">Crops</a><span>/</span><span id="c-sci"></span></div>
<div class="page-head" style="margin-top:0">
  <div class="eyebrow rv">{label}</div>
  <h1 class="display h-xl rv d1" id="c-name" style="margin-top:22px">Crop</h1>
  <p class="lede rv d2" id="c-tag"></p>
  <p class="rv d3" style="margin-top:18px"><span class="tag" id="c-role" style="color:var(--lime)"></span></p>
</div>
<div id="under-warn" class="callout" hidden style="margin:0 auto 22px;max-width:900px">{WARN}<div><b>Grows underground.</b> Only grow this in a clean, knee-high bed or mound filled with outside soil. Never in suspect ground.</div></div>
<div class="switch" id="switch" aria-label="Switch crop"></div>
<nav class="subnav" id="subnav" aria-label="Crop sections"></nav>'''


def detail_bar():
    return bar("Crop", '<span id="bar-name">—</span>', ids=True)


time_main = crop_head("Step 07 · How long it takes") + '''
<div class="facts">
  <div class="stat"><div class="n" id="f-total" style="font-size:clamp(28px,3vw,40px)">—</div><div class="l">From today to first harvest</div></div>
  <div class="stat"><div class="n" id="f-moons" style="font-size:clamp(28px,3vw,40px)">—</div><div class="l">About this many moons</div></div>
  <div class="stat"><div class="n" id="f-sow" style="font-size:20px;line-height:1.15">—</div><div class="l">When to sow</div></div>
  <div class="stat"><div class="n" id="f-first" style="font-size:20px;line-height:1.15">—</div><div class="l">First picking</div></div>
</div>
<section class="card"><span class="sec-no">The whole journey</span><h3>From bare ground to harvest</h3><p class="sub">Length of each stage. Short bars show stages that take only a week or two.</p>
  <div class="g-scale" id="g-axis"></div><div class="gantt" id="gantt"></div>
  <p class="note"><b>The sum:</b> clearing the land (1–2 weeks) + building the bed and letting it settle (1–2 weeks) + the crop’s own time from seed to harvest.</p></section>
<section class="card glass" style="margin-top:18px"><span class="sec-no">Milestones</span><h3>What to expect, week by week</h3>
  <ol class="mile"><li><b>Weeks 0–2</b><span>Lock down the land, lay the barrier, build the bed. Run the sprout check.</span></li><li><b>Weeks 3–4</b><span>Sow the seeds. First tiny leaves appear.</span></li><li><b>Weeks 5–8</b><span>Fast growth. Leaf crops can be picked.</span></li><li><b>Harvest window</b><span>Main harvest, then save seed for next time.</span></li></ol></section>
''' + cta("planting.html", "How to plant it")
doc("timeframe.html", "How long it takes", "timeframe", "dim", "crops.html", time_main, detail_bar(), crops=True)

plant_main = crop_head("Step 08 · How to plant") + '''
<div class="grid g2" style="align-items:start">
  <section class="card"><span class="sec-no">The basics</span><h3>How it goes in</h3><p class="sub">All sizes are measured with your hand.</p>
    <div class="spec">
      <div style="grid-column:1/-1"><b>Where</b><span id="sp-where">—</span></div>
      <div><b>Seeds</b><span id="sp-seeds">—</span></div>
      <div><b>How deep</b><span id="sp-depth">—</span></div>
      <div><b>How far apart</b><span id="sp-space">—</span></div>
      <div><b>Extras</b><span id="sp-extra">—</span></div>
    </div></section>
  <section class="card glass"><span class="sec-no">Picture it</span><h3>Seeds under the surface</h3><p class="sub" style="color:var(--cream)">Each tick on the line is one finger-length.</p><div id="profile" style="border-radius:16px;overflow:hidden"></div></section>
</div>
<section class="card" style="margin-top:18px"><span class="sec-no">Step by step</span><h3>Planting, in order</h3><p class="sub">Do these in order.</p><ol class="olist" id="p-steps"></ol>
  <p class="note">Don’t plant until the bed has passed the three readiness checks. <a href="next-action.html" style="text-decoration:underline">See the checks</a>.</p></section>
''' + cta("care-harvest.html#care", "Care & harvest", ("timeframe.html", "Back to how long it takes"))
doc("planting.html", "How to plant", "planting", "dim", "crops.html", plant_main, detail_bar(), crops=True)

care_main = crop_head("Step 09 · Care & harvest") + '''
<div class="sec-title" id="care"><h2 class="display">Looking after it</h2><span>Week by week</span></div>
<section class="card"><table class="t"><thead><tr><th>When</th><th>What</th><th>What to do</th></tr></thead><tbody id="care-rows"></tbody></table></section>
<section class="card glass" style="margin-top:18px"><span class="sec-no">Something looks wrong?</span><h3>Find the sign, do the fix</h3><p class="sub" style="color:var(--cream)">Match what you see to the row. All fixes use things you can find or make.</p>
  <div class="tbl-wrap"><table class="t on-dark"><thead><tr><th>What you see</th><th>Likely cause</th><th>What to do</th></tr></thead><tbody id="fix-rows"></tbody></table></div></section>
<div class="sec-title" id="harvest"><h2 class="display">Harvest</h2><span>When &amp; how</span></div>
<div class="grid g2" style="align-items:start">
  <section class="card"><span class="sec-no">Ready?</span><h3>How to tell it’s ready</h3><p class="sub" id="h-signs" style="font-size:15px;opacity:1"></p>
    <div class="spec" style="margin-top:8px"><div style="grid-column:1/-1"><b>How to pick</b><span id="h-how" style="font-size:18px">—</span></div><div><b>Keep some for seed</b><span id="h-keep" style="font-size:16px">—</span></div><div><b>Why it matters</b><span id="h-value" style="font-size:16px">—</span></div></div></section>
  <section class="card lime"><span class="sec-no">What next?</span><h3>What to plant after this</h3><p class="sub" style="opacity:1;margin-bottom:14px">Rotate crops so the bed stays rich. Follow the cycle.</p><ol class="rot" id="rot"></ol></section>
</div>
<div class="callout">''' + WARN + '''<div><b>Check before you eat.</b> If the ground was ever suspect, only eat what grew in your clean bed. Wash everything well. Keep plant waste from the damaged ground out of your food and compost.</div></div>
''' + cta("crops.html", "Choose another crop", ("planting.html", "Back to planting"))
doc("care-harvest.html", "Care & harvest", "care", "dim", "crops.html", care_main, detail_bar(), crops=True)

print("built", len(list(OUT.glob("*.html"))), "pages")
