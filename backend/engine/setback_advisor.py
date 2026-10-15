"""
TERRAFORM Module 7: Setback & Crop Failure Triage
Step-by-step emergency recovery protocols for agricultural disasters.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class SetbackAdvisor:
    def __init__(self):
        with open(DATA_DIR / "failure_recovery.json", "r", encoding="utf-8") as f:
            self.setbacks = json.load(f)["setbacks"]

    def triage(self, query: str) -> Dict[str, Any]:
        """
        Matches a survivor's failure description to the most appropriate recovery protocol.
        """
        query_lower = query.lower()
        matched = None

        if any(term in query_lower for term in ["no sprout", "fail to sprout", "zero germination", "not coming up", "empty bed"]):
            matched = self._find_by_id("zero_germination")
        elif any(term in query_lower for term in ["frost", "cold", "frozen", "ice", "freeze", "blackened by cold"]):
            matched = self._find_by_id("unexpected_frost_freeze")
        elif any(term in query_lower for term in ["drought", "wilt", "dry", "scorched", "baked", "heat"]):
            matched = self._find_by_id("severe_drought_and_heat_scorch")
        elif any(term in query_lower for term in ["flood", "waterlog", "puddle", "drowning", "too much rain"]):
            matched = self._find_by_id("flood_waterlogging")
        elif any(term in query_lower for term in ["eaten", "stripped", "chewed", "pest swarm", "bare stems", "bugs devoured"]):
            matched = self._find_by_id("foliage_stripped_by_pests")
        else:
            # Return general resilience checklist if unclear
            matched = self.setbacks[0]

        return {
            "status": "success",
            "matched_setback_id": matched["id"],
            "matched_setback_event": matched["event"],
            "likely_causes": matched["likely_causes"],
            "step_by_step_rescue_actions": matched["step_by_step_recovery"],
            "survivor_encouragement": "Crop setbacks happen on wild ground. Plant roots are remarkably tenacious if you relieve the immediate environmental stress."
        }

    def _find_by_id(self, setback_id: str) -> Dict[str, Any]:
        for s in self.setbacks:
            if s["id"] == setback_id:
                return s
        return self.setbacks[0]
