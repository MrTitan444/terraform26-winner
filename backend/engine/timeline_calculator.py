"""
TERRAFORM Module 6: Timeline & Survival Buffer Calculator
Computes total harvest horizon including explicit buffers for site clearing,
barrier construction, settling, and bioassay verification, plus dynamic milestone tracking.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

CROP_SLUG_ALIASES = {
    "bush-beans": "bush_beans",
    "peas": "peas_sugar_snap",
    "pumpkin-squash": "winter_squash_pumpkin",
    "dwarf-corn": "dwarf_corn",
    "tomatoes": "tomatoes_determinate",
    "cabbage": "kale_collards",
    "chard": "swiss_chard",
    "kale": "kale_collards",
    "sweet-potato": "sweet_potato_slips",
    "buckwheat": "mustard_greens",
    "radish": "radish_fast",
    "potatoes": "potatoes_container"
}

class TimelineCalculator:
    def __init__(self):
        with open(DATA_DIR / "crops_db.json", "r", encoding="utf-8") as f:
            self.crops = {c["id"]: c for c in json.load(f)["crops"]}

    def calculate_timeline(self, crop_id: str, weeks_passed: float = 0.0) -> Dict[str, Any]:
        """
        Calculates the complete survival harvest timeline including preparation buffers.
        """
        # Resolve any kebab-case frontend slug or alias
        norm_id = crop_id.lower().strip()
        resolved_id = CROP_SLUG_ALIASES.get(norm_id, norm_id.replace("-", "_"))
        crop = self.crops.get(resolved_id, self.crops.get(crop_id, list(self.crops.values())[0]))

        # Explicit Buffer Breakdown (Weeks)
        clearing_buffer_min = 0.5
        clearing_buffer_max = 1.0

        building_buffer_min = 1.0
        building_buffer_max = 1.5

        testing_settling_buffer_min = 1.0
        testing_settling_buffer_max = 1.5

        total_prep_buffer_min = clearing_buffer_min + building_buffer_min + testing_settling_buffer_min
        total_prep_buffer_max = clearing_buffer_max + building_buffer_max + testing_settling_buffer_max

        crop_min = crop["growth_duration_weeks_min"]
        crop_max = crop["growth_duration_weeks_max"]

        total_weeks_min = round(total_prep_buffer_min + crop_min, 1)
        total_weeks_max = round(total_prep_buffer_max + crop_max, 1)

        months_min = round(total_weeks_min / 4.3, 1)
        months_max = round(total_weeks_max / 4.3, 1)

        # Milestone Schedule
        sow_week = total_prep_buffer_max
        sprout_week = round(sow_week + 1.0, 1)
        veg_week = round(sow_week + (crop_min * 0.4), 1)
        bloom_week = round(sow_week + (crop_min * 0.7), 1)
        first_harvest_week = round(total_weeks_min, 1)
        final_harvest_week = round(total_weeks_max, 1)

        milestones = [
            {"period": "Week 0 to 1", "phase": "Site Clearing & Debris Lockdown", "action": "Clear scrap metal, sweep rubble, demarcate bed perimeter 1 pace wide."},
            {"period": "Week 1 to 2", "phase": "Barrier Laying & Bed Construction", "action": "Lay 3 layers of wet cardboard/canvas; stack stones knee-high; fill hugelkultur core."},
            {"period": "Week 2 to 3", "phase": "Settling & Canary Sprout Testing", "action": "Water bed; test puddle drain and run 5-seed canary sprout bioassay."},
            {"period": f"Week {sow_week}", "phase": f"Sowing {crop['name']}", "action": "Sow seeds at correct finger-depth; apply light dry mulch blanket."},
            {"period": f"Week {sprout_week}", "phase": "Seedling Emergence", "action": "Look for twin green seed leaves; guard against birds and slugs with ash collars."},
            {"period": f"Week {veg_week}", "phase": "Rapid Vegetative Growth", "action": "Roots establish deeply; apply first splash of diluted nettle tea or wood ash tea."},
            {"period": f"Week {bloom_week}", "phase": "Flowering / Fruit Setting", "action": "Blossoms emerge; top-dress with a handful of crushed bone meal for phosphorus."},
            {"period": f"Week {first_harvest_week} to {final_harvest_week}", "phase": "Harvest Window & Seed Preservation", "action": "Primary food harvest! Save mature viable seeds for the next crop cycle."}
        ]

        # Dynamic Status based on weeks_passed
        current_status = self._get_status_at_time(weeks_passed, sow_week, veg_week, bloom_week, first_harvest_week, final_harvest_week, crop["name"])

        return {
            "status": "success",
            "crop_id": crop["id"],
            "crop_name": crop["name"],
            "buffer_breakdown_weeks": {
                "site_clearing_and_lockdown": f"{clearing_buffer_min} to {clearing_buffer_max} weeks",
                "bed_construction_and_materials": f"{building_buffer_min} to {building_buffer_max} weeks",
                "settling_and_canary_testing": f"{testing_settling_buffer_min} to {testing_settling_buffer_max} weeks",
                "total_pre_planting_buffer": f"{total_prep_buffer_min} to {total_prep_buffer_max} weeks"
            },
            "crop_growth_duration_weeks": f"{crop_min} to {crop_max} weeks",
            "total_time_to_first_food": {
                "in_weeks": f"{total_weeks_min} to {total_weeks_max} weeks",
                "in_months": f"{months_min} to {months_max} moons (~{months_min} to {months_max} months)"
            },
            "growth_milestones": milestones,
            "current_progress_tracking": {
                "weeks_elapsed": weeks_passed,
                "current_stage": current_status["stage"],
                "immediate_survivor_tasks": current_status["tasks"]
            }
        }

    def _get_status_at_time(self, elapsed: float, sow: float, veg: float, bloom: float, harv_min: float, harv_max: float, name: str) -> Dict[str, Any]:
        if elapsed <= 0:
            return {"stage": "Pre-Dawn: Ready to begin clearing", "tasks": ["Gather tools, clear sharp debris, lay barrier foundation."]}
        elif elapsed < 1.0:
            return {"stage": "Clearing Phase", "tasks": ["Stack large masonry, sweep loose glass, outline bed perimeter."]}
        elif elapsed < sow:
            return {"stage": "Bed Building & Testing Phase", "tasks": ["Finish knee-high walls, pack decaying wood core, run canary sprout test."]}
        elif elapsed < veg:
            return {"stage": f"Seedling Germination of {name}", "tasks": ["Ensure damp soil, protect from night frosts and hungry birds."]}
        elif elapsed < bloom:
            return {"stage": "Vegetative Bulking Phase", "tasks": ["Weed carefully by hand, add a splash of diluted nettle tea to root zone."]}
        elif elapsed < harv_min:
            return {"stage": "Bloom & Maturation Phase", "tasks": ["Protect developing fruit/pods, check under leaves for chewing pests."]}
        elif elapsed <= harv_max:
            return {"stage": "HARVEST TIME!", "tasks": ["Harvest ripe food for survival nutrition; tag best specimens for seed saving."]}
        else:
            return {"stage": "Post-Harvest Bed Reset", "tasks": ["Harvest complete. Prepare bed for next rotation cycle."]}
