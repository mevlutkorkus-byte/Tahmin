#!/bin/bash
set -eu
cd "$(dirname "$0")"
source .venv/bin/activate
export PYTHONPATH="$PWD/vendor/genagents:${PYTHONPATH:-}"
python simulation_ui.py
