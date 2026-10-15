"""
TERRAFORM Module 8: Pest & Disease Doctor
Identifies plant pests and pathological symptoms from visual cues and
provides 100% non-chemical, bushcraft and household DIY remedies.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class PestDiseaseDoctor:
    def __init__(self):
        with open(DATA_DIR / "pest_disease_kb.json", "r", encoding="utf-8") as f:
            self.kb = json.load(f)["pests_and_diseases"]

    def diagnose_issue(self, symptom_text: str) -> Dict[str, Any]:
        """
        Takes survivor visual observations and matches pest/disease profiles.
        """
        text = symptom_text.lower()
        matched = []

        for entry in self.kb:
            score = 0
            for sym in entry["visual_symptoms"]:
                keywords = [w.strip("(),.") for w in sym.lower().split() if len(w) > 3]
                if any(k in text for k in keywords):
                    score += 1
            if score > 0:
                matched.append((entry, score))

        # Fallback if no direct keyword match
        if not matched:
            if "bug" in text or "hole" in text or "caterpillar" in text or "worm" in text:
                matched.append((self.kb[0], 1))
            elif "white" in text or "powder" in text or "mold" in text:
                matched.append((self.kb[2], 1))
            elif "spot" in text or "yellow" in text or "blight" in text:
                matched.append((self.kb[4], 1))
            else:
                matched.append((self.kb[0], 1))

        # Sort by match score descending
        matched.sort(key=lambda x: x[1], reverse=True)
        top_match = matched[0][0]

        return {
            "status": "success",
            "detected_issue_id": top_match["id"],
            "category": top_match["category"],
            "visual_symptoms_confirmed": top_match["visual_symptoms"],
            "commonly_affected_crops": top_match["affected_crops"],
            "prescribed_diy_remedies": top_match["diy_remedies"],
            "survivor_safety_note": "Never use automotive fluids, battery acid, or unverified industrial powders for pest control; only use campfire ash, clean camp soap, and botanical garlic/chili sprays."
        }
