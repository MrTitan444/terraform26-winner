"""
TERRAFORM Case Study NLP & Multimodal Extractor
Analyzes 300-500 word case study summaries and land photo clues to autofill
all 14 intake fields without human lab numbers or instruments.
"""

import re
from typing import Dict, Any, List, Optional

class CaseStudyExtractor:
    def __init__(self):
        # Keyword patterns for past use
        self.past_use_rules = [
            ("factory", ["factory", "workshop", "industrial", "machinery", "smelter", "refinery", "foundry", "plant", "assembly", "mechanic", "garage", "mill"]),
            ("road", ["rail", "railway", "train", "tracks", "road", "highway", "asphalt", "tarmac", "station", "depot", "transport", "siding"]),
            ("rubble", ["rubble", "demolition", "demolished", "collapsed wall", "knocked down", "masonry", "crushed concrete", "ruins", "brick pile"]),
            ("farm", ["farm", "field", "orchard", "pasture", "monoculture", "overfarmed", "plowed", "crop", "pesticide"]),
            ("dump", ["dump", "rubbish tip", "landfill", "trash", "scrap yard", "waste pile", "junkyard", "refuse"]),
        ]

        # Stains
        self.stain_rules = [
            ("black", ["black", "dark and stained", "dark stain", "motor oil", "petroleum", "tar", "soot", "pitch"]),
            ("rainbow", ["rainbow", "oily shine", "iridescent", "sheen", "oil slick", "slick"]),
            ("rust", ["rust", "orange", "rusted metal", "corrosion", "reddish-brown", "iron oxide"]),
            ("white", ["white crust", "white film", "chalky", "salt crust", "lime powder", "efflorescence"]),
            ("none", ["clean soil", "no stains seen", "unstained", "no discoloration"]),
        ]

        # Smells
        self.smell_rules = [
            ("sour", ["sour", "acid", "vinegar", "rotting", "acrid", "sour smell"]),
            ("egg", ["rotten egg", "sulfur", "sewer", "hydrogen sulfide", "stench of sulfur"]),
            ("metal", ["metal", "metallic", "iron smell", "sharp copper", "scrap odor"]),
            ("fuel", ["fuel", "chemical", "petrol", "diesel", "gasoline", "solvent", "kerosene", "oil smell", "oily odor"]),
            ("earthy", ["earthy", "forest", "rain smell", "petrichor", "rich earth"]),
            ("none", ["no smell", "odorless", "fresh air", "neutral scent"]),
        ]

        # Junk / Debris
        self.junk_rules = [
            ("rubble", ["concrete", "brick", "mortar", "masonry", "rubble", "cement", "broken stones"]),
            ("metal", ["rusted metal", "scrap metal", "rebar", "iron", "nails", "wire mesh", "rusty metal"]),
            ("glass", ["broken glass", "glass shards", "shattered glass", "bottles"]),
            ("cinder", ["cinder", "ash", "charcoal crumbs", "slag", "burnt debris", "clinker"]),
            ("pipes", ["pipes", "wires", "conduit", "cables", "copper lines"]),
            ("plastic", ["plastic", "synthetic", "trash", "rubbish", "nylon", "poly", "tarpaulin"]),
            ("none", ["no junk", "clear ground", "clean surface", "no debris"]),
        ]

        # Vegetation
        self.plant_rules = [
            ("thistle", ["thistle", "thistles", "clumpy weeds", "weeds grow in clumps", "thorny", "burdock"]),
            ("lush", ["lush", "dark green weeds", "nettle", "dock weed", "vigorous weeds", "dense greenery"]),
            ("pale", ["pale", "yellow", "stunted weeds", "stunted", "chlorotic", "yellowish"]),
            ("moss", ["moss", "lichen", "green crust", "damp moss"]),
            ("bare", ["bare patches", "nothing grows evenly", "patchy", "bald spots", "exposed soil", "bare", "bald"]),
            ("nothing", ["nothing grows at all", "nothing can grow", "barren ground", "dead zone", "zero vegetation"]),
        ]

        # In-field checks
        self.check_rules = {
            "dig": [
                ("rubble", ["rubble or junk underneath", "rubble underneath", "concrete chunks underneath", "masonry buried"]),
                ("stained", ["smelly or stained soil underneath", "stained soil underneath", "dark smelly layer", "black subsoil"]),
                ("hard", ["hard layer i couldn’t dig through", "hard layer", "hardpan", "impenetrable", "couldn't dig through", "rock hard base"]),
                ("same", ["same soil all the way", "uniform soil", "consistent depth"])
            ],
            "rainSmell": [
                ("sour", ["sour smell after rain", "sour after rain", "smells sour", "sour odor"]),
                ("fuel", ["fuel or chemical smell after rain", "fuel smell", "diesel vapors", "chemical smell", "diesel fuel"]),
                ("earthy", ["earthy after rain", "earthy smell after rain", "fresh earth scent"]),
                ("none", ["no smell after rain"])
            ],
            "drain": [
                ("stands", ["water sits for days", "sits for days", "stagnant puddles", "pools for days", "standing puddles"]),
                ("slow", ["soaks in slowly", "slow to drain", "sluggish drainage"]),
                ("fast", ["soaks in quickly", "drains rapidly", "fast soaking"])
            ],
            "squeeze": [
                ("ribbon", ["sticky strip", "sticky ribbon", "dense ribbon", "forms a sticky ribbon", "heavy clay", "clay ribbon", "thumb-joints"]),
                ("crumbly", ["crumbles like breadcrumbs", "crumbly", "rich loam", "soft breadcrumbs"]),
                ("runs", ["runs through my fingers", "loose sand", "slips through fingers"])
            ],
            "squish": [
                ("sponge", ["springs back like a sponge", "springy", "spongy"]),
                ("hard", ["rock hard", "cement-like", "dense clod"]),
                ("slimy", ["slimy", "greasy feel", "slimy soil"])
            ],
            "stick": [
                ("shallow", ["less than a hand-width", "penetrates less than a hand-width", "shallow penetration", "stopped by hard layer", "hard to push"]),
                ("deep", ["more than a hand-width", "goes in easily", "deep penetration", "plunges deep"])
            ],
            "jar": [
                ("sheen", ["rainbow shine", "rainbow sheen", "rainbow slick", "fuel smell in jar", "oily film", "iridescent film in jar", "oil ring"]),
                ("clear", ["clear, no shine", "settled clear", "no sheen", "clean water layer"])
            ],
            "sprout": [
                ("poor", ["site cup is poorer", "leaf tips turned black", "blackened root tips", "blackened tips", "stunted in site soil", "failed sprout", "curled black tips", "seedling failure"]),
                ("ok", ["both sprouted fine", "sprouted well", "normal growth in site cup"])
            ]
        }

    def extract(self, text: str, image_hints: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Parses text and optional image hints to generate an autofill dictionary
        for the input.html form.
        """
        lower = text.lower()
        image_hints = [h.lower() for h in (image_hints or [])]
        detected_clues = []

        # 1. Past Use
        past_use = "unknown"
        for code, kws in self.past_use_rules:
            for kw in kws:
                if kw in lower:
                    past_use = code
                    detected_clues.append(f"Past use identified as '{code}' (keyword: '{kw}')")
                    break
            if past_use != "unknown":
                break

        # 2. Dimensions (paces / meters)
        pace_long = ""
        pace_wide = ""
        # Look for "20 paces long by 10 paces wide", "20 by 10 paces", "20x10 meters", etc.
        dim_match = re.search(r"(\d+)\s*(?:paces?|m|meters?|steps?)?\s*(?:long)?\s*(?:by|x|\*|and)\s*(\d+)\s*(?:paces?|m|meters?|steps?|wide)", lower)
        if dim_match:
            pace_long = dim_match.group(1)
            pace_wide = dim_match.group(2)
            detected_clues.append(f"Dimensions extracted: {pace_long} paces long × {pace_wide} paces wide")
        else:
            single_match = re.search(r"(\d+)\s*paces", lower)
            if single_match:
                pace_long = single_match.group(1)
                detected_clues.append(f"Length extracted: {pace_long} paces")

        # 3. Sun Exposure
        sun = ""
        if any(w in lower for w in ["full sun", "all day", "open sky", "baked in sun", "baked in open sunlight", "unshaded", "most of the day"]):
            sun = "most"
            detected_clues.append("Sun exposure: Most of the day (full sun)")
        elif any(w in lower for w in ["dense shade", "high walls", "deep shadow", "canopy", "mostly shade"]):
            sun = "shade"
            detected_clues.append("Sun exposure: Mostly shade")
        elif any(w in lower for w in ["half day", "partial shade", "morning sun", "afternoon shade", "half the day"]):
            sun = "half"
            detected_clues.append("Sun exposure: About half the day")

        # 4. Water Source
        water = ""
        if any(w in lower for w in ["carry", "bucket", "carrying water", "carry it in buckets"]):
            water = "carry"
            detected_clues.append("Water source: Carried in buckets")
        elif any(w in lower for w in ["tap", "well", "pump", "spigot", "hose"]):
            water = "tap"
            detected_clues.append("Water source: Tap or well")
        elif any(w in lower for w in ["rain barrel", "cistern", "butt", "catches rain", "catchment"]):
            water = "rain"
            detected_clues.append("Water source: Rain barrel")
        elif any(w in lower for w in ["stream", "creek", "brook", "river", "pond"]):
            water = "stream"
            detected_clues.append("Water source: Stream or pond")
        elif any(w in lower for w in ["no water", "dry ground", "none yet", "waterless"]):
            water = "none"
            detected_clues.append("Water source: None yet")

        # 5. Stains
        stains = []
        for code, kws in self.stain_rules:
            if code == "none":
                continue
            if any(kw in lower for kw in kws) or (code in image_hints):
                stains.append(code)
                detected_clues.append(f"Stain detected: {code}")
        if not stains:
            if any(kw in lower for kw in ["no stain", "clean soil", "unstained"]):
                stains.append("none")

        # 6. Smells
        smells = []
        for code, kws in self.smell_rules:
            if code == "none":
                continue
            if any(kw in lower for kw in kws):
                smells.append(code)
                detected_clues.append(f"Smell detected: {code}")
        if not smells:
            if any(kw in lower for kw in ["no smell", "odorless", "fresh air"]):
                smells.append("none")

        # 7. Junk / Debris
        junk = []
        for code, kws in self.junk_rules:
            if code == "none":
                continue
            if any(kw in lower for kw in kws) or (code in image_hints):
                junk.append(code)
                detected_clues.append(f"Debris detected: {code}")
        if not junk:
            if any(kw in lower for kw in ["no junk", "clean surface", "no debris"]):
                junk.append("none")

        # 8. Plants / Vegetation
        plants = []
        for code, kws in self.plant_rules:
            if any(kw in lower for kw in kws):
                plants.append(code)
                detected_clues.append(f"Vegetation indicator: {code}")

        # 9. Quick Hand Checks
        checks = {}
        for check_name, opt_list in self.check_rules.items():
            for code, kws in opt_list:
                if any(kw in lower for kw in kws):
                    checks[check_name] = code
                    detected_clues.append(f"Hand check '{check_name}' deduced as '{code}'")
                    break

        # Generate a descriptive Site Name
        site_name = ""
        name_match = re.search(r"(?:site|patch|location|area|ground)\s*(?:named|called)\s*[\"']?([^\"'\n\.,;]+)[\"']?", lower)
        if name_match and len(name_match.group(1).split()) <= 4 and not any(w in name_match.group(1).lower() for w in ["of ", "that ", "was ", "is "]):
            site_name = name_match.group(1).title()
        else:
            # Fallback based on past use and stains
            descriptor = "Disturbed"
            if "rust" in stains:
                descriptor = "Rusted"
            elif "black" in stains:
                descriptor = "Dark-Stained"
            elif "rubble" in junk:
                descriptor = "Rubble"

            target = "Ground"
            if past_use == "factory":
                target = "Workshop Yard"
            elif past_use == "road":
                target = "Rail Siding"
            elif past_use == "rubble":
                target = "Collapsed Wall Site"
            elif past_use == "farm":
                target = "Worn Farm Plot"
            elif past_use == "dump":
                target = "Refuse Tip"

            site_name = f"{descriptor} {target}"

        words = len(text.split())

        return {
            "status": "success",
            "word_count": words,
            "extracted_fields": {
                "siteName": site_name,
                "pastUse": past_use,
                "paceLong": pace_long,
                "paceWide": pace_wide,
                "sun": sun,
                "water": water,
                "stains": stains,
                "smells": smells,
                "junk": junk,
                "plants": plants,
                "dig": checks.get("dig", ""),
                "rainSmell": checks.get("rainSmell", ""),
                "drain": checks.get("drain", ""),
                "squeeze": checks.get("squeeze", ""),
                "squish": checks.get("squish", ""),
                "stick": checks.get("stick", ""),
                "jar": checks.get("jar", ""),
                "sprout": checks.get("sprout", ""),
                "problems": text.strip()
            },
            "detected_clues": detected_clues,
            "summary_statement": f"Analyzed {words} words: Extracted past use '{past_use}', {len(stains)} stains, {len(smells)} smells, {len(junk)} debris types, and {len(checks)} in-field checks."
        }
