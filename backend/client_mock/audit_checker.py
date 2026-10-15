"""
TERRAFORM Comprehensive System Audit & Bug Detector
Audits frontend assets, links, CSS, JavaScript, and backend endpoints.
"""

import sys
import re
from pathlib import Path
from starlette.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "backend"))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from api.server import app

def run_audit():
    print("=" * 65)
    print("  TERRAFORM SYSTEM AUDIT & ISSUE DETECTOR")
    print("=" * 65)

    client = TestClient(app)
    issues_found = []

    # 1. Audit Frontend Files and Internal Links
    print("\n[AUDIT 1] Checking Frontend HTML Assets and Links...")
    site_dir = ROOT_DIR / "frontend" / "site"
    html_files = list(site_dir.glob("*.html"))
    print(f"  Found {len(html_files)} HTML pages.")

    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")

        # Check script sources
        for src in re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', content):
            if not src.startswith("http"):
                target = site_dir / src
                if not target.exists():
                    issues_found.append(f"Broken script link in {html_file.name}: '{src}' not found on disk")

        # Check link stylesheets
        for href in re.findall(r'<link[^>]+href=["\']([^"\']+)["\']', content):
            if not href.startswith("http"):
                target = site_dir / href
                if not target.exists():
                    issues_found.append(f"Broken stylesheet link in {html_file.name}: '{href}' not found on disk")

        # Check images
        for img in re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content):
            if not img.startswith("http"):
                target = site_dir / img
                if not target.exists():
                    issues_found.append(f"Broken image in {html_file.name}: '{img}' not found on disk")

        # Check internal anchor links
        for a in re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', content):
            clean_a = a.split("?")[0].split("#")[0]
            if clean_a and not clean_a.startswith(("http", "mailto:", "tel:", "javascript:")):
                target = site_dir / clean_a
                if not target.exists():
                    issues_found.append(f"Broken anchor in {html_file.name}: '{a}' points to non-existent file")

    if not issues_found:
        print("  ✓ All HTML script tags, stylesheets, images, and anchor links are valid.")

    # 2. Audit CSS File for Missing Background Images
    print("\n[AUDIT 2] Checking CSS asset references...")
    css_file = site_dir / "assets" / "css" / "style.css"
    if css_file.exists():
        css_content = css_file.read_text(encoding="utf-8")
        for url in re.findall(r'url\(["\']?([^"\')]+)["\']?\)', css_content):
            if not url.startswith("data:") and not url.startswith("http"):
                target = css_file.parent / url
                if not target.exists():
                    issues_found.append(f"Broken CSS asset: '{url}' in style.css resolved to missing file {target}")
                else:
                    print(f"  ✓ CSS Asset '{url}' resolved successfully.")

    # 3. HTTP Route Verification (FastAPI)
    print("\n[AUDIT 3] Checking HTTP Routes via FastAPI TestClient...")
    routes_to_test = [
        ("/", 200),
        ("/index.html", 200),
        ("/input.html", 200),
        ("/analysis.html", 200),
        ("/protocol.html", 200),
        ("/next-action.html", 200),
        ("/crops.html", 200),
        ("/timeframe.html", 200),
        ("/planting.html", 200),
        ("/care-harvest.html", 200),
        ("/assets/css/style.css", 200),
        ("/assets/js/app.js", 200),
        ("/assets/js/crops-data.js", 200),
        ("/assets/img/tree.jpg", 200),
        ("/api/health", 200),
        ("/docs", 200),
    ]

    for path, expected_status in routes_to_test:
        res = client.get(path)
        if res.status_code != expected_status:
            issues_found.append(f"HTTP GET {path} returned status {res.status_code}, expected {expected_status}")
        else:
            print(f"  ✓ GET {path:25} -> {res.status_code} OK")

    # 4. Frontend-to-Backend Wiring Audit
    print("\n[AUDIT 4] Checking Frontend-to-Backend API Integration...")
    app_js_path = site_dir / "assets" / "js" / "app.js"
    app_js_content = app_js_path.read_text(encoding="utf-8")
    
    if "fetch(" not in app_js_content and "axios" not in app_js_content:
        issues_found.append("MAJOR INTEGRATION GAP: frontend/site/assets/js/app.js has zero API calls (no fetch() or XMLHttpRequest). It operates purely on client-side localStorage without communicating with the backend reasoning engine.")
    else:
        print("  ✓ Frontend makes network calls to backend API.")

    # 5. Offline Font Dependency Audit
    print("\n[AUDIT 5] Checking Offline Readiness (Fonts & External Resources)...")
    external_fonts = []
    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        if "fonts.googleapis.com" in content:
            external_fonts.append(html_file.name)
    if external_fonts:
        issues_found.append(f"OFFLINE RISK: The following pages rely on Google Fonts over the internet: {', '.join(external_fonts)}. If the judging laptop has no internet access, fonts will fallback to system Georgia/serif.")

    # 6. Summary of Audit
    print("\n" + "=" * 65)
    print(f"  AUDIT COMPLETE: {len(issues_found)} ISSUES / GAPS DETECTED")
    print("=" * 65)

    for i, issue in enumerate(issues_found, 1):
        print(f"  {i}. {issue}")

    return issues_found

if __name__ == "__main__":
    run_audit()
