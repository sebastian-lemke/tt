@echo off
echo Starting build process...

:: Optional: Ensure pyinstaller is up to date
pip install --upgrade pyinstaller

:: Run the PyInstaller command
python -m PyInstaller --onefile --clean tt/tt.py

echo.
echo Build complete! Check the "dist" folder for your executable.
pause