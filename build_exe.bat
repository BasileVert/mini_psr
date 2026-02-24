@echo off
setlocal

python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller

pyinstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --windowed ^
  --name new_psr ^
  procedure_recorder\main.py

echo.
echo Build termine: dist\new_psr.exe
endlocal
