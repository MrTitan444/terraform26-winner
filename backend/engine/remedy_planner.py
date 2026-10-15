"""
TERRAFORM Module 4: Immediate Remedy Planner
Generates practical remediation protocols strictly adhering to hand-measured
amounts and zero scientific/lab readings.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class RemedyPlanner:
    def __init__(self):
        with open(DATA_DIR / "remedies_catalog.json", "r", encoding="utf-8") as f:
            self.catalog = json.load(f)["remedies"]

    def plan_remedy(self, preference: Dict[str, Any]) -> Dict[str, Any]:
        """
        Input preference can include:
          - remedy_type: "barrier_raised_hugelkultur" | "salvage_container_isolation" | "sheet_mulch_lasagna_bed" | "auto"
          - bed_length_paces: int (default 4 paces)
          - available_materials: List[str]
        """
        remedy_type = preference.get("remedy_type", "auto")
        paces = int(preference.get("bed_length_paces", 4))

        if remedy_type == "auto":
            # Default to safest universal protocol
            remedy = self.catalog[0]
        else:
            remedy = next((r for r in self.catalog if r["id"] == remedy_type), self.catalog[0])

        # Calculate exact hand-measured material quantities based on bed size
        quantities = self._calculate_hand_quantities(remedy["id"], paces)

        return {
            "status": "success",
            "selected_remedy_id": remedy["id"],
            "remedy_name": remedy["name"],
            "target_scenario": remedy["target_scenario"],
            "safety_guarantee": remedy["safety_guarantee"],
            "hand_measured_materials_bill": quantities,
            "step_by_step_instructions": remedy["step_by_step_instructions"],
            "survivor_rule_compliance": "All quantities expressed in bucketfuls, handfuls, armfuls, knee-height, and walking paces. Zero lab values."
        }

    def _calculate_hand_quantities(self, remedy_id: str, paces: int) -> List[str]:
        if remedy_id == "barrier_raised_hugelkultur":
            return [
                f"Sufficient salvaged stone, brick, or masonry chunks to build a knee-high perimeter wall ({paces} paces long by 1 pace wide).",
                f"At least {paces * 3} broad sheets of thick cardboard, burlap, or heavy canvas (to lay 3 overlapping layers).",
                f"Approximately {paces * 2} armfuls of forearm-thick rotting logs and fallen tree branches (hugelkultur core).",
                f"{paces * 2} armfuls of green weed trimmings and freshly cut leafy branches.",
                f"{paces * 2} bucketfuls of rich forest topsoil / leaf-mold per pace ({paces * 2} bucketfuls total).",
                f"{paces * 1} bucketful of well-rotted dark compost per pace ({paces} bucketfuls total).",
                f"{paces * 1} double-handful of cold campfire wood ash and crushed charcoal."
            ]
        elif remedy_id == "salvage_container_isolation":
            return [
                "2 to 4 salvaged food-grade barrels, metal drums, wooden crates, or stacked tires.",
                "1 bucketful of coarse gravel or clean broken brick chunks for base drainage.",
                "3 bucketfuls of clean forest soil per container.",
                "1 bucketful of rotted leaf-mold per container.",
                "2 double-handfuls of crushed campfire charcoal per container."
            ]
        else:  # sheet_mulch_lasagna_bed
            return [
                f"Cardboard sheets to blanket {paces} paces of ground (at least 2 layers deep).",
                f"{paces * 3} armfuls of dry fallen brown leaves and shredded straw.",
                f"{paces * 3} armfuls of fresh green grass trimmings and young nettles.",
                f"{paces} bucketfuls of rich decomposed compost for surface seed pockets."
            ]
