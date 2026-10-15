"""
TERRAFORM Module 1 & 2: Soil Diagnostician & Risk Evaluator
Faithfully takes in survivor observations, detects soil archetypes,
identifies unchecked blindspots, prescribes sensory tests, and
explicitly states what sensory tests cannot prove.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class SoilDiagnostician:
    def __init__(self):
        with open(DATA_DIR / "soil_archetypes.json", "r", encoding="utf-8") as f:
            self.archetype_db = json.load(f)

    def diagnose(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes raw survivor observations and returns structured diagnostic output.
        Input dictionary can contain:
          - previous_use: Optional[str]
          - surface_condition: Optional[str]
          - smells: Optional[str]
          - stains: Optional[str]
          - debris: Optional[str]
          - vegetation: Optional[str]
          - checks_already_done: Optional[List[str]]
          - weather_climate: Optional[str]
        """
        # 1. Faithful Restatement without inventing details
        faithful_intake = {
            "previous_use": observation.get("previous_use") or "Not reported by survivor",
            "surface_condition": observation.get("surface_condition") or "Not reported by survivor",
            "smells": observation.get("smells") or "Not reported by survivor",
            "stains": observation.get("stains") or "Not reported by survivor",
            "debris": observation.get("debris") or "Not reported by survivor",
            "vegetation": observation.get("vegetation") or "Not reported by survivor",
            "checks_already_done": observation.get("checks_already_done") or []
        }

        # 2. Identify what has NOT been checked yet
        all_possible_checks = [
            "Subsurface texture at a hand's depth (Palm Squeeze & Ribbon Test)",
            "Stick penetration depth using body weight (Stick Probe Test)",
            "Petroleum / chemical sheen in shaken water (Jar Sheen Test)",
            "Water drainage speed in a hand-deep hole (Puddle Drain Test)",
            "Scent profile after wetting a clod with clean water",
            "Side-by-side seedling germination comparison (Canary Sprout Bioassay)"
        ]
        
        checks_done_text = " ".join(faithful_intake["checks_already_done"]).lower()
        unchecked_items = []
        for check in all_possible_checks:
            keyword = check.split("(")[0].strip().lower()
            if keyword not in checks_done_text:
                unchecked_items.append(check)

        # 3. Archetype Matching Heuristic
        combined_text = f"{faithful_intake['previous_use']} {faithful_intake['surface_condition']} {faithful_intake['smells']} {faithful_intake['stains']} {faithful_intake['debris']} {faithful_intake['vegetation']}".lower()

        matched_archetype = None
        if any(term in combined_text for term in ["stain", "oil", "fuel", "chemical", "collapsed wall", "broken concrete", "rusted metal", "clump"]):
            matched_archetype = self._get_archetype("disturbed_soil_unknown_safety")
        elif any(term in combined_text for term in ["brick", "concrete", "mortar", "rubble", "crushed stone"]):
            matched_archetype = self._get_archetype("industrial_rubble_mortar")
        elif any(term in combined_text for term in ["compacted", "hardpan", "puddle", "plate", "paved", "flat"]):
            matched_archetype = self._get_archetype("compacted_urban_fill")
        elif any(term in combined_text for term in ["sand", "gravel", "river", "washout", "loose grit"]):
            matched_archetype = self._get_archetype("sandy_gravelly_washout")
        else:
            # Default to safest precautionary archetype
            matched_archetype = self._get_archetype("disturbed_soil_unknown_safety")

        # 4. Unknowns Analysis
        unknowns = [
            "Exact chemical composition and history of previous human activity on this ground.",
            "Presence of odorless, invisible heavy metal salts (lead, cadmium, arsenic) in the mineral layer.",
            "Presence of persistent synthetic herbicides or toxic solvents.",
            "Biological life and earthworm presence beneath the surface crust."
        ]

        # 5. Prescribed No-Equipment Sensory Checks
        recommended_tests = self.archetype_db.get("sensory_diagnostic_tests", [])

        # 6. Qualitative Nutrient & Climate Indicators
        climate_notes = self._evaluate_climate_clues(observation.get("weather_climate", ""), faithful_intake["vegetation"])

        return {
            "status": "success",
            "faithful_restatement": faithful_intake,
            "unverified_blindspots": unchecked_items,
            "detected_archetype": {
                "id": matched_archetype["id"],
                "name": matched_archetype["name"],
                "inherent_risks": matched_archetype["inherent_risks"],
                "safety_rules": matched_archetype["safety_rules"]
            },
            "what_is_unknown": unknowns,
            "prescribed_sensory_checks": recommended_tests,
            "negative_scope_warning": self.archetype_db.get("untested_blindspots_warning"),
            "qualitative_nutrient_clues": climate_notes
        }

    def _get_archetype(self, archetype_id: str) -> Dict[str, Any]:
        for arch in self.archetype_db["archetypes"]:
            if arch["id"] == archetype_id:
                return arch
        return self.archetype_db["archetypes"][0]

    def _evaluate_climate_clues(self, weather_climate: str, vegetation: str) -> Dict[str, Any]:
        text = f"{weather_climate} {vegetation}".lower()
        clues = []
        
        if "stinging nettle" in text or "lush" in text or "dark green" in text:
            clues.append("Dark green leafy weed growth indicates local patches of rich nitrogen from rotting organic matter.")
        else:
            clues.append("Pale, stunted wild weeds suggest nitrogen starvation across the exposed surface.")

        if "rain" in text or "wet" in text or "humid" in text:
            clues.append("Wet weather warning: High risk of fungal spores and anaerobic root drowning. Beds must be elevated knee-high to ensure side aeration.")
        elif "dry" in text or "arid" in text or "hot" in text or "sun" in text:
            clues.append("Dry/hot conditions: Surface will bake into hard crust. Heavy blanket mulching (a hand's depth of dry grass/leaves) is mandatory to retain moisture.")
        else:
            clues.append("Variable conditions: Monitor soil dampness at one finger-joint depth beneath the surface.")

        return {
            "environmental_summary": clues,
            "tactile_check_advice": "Rub moist soil between your palms: if it rolls into a glossy sticky ribbon longer than two thumb-joints, it is heavy clay; if it crumbles like dry breadcrumbs, it is loose loam; if it slips through fingers, it is leached sand."
        }
