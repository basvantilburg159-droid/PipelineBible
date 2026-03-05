@echo off
REM Pipe Standards Pro v12 - Windows Launcher
REM This keeps the window open and shows errors

echo ========================================
echo Pipe Standards Pro v12
echo ========================================
echo.

REM Check Python
echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from python.org
    pause
    exit /b 1
)

REM Check virtual environment
echo.
echo Checking virtual environment...
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing/updating dependencies...
pip install -q -r requirements.txt

REM Check imports
echo.
echo Checking imports...
python -c "import tkinter; print('✓ tkinter OK')" || (echo ✗ tkinter FAILED & pause & exit /b 1)
python -c "import matplotlib; print('✓ matplotlib OK')" || (echo ✗ matplotlib FAILED & pause & exit /b 1)
python -c "import numpy; print('✓ numpy OK')" || (echo ✗ numpy FAILED & pause & exit /b 1)

REM Run application
echo.
echo ========================================
echo Starting Pipe Standards Pro v12...
echo ========================================
echo.

python pipe_standards_v12.py

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start!
    echo Check the error messages above.
    pause
)
