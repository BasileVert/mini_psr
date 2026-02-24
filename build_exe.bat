@echo off
setlocal

python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller

pyinstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --windowed ^
  --name mini_psrv1.0.0_win ^
  procedure_recorder\main.py

echo.
echo Build termine: dist\mini_psrv1.0.0_win.exe
endlocal
