"""
TERRAFORM Module 5: Readiness Checker
Evaluates if a treated plot/bed is genuinely safe and cultivable for a selected crop.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class ReadinessChecker:
    def __init__(self):
        with open(DATA_DIR / "readiness_checklist.json", "r", encoding="utf-8") as f:
            self.checklist = json.load(f)["readiness_criteria"]
        with open(DATA_DIR / "crops_db.json", "r", encoding="utf-8") as f:
            self.crops = {c["id"]: c for c in json.load(f)["crops"]}

    def check_readiness(self, check_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Input check_results can contain:
          - target_crop_id: str (e.g. "bush_beans", "winter_squash_pumpkin")
          - puddle_drain_passed: bool
          - fever_heat_passed: bool
          - depth_passed: bool
          - barrier_seal_passed: bool
          - canary_sprout_passed: bool
        """
        crop_id = check_results.get("target_crop_id", "bush_beans")
        target_crop = self.crops.get(crop_id, list(self.crops.values())[0])

        evaluations = []
        all_passed = True
        failed_remedies = []

        mapping = {
            "puddle_drain_check": check_results.get("puddle_drain_passed", False),
            "fever_heat_check": check_results.get("fever_heat_passed", False),
            "depth_verification_check": check_results.get("depth_passed", False),
            "barrier_integrity_check": check_results.get("barrier_seal_passed", False),
            "canary_sprout_check": check_results.get("canary_sprout_passed", False)
        }

        for crit in self.checklist:
            passed = mapping.get(crit["id"], False)
            if not passed:
                all_passed = False
                failed_remedies.append({
                    "check": crit["name"],
                    "status": "FAILED",
                    "action_required": crit["fail_fix"]
                })
            evaluations.append({
                "id": crit["id"],
                "name": crit["name"],
                "passed": passed,
                "pass_condition": crit["pass_condition"]
            })

        crop_specific_clearance = {
            "crop_name": target_crop["name"],
            "required_bed_depth": f"{target_crop['root_depth_hand_spans']} hand-spans ({target_crop['min_bed_height']})",
            "safe_for_planting": all_passed
        }

        verdict = "GREENLIGHT: The bed has passed all sensory and biological readiness tests. It is safe to sow seeds." if all_passed else "HOLD: One or more critical readiness gates failed. Apply the corrective actions before planting to prevent seed loss or poisoning."

        return {
            "status": "success",
            "overall_ready": all_passed,
            "verdict": verdict,
            "crop_clearance": crop_specific_clearance,
            "checklist_details": evaluations,
            "corrective_actions_needed": failed_remedies
        }
