@echo off
echo Building executable...
pyinstaller --clean --onefile --noconsole --icon=icon.ico  mono_focus.py
echo Done. Check the dist\ folder.
pause