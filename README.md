# TERRAFORM — Offline Agricultural Intelligence System
> **Full Stack Edition | Frontend (UI) + Backend (Knowledge Base)**

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
terraform/
├── frontend/                             # 🖥️ FRONTEND INTERFACE (HTML, CSS, JS)
│   ├── site/                             # 9-page survivor UI
│   │   ├── index.html                    # Welcome screen & ground rules
│   │   ├── input.html                    # Land diagnosis intake form
│   │   ├── analysis.html                 # Missing checks & archetype analysis
│   │   ├── protocol.html                 # Step-by-step barrier & bed building guide
│   │   ├── next-action.html              # Readiness gates & task board
│   │   ├── crops.html                    # 10 staple crop boxes & filters
│   │   ├── timeframe.html                # Growth timeline & buffer chart
│   │   ├── planting.html                 # Visual planting profile & spacing
│   │   ├── care-harvest.html             # Care, triage fixes, & 4-stage rotation
│   │   └── assets/                       # CSS, icons, images, & scripts
│   ├── source/build.py                   # Site template generator
│   ├── references/                       # Style guides, images, knowledge base notes
│   └── HANDOFF.md                        # UI design specs & component notes
│
├── backend/                              # 🧠 BACKEND KNOWLEDGE BASE ENGINE
│   ├── data/                             # Offline JSON Knowledge Databases
│   │   ├── crops_db.json                 # 15+ survivor staple crops with complete metadata
│   │   ├── soil_archetypes.json          # 5 terrain archetypes + sensory tests + negative scope
│   │   ├── remedies_catalog.json         # DIY barrier & hugelkultur recipes in hand units
│   │   ├── readiness_checklist.json      # Pre-planting sensory gates (drain, fever, canary sprout)
│   │   ├── pest_disease_kb.json          # Visual symptoms & organic bushcraft remedies
│   │   ├── deficiency_kb.json            # Leaf-reading deficiency keys & campfire recipes
│   │   ├── rotation_cycles.json          # 4-stage succession cycles & pioneer cover crops
│   │   └── failure_recovery.json         # Stepwise triage for agricultural disasters
│   ├── engine/                           # Expert Reasoning Logic (Deterministic & Safe)
│   │   ├── validator.py                  # Strict survivor constraint validator
│   │   ├── soil_diagnostician.py         # Modules 1 & 2: Faithful intake & risk checks
│   │   ├── crop_selector.py              # Module 3: Safety veto & crop ranking from JSON catalog
│   │   ├── remedy_planner.py             # Module 4: Hand-measured remediation recipes
│   │   ├── readiness_checker.py          # Module 5: Pre-planting verification engine
│   │   ├── timeline_calculator.py        # Module 6: Harvest horizon + explicit prep buffers
│   │   ├── setback_advisor.py            # Module 7: Disaster recovery triage
│   │   ├── pest_disease_doctor.py        # Module 8: Plant disease & insect doctor
│   │   ├── rotation_planner.py           # Module 9: Crop rotation & cover crop advisor
│   │   └── cycle_reset_enricher.py       # Module 10: Field reset & organic soil rechargers
│   ├── ai/                               # Offline LLM & Reasoning Bridge
│   │   └── reasoning_engine.py           # System prompts, few-shot unseen scenarios, Ollama bridge
│   ├── api/                              # REST Service & Static Server
│   │   └── server.py                     # FastAPI server mounting frontend & API endpoints
│   ├── client_mock/                      # Integration Package
│   │   ├── mock_contract.json            # Full mock request/response JSON payloads
│   │   └── test_scenarios.py             # Automated test suite (24/24 passing)
│   └── main.py                           # Backend CLI launcher
│
├── run.py                                # 🚀 Root Unified Launcher (Runs both Frontend & Backend)
├── LICENSE                               # Open-source MIT License
└── README.md                             # Documentation & user guide
```

---

## 🚀 Quick Start (Run Locally)

### 1. Launch the Complete System (Frontend + Backend)
From the project root folder:
```powershell
python run.py
```
This launches a single local server running **both** the interactive web UI and the reasoning API:
- **Web App (Frontend):** [http://localhost:8000](http://localhost:8000)
- **Backend API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Technical Specs (ReDoc):** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **System Health Check:** [http://localhost:8000/api/health](http://localhost:8000/api/health)

### 2. Run the Judging Verification Suite
Verifies all 10 capabilities against the Hackathon Starter Scenario, the 5 archetypes, an unseen judging variation, and strict survivor constraint checks:
```powershell
python run.py test
```

### 3. Interactive Survivor Shell (Judging Q&A)
```powershell
python run.py interactive
```

---

## 📡 REST API Reference

| Endpoint | Method | Capability / Description |
| :--- | :---: | :--- |
| `/` | `GET` | **Frontend Website:** Serves `frontend/site/index.html` |
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
