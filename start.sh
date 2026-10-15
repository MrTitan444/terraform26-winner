#!/usr/bin/env bash

# TERRAFORM Offline Server Launcher
# Navigate to the repository root directory
cd "$(dirname "$0")" || exit 1

echo "========================================================"
echo "  🌱 Starting TERRAFORM Offline Knowledge Base Server"
echo "========================================================"

# Detect available Python interpreter
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
elif command -v py &>/dev/null; then
    PYTHON_CMD="py"
else
    echo "❌ Error: Python is not installed or not in PATH."
    exit 1
fi

echo "Using: $($PYTHON_CMD --version)"
echo "Local Application: http://localhost:8000"
echo "Press Ctrl+C to stop the server."
echo "========================================================"

exec $PYTHON_CMD run.py serve "$@"
