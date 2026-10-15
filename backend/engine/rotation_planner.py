"""
TERRAFORM Module 9: Crop Rotation & Cover Crop Planner
Plans sustainable 4-stage succession cycles and prescribes pioneer green manures
to build living soil without commercial inputs.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class RotationPlanner:
    def __init__(self):
        with open(DATA_DIR / "rotation_cycles.json", "r", encoding="utf-8") as f:
            self.cycle_db = json.load(f)
        with open(DATA_DIR / "crops_db.json", "r", encoding="utf-8") as f:
            self.crops_by_id = {c["id"]: c for c in json.load(f)["crops"]}

    def plan_next_cycle(self, current_crop_id: str) -> Dict[str, Any]:
        """
        Determines the current stage and prescribes the next crop rotation phase.
        """
        current_crop = self.crops_by_id.get(current_crop_id, list(self.crops_by_id.values())[0])
        feeder_type = current_crop.get("feeder_type", "heavy_feeder")

        # Determine current stage in 4-stage rotation
        if feeder_type == "heavy_feeder":
            current_stage_idx = 0  # Stage 1
            next_stage_idx = 1     # Move to Stage 2: Light Feeders
        elif feeder_type == "moderate_feeder" or feeder_type == "light_feeder":
            current_stage_idx = 1  # Stage 2
            next_stage_idx = 2     # Move to Stage 3: Nitrogen Fixers / Legumes
        elif feeder_type == "nitrogen_fixer":
            current_stage_idx = 2  # Stage 3
            next_stage_idx = 3     # Move to Stage 4: Cover Crop or Back to Heavy Feeder
        else:
            current_stage_idx = 3
            next_stage_idx = 0

        current_stage = self.cycle_db["standard_4_stage_cycle"][current_stage_idx]
        next_stage = self.cycle_db["standard_4_stage_cycle"][next_stage_idx]

        # Get crop objects for the next stage
        recommended_next_crops = []
        for cid in next_stage.get("crop_types", []):
            if cid in self.crops_by_id:
                crop = self.crops_by_id[cid]
                recommended_next_crops.append({
                    "id": crop["id"],
                    "name": crop["name"],
                    "type": crop["type"],
                    "survivor_tip": crop["survivor_tip"]
                })

        return {
            "status": "success",
            "just_harvested_crop": {
                "id": current_crop["id"],
                "name": current_crop["name"],
                "feeder_classification": feeder_type
            },
            "current_stage": {
                "number": current_stage["stage"],
                "name": current_stage["name"],
                "soil_impact": current_stage["outcome"]
            },
            "next_stage_succession": {
                "number": next_stage["stage"],
                "name": next_stage["name"],
                "soil_demand": next_stage["soil_demand"],
                "input_protocol": next_stage["input_protocol"],
                "recommended_crops": recommended_next_crops
            },
            "pioneer_cover_crop_alternatives": self.cycle_db["pioneer_cover_crops"],
            "golden_rule_reminder": "Always leave legume root systems in the soil upon harvest—cut tops at ground level so nitrogen nodules rot in place to feed the following crop."
        }
