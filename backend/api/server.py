from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from engine import TerraformEngine

app = FastAPI(
    title="TERRAFORM Knowledge Base API",
    description="Offline survivor agricultural reasoning engine. Strictly follows non-scientific, hand-measured protocols.",
    version="1.0.0"
)

# Enable CORS for Laptop 2 interface (React, Vite, Vue, Next.js, Electron, mobile)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = TerraformEngine()

# ----------------- Request Models ----------------- #

class SoilDiagnosisRequest(BaseModel):
    previous_use: Optional[str] = Field(None, example="broken concrete, collapsed wall, rusted metal")
    surface_condition: Optional[str] = Field(None, example="clumpy weeds, uneven surface, dark and stained soil")
    smells: Optional[str] = Field(None, example="sharp metallic and faint chemical odor")
    stains: Optional[str] = Field(None, example="dark oily patches on dry ground")
    debris: Optional[str] = Field(None, example="rebar, concrete chunks, scrap iron")
    vegetation: Optional[str] = Field(None, example="patchy clumps of thistles with bare zones")
    checks_already_done: Optional[List[str]] = Field(default=[], example=["smell test", "surface visual scan"])
    weather_climate: Optional[str] = Field(None, example="dry windy warm afternoon")

class CropSelectionRequest(BaseModel):
    soil_safety_tier: Optional[str] = Field("compromised", example="compromised")
    sun_exposure: Optional[str] = Field("any", example="full_sun")
    water_availability: Optional[str] = Field("moderate", example="moderate")
    goal: Optional[str] = Field("balanced", example="rapid_calories")

class RemedyPlanRequest(BaseModel):
    remedy_type: Optional[str] = Field("auto", example="barrier_raised_hugelkultur")
    bed_length_paces: Optional[int] = Field(4, example=4)

class ReadinessCheckRequest(BaseModel):
    target_crop_id: Optional[str] = Field("bush_beans", example="bush_beans")
    puddle_drain_passed: bool = Field(False, example=True)
    fever_heat_passed: bool = Field(False, example=True)
    depth_passed: bool = Field(False, example=True)
    barrier_seal_passed: bool = Field(False, example=True)
    canary_sprout_passed: bool = Field(False, example=True)

class SetbackTriageRequest(BaseModel):
    query: str = Field(..., example="Leaves were chewed down to bare stems overnight by a swarm of bugs")

class PestDiseaseRequest(BaseModel):
    symptom_text: str = Field(..., example="White powdery flour coating on upper leaves of squash")

class ResetEnrichRequest(BaseModel):
    leaf_symptoms: Optional[str] = Field("", example="Oldest bottom leaves are turning bright yellow while top leaves are pale")
    previous_crop_type: Optional[str] = Field("winter_squash_pumpkin", example="winter_squash_pumpkin")

class CaseStudyExtractRequest(BaseModel):
    text: str = Field(..., example="The survivor wakes on a patch of ground: broken concrete, rusted metal, collapsed wall...")
    image_hints: Optional[List[str]] = Field(default=[], example=["rust", "dark_stain", "rubble"])

# ----------------- API Endpoints ----------------- #

@app.get("/favicon.ico")
def favicon():
    fav_path = Path(__file__).resolve().parent.parent.parent / "frontend" / "site" / "assets" / "favicon.svg"
    if fav_path.exists():
        return FileResponse(str(fav_path), media_type="image/svg+xml")
    raise HTTPException(status_code=404)

@app.get("/api/health")
def healthcheck():
    return {
        "status": "online",
        "system": "TERRAFORM Offline Knowledge Base",
        "ground_rule": "Strictly non-scientific, hand-measured survivor protocol"
    }

@app.post("/api/diagnose")
def diagnose_soil(request: SoilDiagnosisRequest):
    """
    Module 1 & 2: Faithful intake, unchecked checklist, soil archetype identification,
    simple sensory tests, and explicit negative scope disclosure.
    """
    return engine.diagnose_soil(request.model_dump())

@app.post("/api/crops")
def select_crops(request: CropSelectionRequest):
    """
    Module 3: Safety-first crop selection and ranking from offline catalog.
    """
    return engine.select_crops(request.model_dump())

@app.post("/api/remedies")
def plan_remedy(request: RemedyPlanRequest):
    """
    Module 4: Immediate remediation protocols in hand-measured amounts (knee-high beds, bucketfuls).
    """
    return engine.plan_remedy(request.model_dump())

@app.post("/api/readiness")
def check_readiness(request: ReadinessCheckRequest):
    """
    Module 5: Pre-planting readiness check comparing tests against crop-specific safety requirements.
    """
    return engine.check_readiness(request.model_dump())

@app.get("/api/timeline/{crop_id}")
def get_timeline(crop_id: str, weeks_passed: float = 0.0):
    """
    Module 6: Crop maturity plus explicit buffer for clearing, building, and testing,
    with growth timeline and progress tracking based on elapsed time.
    """
    return engine.get_timeline(crop_id, weeks_passed)

@app.post("/api/setbacks")
def triage_setback(request: SetbackTriageRequest):
    """
    Module 7: Stepwise emergency recovery triage for crop failures and disasters.
    """
    return engine.triage_setback(request.query)

@app.post("/api/pests-and-diseases")
def diagnose_pests_and_diseases(request: PestDiseaseRequest):
    """
    Module 8: Visual pest and plant disease diagnosis with DIY non-chemical bushcraft recipes.
    """
    return engine.diagnose_pest_or_disease(request.symptom_text)

@app.get("/api/rotation/{current_crop_id}")
def plan_rotation(current_crop_id: str):
    """
    Module 9: 4-stage crop rotation succession planner and pioneer cover crop advisor.
    """
    return engine.plan_rotation(current_crop_id)

@app.post("/api/reset-and-enrich")
def reset_and_enrich_soil(request: ResetEnrichRequest):
    """
    Module 10: Field clearing steps, visual leaf deficiency diagnosis, and DIY campfire/ferment soil feeds.
    """
    return engine.analyze_deficiency_and_reset(request.model_dump())

@app.post("/api/extract-case-study")
def extract_case_study(request: CaseStudyExtractRequest):
    """
    Parses a 300-500 word case study narrative and visual photo hints to autofill all intake fields.
    """
    return engine.extract_case_study(request.text, request.image_hints)

@app.get("/api/database/crops")
def get_all_crops():
    """Direct export of raw offline crops catalog for frontend filtering."""
    return engine.crop_selector.catalog

@app.get("/api/database/archetypes")
def get_all_archetypes():
    """Direct export of raw soil archetypes and sensory tests."""
    return engine.diagnostician.archetype_db

# Mount static frontend site (index.html, analysis.html, etc.)
FRONTEND_SITE_DIR = Path(__file__).resolve().parent.parent.parent / "frontend" / "site"
if FRONTEND_SITE_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_SITE_DIR), html=True), name="frontend")
