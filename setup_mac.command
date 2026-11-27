#!/bin/bash
set -eu
cd "$(dirname "$0")"
python3 -m venv .venv
source .venv/bin/activate
if [ ! -d vendor/genagents/.git ]; then
  mkdir -p vendor
  git clone --depth 1 https://github.com/StanfordHCI/genagents.git vendor/genagents
fi
git -C vendor/genagents rev-parse HEAD > vendor/upstream-version.txt
python -m pip install -r requirements.txt -r vendor/genagents/requirements.txt
python -m pip install pyinstaller
cp genagents_settings.py vendor/genagents/simulation_engine/settings.py
echo "Kurulum tamamlandı. API anahtarını ortam değişkeni olarak tanımlayın."
