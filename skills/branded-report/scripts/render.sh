#!/usr/bin/env bash
# Render a branded PDF report:  bash render.sh path/to/report.json [--out file.pdf] [--html]
# The first run builds a private Python environment with Playwright (about a minute, one time).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="${BRANDED_REPORT_VENV:-$HOME/.cache/branded-report/venv}"

if ! "$VENV/bin/python" -c "import playwright, pypdf" >/dev/null 2>&1; then
  PY="$(command -v python3 || true)"
  if [ -z "$PY" ]; then
    echo "python3 is not installed. On a Mac run: xcode-select --install, then try again." >&2
    exit 2
  fi
  echo "First run: setting up Playwright in $VENV (one time)..." >&2
  mkdir -p "$(dirname "$VENV")"
  [ -x "$VENV/bin/python" ] || "$PY" -m venv "$VENV"
  "$VENV/bin/python" -m pip install --quiet --disable-pip-version-check playwright pypdf
fi

exec "$VENV/bin/python" "$HERE/render.py" "$@"
