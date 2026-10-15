"""
TERRAFORM Module 10: Field Reset, Nutrient Deficiency Doctor & Soil Recharge
Guides post-harvest field cleanup, identifies residual nutrient deficiencies
through visual leaf symptom analysis, and formulates organic DIY soil rechargers.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class CycleResetEnricher:
    def __init__(self):
        with open(DATA_DIR / "deficiency_kb.json", "r", encoding="utf-8") as f:
            self.deficiencies = json.load(f)["deficiencies"]

    def analyze_and_enrich(self, observations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Input observations can include:
          - leaf_symptoms: str (e.g. "bottom leaves turned yellow", "purple stems", "brown burnt margins")
          - bed_condition: str
          - previous_crop_type: str
        """
        leaf_text = observations.get("leaf_symptoms", "").lower()

        # Step 1: Field Clearing Protocol
        clearing_steps = [
            {
                "step": 1,
                "action": "Harvest & Seed Salvage",
                "details": "Pick all remaining mature and immature fruits. Set aside the healthiest specimens to dry and harvest seed stock."
            },
            {
                "step": 2,
                "action": "Selective Stalk Removal",
                "details": "If the previous crop was a legume (beans, peas), cut stalks right at the soil surface and leave the root systems undisturbed so the nitrogen nodules decompose in the ground. If previous plants showed fungal spots or blight, remove entire plant and burn away from garden."
            },
            {
                "step": 3,
                "action": "Debris & Mulch Raking",
                "details": "Lightly rake back the surface mulch to inspect the topsoil for grubs or compaction."
            },
            {
                "step": 4,
                "action": "Aeration Without Inversion",
                "details": "Push a pointed branch or rebar into the soil every hand-span to crack open air channels without flipping dead subsoil to the top."
            }
        ]

        # Step 2: Visual Nutrient Deficiency Analysis
        detected_deficiencies = []
        for d in self.deficiencies:
            score = 0
            for sym in d["visual_leaf_symptoms"]:
                keywords = [k for k in sym.lower().split() if len(k) > 4]
                if any(k in leaf_text for k in keywords):
                    score += 1
            if score > 0:
                detected_deficiencies.append(d)

        # Fallback if no specific symptom was passed
        if not detected_deficiencies:
            if "yellow" in leaf_text:
                detected_deficiencies.append(self.deficiencies[0]) # Nitrogen
            elif "purple" in leaf_text or "red" in leaf_text:
                detected_deficiencies.append(self.deficiencies[1]) # Phosphorus
            elif "brown" in leaf_text or "scorch" in leaf_text or "curl" in leaf_text:
                detected_deficiencies.append(self.deficiencies[2]) # Potassium
            else:
                # General balanced re-enrichment
                detected_deficiencies = [self.deficiencies[0], self.deficiencies[1]]

        # Step 3: Re-enrichment Recipes Formulation
        recharge_recipes = []
        for defic in detected_deficiencies:
            recharge_recipes.append({
                "target_nutrient": defic["nutrient"],
                "biological_cause": defic["biological_reason"],
                "primary_diy_recipe": defic["diy_remedy"],
                "alternative_diy_recipe": defic.get("alternative_remedy")
            })

        # Universal Soil Recharge Protocol for Next Cycle
        universal_recharge = [
            "Add 1 bucketful of dark, well-rotted forest compost or leaf-mold per pace.",
            "Sprinkle 1 handful of roasted crushed campfire bone meal per pace.",
            "Dust lightly with 1 double-handful of cold wood ash and crushed charcoal (biochar).",
            "Cap with a two-finger blanket of dry straw or shredded leaves to lock in biology."
        ]

        return {
            "status": "success",
            "field_clearing_protocol": clearing_steps,
            "deficiency_diagnostic_report": {
                "symptoms_evaluated": leaf_text if leaf_text else "General post-harvest reset",
                "identified_deficiencies": [d["nutrient"] for d in detected_deficiencies],
                "tailored_diy_recipes": recharge_recipes
            },
            "universal_bed_recharge_plan": universal_recharge,
            "survivor_rule_compliance": "Zero synthetic chemicals or chemical fertilizer numbers. All nutrition generated from campfire coals, roasted bones, wild weed teas, and fermented organic matter."
        }
