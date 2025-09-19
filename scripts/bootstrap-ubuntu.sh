#!/usr/bin/env bash
set -euo pipefail

# 1) OS dependancies (Ubuntu/Debian only)
if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y python3 python3-venv python3-pip python3-tk
fi

# 2) Create a virtual environment if one doesnt exist
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# 3) Activate the virtual environment and install Python dependancies
. .venv/bin/activate
python -m pip install --upgrade pip 
pip install -r requirements.txt

echo
echo "✅ Setup complete."
