"""
TERRAFORM Knowledge Base Engine
Master integration package for all 10 survivor reasoning capabilities.
"""

from .validator import validate_text, sanitize_text
from .soil_diagnostician import SoilDiagnostician
from .crop_selector import CropSelector
from .remedy_planner import RemedyPlanner
from .readiness_checker import ReadinessChecker
from .timeline_calculator import TimelineCalculator
from .setback_advisor import SetbackAdvisor
from .pest_disease_doctor import PestDiseaseDoctor
from .rotation_planner import RotationPlanner
from .cycle_reset_enricher import CycleResetEnricher

class TerraformEngine:
    def __init__(self):
        self.diagnostician = SoilDiagnostician()
        self.crop_selector = CropSelector()
        self.remedy_planner = RemedyPlanner()
        self.readiness_checker = ReadinessChecker()
        self.timeline_calculator = TimelineCalculator()
        self.setback_advisor = SetbackAdvisor()
        self.pest_doctor = PestDiseaseDoctor()
        self.rotation_planner = RotationPlanner()
        self.cycle_resetter = CycleResetEnricher()

    def diagnose_soil(self, observation: dict) -> dict:
        result = self.diagnostician.diagnose(observation)
        return self._sanitize_dict(result)

    def select_crops(self, criteria: dict) -> dict:
        result = self.crop_selector.select_crops(criteria)
        return self._sanitize_dict(result)

    def plan_remedy(self, preference: dict) -> dict:
        result = self.remedy_planner.plan_remedy(preference)
        return self._sanitize_dict(result)

    def check_readiness(self, check_results: dict) -> dict:
        result = self.readiness_checker.check_readiness(check_results)
        return self._sanitize_dict(result)

    def get_timeline(self, crop_id: str, weeks_passed: float = 0.0) -> dict:
        result = self.timeline_calculator.calculate_timeline(crop_id, weeks_passed)
        return self._sanitize_dict(result)

    def triage_setback(self, query: str) -> dict:
        result = self.setback_advisor.triage(query)
        return self._sanitize_dict(result)

    def diagnose_pest_or_disease(self, symptom_text: str) -> dict:
        result = self.pest_doctor.diagnose_issue(symptom_text)
        return self._sanitize_dict(result)

    def plan_rotation(self, current_crop_id: str) -> dict:
        result = self.rotation_planner.plan_next_cycle(current_crop_id)
        return self._sanitize_dict(result)

    def analyze_deficiency_and_reset(self, observations: dict) -> dict:
        result = self.cycle_resetter.analyze_and_enrich(observations)
        return self._sanitize_dict(result)

    def _sanitize_dict(self, data: any) -> any:
        """Recursively sanitizes all strings in a data structure to adhere to survivor rules."""
        if isinstance(data, str):
            return sanitize_text(data)
        elif isinstance(data, dict):
            return {k: self._sanitize_dict(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._sanitize_dict(item) for item in data]
        return data

__all__ = ["TerraformEngine", "validate_text", "sanitize_text"]
