"""
TERRAFORM Master Command Center
Entry point for serving the API to Laptop 2, running tests, or entering interactive survivor mode.
"""

import sys
import argparse
import uvicorn
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# Ensure Windows terminal UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def serve(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    print(f"\n=======================================================")
    print(f"  LAUNCHING TERRAFORM API SERVER ON http://{host}:{port}")
    print(f"  Swagger Docs (for Laptop 2 UI Team): http://localhost:{port}/docs")
    print(f"  ReDoc: http://localhost:{port}/redoc")
    print(f"=======================================================\n")
    uvicorn.run("api.server:app", host=host, port=port, reload=reload)

def test():
    from client_mock.test_scenarios import run_tests
    run_tests()

def interactive():
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

            # Run diagnosis
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
    parser = argparse.ArgumentParser(description="TERRAFORM Knowledge Base Engine CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start the FastAPI REST server for Laptop 2")
    serve_parser.add_argument("--host", default="0.0.0.0", help="Host interface (default 0.0.0.0)")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port (default 8000)")
    serve_parser.add_argument("--reload", action="store_true", help="Auto reload on file change")

    # Test command
    subparsers.add_parser("test", help="Run the automated scenario test suite")

    # Interactive command
    subparsers.add_parser("interactive", help="Start interactive survivor CLI shell")

    args = parser.parse_args()

    if args.command == "serve":
        serve(args.host, args.port, args.reload)
    elif args.command == "test":
        test()
    elif args.command == "interactive":
        interactive()
    else:
        # Default to interactive if no args, or print help
        parser.print_help()

if __name__ == "__main__":
    main()
