# TERRAFORM — Offline Agricultural Intelligence System
> **Tech Event Edition | Laptop 1: Knowledge Base Engine**

---

## 🧭 The Premise & Survivor Ground Rules
You wake on unknown, post-collapse terrain with no memory, no agricultural background, and one tool between you and starvation: **TERRAFORM**.

### The Non-Negotiable Survivor Ground Rules
1. **Zero Scientific Readings:** The system **never** asks for, quotes, or depends on scientific readings or fixed chemical values (no pH numbers, NPK ppm, electrical conductivity, or chemical formulas).
2. **Everyday Hand-Measurements Only:**
   - *Volumes:* "a handful", "two cupped palms", "a bucketful" (~10L), "an armful", "a wheelbarrow-load".
   - *Lengths & Depths:* "a finger-width", "a thumb-joint", "a hand-span" (~20 cm), "a hand's depth", "knee-high" (~45 cm), "a pace" (~1 meter).
   - *Time:* "sun cycles" (days), "moon cycles" (~4 weeks / months), "seasons".
3. **Safety-First Precautionary Principle:**
   - Dark stains, chemical smells, rusted metal, or demolition rubble = **assumed hazardous (heavy metals, petrochemicals)**.
   - Root crops (potatoes, carrots, radishes) are **strictly forbidden** directly in suspect ground.
   - Mandates **physical barrier isolation** (3 layers of wet canvas/cardboard) + **knee-high raised beds** or deep containers.
4. **Faithful Intake:** Restates the survivor's observations without hallucinating, and itemizes what has **not yet been checked**.
5. **Explicit Negative Scope:** Explicitly states what household/sensory checks **CANNOT prove** (cannot detect invisible heavy metals or odorless pesticides).

---

## 📁 Project Structure

```
c:\Users\win 10\OneDrive\Documents\terraform\
├── data/                                 # Offline JSON Database Layer
│   ├── crops_db.json                     # 15+ survivor staple crops with complete metadata
│   ├── soil_archetypes.json              # 5 terrain archetypes + sensory tests + negative scope
│   ├── remedies_catalog.json             # DIY barrier & hugelkultur recipes in hand units
│   ├── readiness_checklist.json          # Pre-planting sensory gates (drain, fever, canary sprout)
│   ├── pest_disease_kb.json              # Visual symptoms & organic bushcraft remedies
│   ├── deficiency_kb.json                # Leaf-reading deficiency keys & campfire recipes
│   ├── rotation_cycles.json              # 4-stage succession cycles & pioneer cover crops
│   └── failure_recovery.json             # Stepwise triage for agricultural disasters
├── engine/                               # Expert Reasoning Logic (Deterministic & Safe)
│   ├── validator.py                      # Enforces zero-scientific-terms survivor rulebook
│   ├── soil_diagnostician.py             # Modules 1 & 2: Faithful intake, archetypes & sensory tests
│   ├── crop_selector.py                  # Module 3: Safety veto & crop ranking from JSON catalog
│   ├── remedy_planner.py                 # Module 4: Hand-measured remediation recipes
│   ├── readiness_checker.py              # Module 5: Pre-planting verification engine
│   ├── timeline_calculator.py            # Module 6: Harvest horizon + explicit prep buffers
│   ├── setback_advisor.py                # Module 7: Disaster recovery triage
│   ├── pest_disease_doctor.py            # Module 8: Plant disease & insect doctor
│   ├── rotation_planner.py               # Module 9: Crop rotation & cover crop advisor
│   └── cycle_reset_enricher.py           # Module 10: Field reset & organic soil rechargers
├── ai/                                   # Local Offline LLM & Reasoning Bridge
│   └── reasoning_engine.py               # System prompts, few-shot unseen scenarios, Ollama bridge
├── api/                                  # REST Service for Laptop 2 (Interface Team)
│   └── server.py                         # FastAPI server with CORS & Swagger UI
├── client_mock/                          # Integration Package for Interface Team
│   ├── mock_contract.json                # Complete sample request/response JSON payloads
│   └── test_scenarios.py                 # Automated verification test suite (24/24 passing)
├── main.py                               # Master CLI (serve, test, interactive)
└── README.md                             # System documentation
```

---

## 🚀 Quick Start Instructions

### 1. Launch the API Server (For Laptop 2 Integration)
From the project folder, run:
```powershell
python main.py serve
```
- **API URL:** `http://localhost:8000`
- **Interactive Swagger UI:** `http://localhost:8000/docs`
- **ReDoc Documentation:** `http://localhost:8000/redoc`

*Note: CORS is fully enabled (`*`), so Laptop 2 can connect from React, Vite, Next.js, Electron, or mobile apps over the local Wi-Fi / hotspot network.*

### 2. Run the Judging & Verification Test Suite
Verifies all 10 capabilities against the Hackathon Starter Scenario, the 5 archetypes, an unseen judging variation, and strict survivor constraint checks:
```powershell
python main.py test
```

### 3. Launch the Interactive Survivor Shell
```powershell
python main.py interactive
```

---

## 📡 REST API Reference (For Laptop 2 Interface Team)

| Endpoint | Method | Capability / Description |
| :--- | :---: | :--- |
| `/api/health` | `GET` | Health check and system verification |
| `/api/diagnose` | `POST` | **Module 1 & 2:** Soil intake, unchecked checklist, archetype detection, sensory tests, negative scope |
| `/api/crops` | `POST` | **Module 3:** Safety-first crop selection, caloric ranking, strict root crop vetoes |
| `/api/remedies` | `POST` | **Module 4:** Immediate remediation protocols in hand units (knee-high beds, bucketfuls) |
| `/api/readiness` | `POST` | **Module 5:** Pre-planting readiness gate check vs crop root requirements |
| `/api/timeline/{crop_id}` | `GET` | **Module 6:** Maturity + explicit buffers (clearing, building, testing) + dynamic milestones |
| `/api/setbacks` | `POST` | **Module 7:** Step-by-step triage for agricultural disasters (frost, drought, bugs) |
| `/api/pests-and-diseases` | `POST` | **Module 8:** Visual symptom matching + DIY bushcraft recipes (ash, milk wash, chili spray) |
| `/api/rotation/{crop_id}` | `GET` | **Module 9:** 4-stage crop rotation planner & pioneer green manures |
| `/api/reset-and-enrich` | `POST` | **Module 10:** Field clearing, leaf deficiency diagnosis, and DIY organic soil feeds |
| `/api/database/crops` | `GET` | Direct export of all 15+ crops in JSON catalog |
| `/api/database/archetypes` | `GET` | Direct export of all 5 archetypes and sensory tests |

---

## 🛡️ Built for Judging: Unseen Scenario Reasoning
TERRAFORM was built not just to pass the starter scenario, but to generalize across any terrain variation handed to the team at judging time:
1. **Compacted Urban Hardpan / Footing Fill**
2. **Demolition Rubble & Mortar Fill**
3. **Disturbed Ground of Unknown Safety & Industrial Debris**
4. **Exhausted Silt / Crusted Dead Topsoil**
5. **Coarse Sand & Leached River Gravel**
