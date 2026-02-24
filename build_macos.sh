#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt pyinstaller

pyinstaller \
  --noconfirm \
  --clean \
  --onefile \
  --windowed \
  --name mini_psrv1.0.0_macos \
  procedure_recorder/main.py

echo
echo "Build termine: dist/mini_psrv1.0.0_macos"
