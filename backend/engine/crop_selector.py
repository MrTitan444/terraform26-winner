"""
TERRAFORM Module 3: Safety-First Crop Selector
Filters and ranks ideal survivor crops from offline JSON catalog
based on site constraints, safety tiers, and nutritional survival priorities.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class CropSelector:
    def __init__(self):
        with open(DATA_DIR / "crops_db.json", "r", encoding="utf-8") as f:
            self.catalog = json.load(f)["crops"]

    def select_crops(self, criteria: Dict[str, Any]) -> Dict[str, Any]:
        """
        Criteria input can include:
          - soil_safety_tier: "compromised" | "clean_raised_bed" | "deep_container"
          - sun_exposure: "full_sun" | "partial_shade" | "any"
          - water_availability: "scarce" | "moderate" | "abundant"
          - goal: "rapid_calories" | "fast_survival_greens" | "soil_rebuilding" | "balanced"
        """
        safety_tier = criteria.get("soil_safety_tier", "compromised")
        sun = criteria.get("sun_exposure", "any")
        water = criteria.get("water_availability", "moderate")
        goal = criteria.get("goal", "balanced")

        recommended = []
        cautions = []
        vetoed = []

        for crop in self.catalog:
            # 1. Enforce strict safety veto for compromised/unverified raw ground
            if safety_tier == "compromised":
                if crop["edible_part"] in ["subterranean_root_and_leaves", "subterranean_tubers", "greens_and_bulbs"]:
                    vetoed.append({
                        "crop_id": crop["id"],
                        "name": crop["name"],
                        "reason": "VETOED: Direct root crops absorb concentrated heavy metals and toxins directly through skin contact in suspect ground."
                    })
                    continue
                if crop["safety_tier"] == "bioaccumulator_warning":
                    vetoed.append({
                        "crop_id": crop["id"],
                        "name": crop["name"],
                        "reason": "VETOED FOR FOOD: Known hyper-accumulator of heavy metals (lead/cadmium). Seeds will concentrate poisons."
                    })
                    continue

            # 2. Environmental suitability scoring
            score = 10
            notes = []

            # Sun match
            if sun == "partial_shade":
                if "shade" in crop["sun_requirement"] or "partial" in crop["sun_requirement"]:
                    score += 3
                    notes.append("Tolerates shade cast by collapsed walls.")
                elif crop["sun_requirement"] == "hot_full_sun":
                    score -= 4
                    notes.append("May struggle without full overhead sun.")

            # Water match
            if water == "scarce":
                if crop["drought_tolerance"] in ["high", "very_high"]:
                    score += 3
                    notes.append("High drought resilience.")
                elif crop["drought_tolerance"] == "low":
                    score -= 3
                    notes.append("Needs frequent watering; will wilt in dry rubble.")

            # Goal match
            if goal == "rapid_calories" and crop["caloric_density"] in ["high", "very_high", "exceptionally_high"]:
                score += 4
                notes.append("Excellent caloric density for hunger relief.")
            elif goal == "fast_survival_greens" and crop["growth_duration_weeks_min"] <= 6:
                score += 4
                notes.append("Fast harvest turnaround (under 6 weeks).")
            elif goal == "soil_rebuilding" and crop["feeder_type"] == "nitrogen_fixer":
                score += 5
                notes.append("Recharges soil biology by fixing atmospheric nitrogen.")

            # Recommended list entry
            crop_entry = {
                "id": crop["id"],
                "name": crop["name"],
                "type": crop["type"],
                "feeder_type": crop["feeder_type"],
                "edible_part": crop["edible_part"],
                "growth_duration": f"{crop['growth_duration_weeks_min']} to {crop['growth_duration_weeks_max']} weeks",
                "min_bed_height": crop["min_bed_height"],
                "caloric_density": crop["caloric_density"],
                "key_nutrients": crop["key_nutrients"],
                "companion_friends": crop["companion_friends"],
                "survivor_tip": crop["survivor_tip"],
                "suitability_score": score,
                "notes": notes
            }

            if crop["safety_tier"].startswith("root_caution"):
                cautions.append(f"Caution for {crop['name']}: Only cultivate if isolated in knee-high clean raised beds or containers.")

            recommended.append(crop_entry)

        # Sort recommended by suitability score descending
        recommended.sort(key=lambda x: x["suitability_score"], reverse=True)

        return {
            "status": "success",
            "safety_context": f"Evaluated under '{safety_tier}' condition.",
            "top_recommended_crops": recommended[:6],
            "all_qualified_crops": recommended,
            "cautions": cautions,
            "strictly_vetoed_crops": vetoed
        }
