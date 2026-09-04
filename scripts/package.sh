#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 /Users/ashishpunj/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
for skill in skills/*; do
  python3 /Users/ashishpunj/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$skill"
done
mkdir -p dist
rm -f dist/meta-growth-system-plugin.zip
zip -qr dist/meta-growth-system-plugin.zip . \
  -x '.git/*' 'dist/*' '*/__pycache__/*' '*.pyc' '.DS_Store'
echo "Built dist/meta-growth-system-plugin.zip"
