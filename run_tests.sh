#!/usr/bin/env bash
# Runs the Dash test suite. Exits 0 if every test passes, 1 otherwise.
set -u
cd "$(dirname "$0")"

if [ -d venv ]; then
  # shellcheck disable=SC1091
  source venv/bin/activate 2>/dev/null || source venv/Scripts/activate
fi

if python -m pytest test_app.py; then
  echo "All tests passed."
  exit 0
else
  echo "Tests failed."
  exit 1
fi
