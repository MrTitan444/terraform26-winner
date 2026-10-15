"""
TERRAFORM Unified Launcher
Runs the complete TERRAFORM system (Frontend + Backend) locally.
"""

import sys
import argparse
from pathlib import Path

# Add backend directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

# Ensure Windows terminal handles UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def start_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    import uvicorn
    print("\n" + "=" * 65)
    print("  🌱 TERRAFORM UNIFIED SYSTEM (FRONTEND + BACKEND)")
    print("=" * 65)
    print(f"  👉 Web Application (Frontend): http://localhost:{port}")
    print(f"  👉 Backend API Swagger Docs:   http://localhost:{port}/docs")
    print(f"  👉 ReDoc Technical Specs:      http://localhost:{port}/redoc")
    print(f"  👉 Health Check:               http://localhost:{port}/api/health")
    print("=" * 65)
    print("  Press Ctrl+C to stop the server.\n")
    uvicorn.run("api.server:app", host=host, port=port, reload=reload)

def run_tests():
    from client_mock.test_scenarios import run_tests as execute_suite
    execute_suite()

def run_interactive():
    from engine import TerraformEngine
    engine = TerraformEngine()

    print("\n" + "=" * 60)
    print("  TERRAFORM OFFLINE REASONING TERMINAL (SURVIVOR MODE)")
    print("  Type 'exit' to quit. Describe any ground scenario.")
    print("=" * 60 + "\n")

    while True:
        try:
            user_input = input("TERRAFORM> ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Logging off TERRAFORM system.")
                break

            diag = engine.diagnose_soil({
                "surface_condition": user_input,
                "previous_use": "Survivor observed terrain",
                "checks_already_done": []
            })

            print("\n" + "-" * 50)
            print(f"[DIAGNOSIS]: {diag['detected_archetype']['name']}")
            print("-" * 50)
            print("Inherent Hazards:")
            for r in diag['detected_archetype']['inherent_risks']:
                print(f"  * {r}")
            print("\nNon-Lab Sensory Checks:")
            for t in diag['prescribed_sensory_checks'][:2]:
                print(f"  * {t['name']}: {t['instructions']}")
            print("\nNegative Scope Warning:")
            print(f"  ! {diag['negative_scope_warning']}")
            print("-" * 50 + "\n")

        except (KeyboardInterrupt, EOFError):
            break

def main():
    parser = argparse.ArgumentParser(description="TERRAFORM Unified Launcher")
    parser.add_argument("command", nargs="?", default="serve", choices=["serve", "test", "interactive"],
                        help="Action to perform (default: serve)")
    parser.add_argument("--host", default="0.0.0.0", help="Host interface (default 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port (default 8000)")
    parser.add_argument("--reload", action="store_true", help="Auto reload on file change")

    args = parser.parse_args()

    if args.command == "serve":
        start_server(args.host, args.port, args.reload)
    elif args.command == "test":
        run_tests()
    elif args.command == "interactive":
        run_interactive()

if __name__ == "__main__":
    main()
