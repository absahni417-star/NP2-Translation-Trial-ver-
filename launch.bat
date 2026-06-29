@echo off
title NP2 Translator
echo ================================
echo   Neko Project II Translator
echo   Japanese to English Overlay
echo ================================
echo.

:: Check Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

:: Install dependencies if needed
echo Checking dependencies...
pip install -r requirements.txt --quiet

:: Check for API key in config.json
python -c "import json; c=json.load(open('config.json')); exit(0 if c.get('api_key') else 1)" >nul 2>&1
if errorlevel 1 (
    echo.
    echo *** No API key found in config.json ***
    echo Please open config.json and set your Anthropic API key:
    echo   "api_key": "sk-ant-..."
    echo.
    echo Or set the environment variable:
    echo   set ANTHROPIC_API_KEY=sk-ant-...
    echo.
    pause
)

echo.
echo Starting NP2 Translator...
echo Make sure Neko Project II is already running!
echo.
echo Hotkeys:
echo   F1  = Toggle translation overlay on/off
echo   F2  = Force fresh translation
echo   ESC = Quit
echo.

python main.py

pause
