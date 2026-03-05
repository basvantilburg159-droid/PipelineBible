@echo off
REM PipelineBible Launcher voor Windows
REM Dit script houdt de console open zodat je de output kunt lezen

echo ============================================================
echo PipelineBible v1.1 - Pipeline Standards Tool
echo ============================================================
echo.

REM Check of Python geinstalleerd is
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is niet geinstalleerd!
    echo.
    echo Download Python van: https://www.python.org/downloads/
    echo Zorg dat je "Add Python to PATH" aanvinkt tijdens installatie.
    echo.
    pause
    exit /b 1
)

echo Python gevonden!
echo.

REM Vraag gebruiker wat te doen
echo Wat wil je doen?
echo.
echo 1. Test PipelineBible (alle functies testen)
echo 2. Demo (laat functionaliteit zien)
echo 3. Interactieve Python console
echo 4. Afsluiten
echo.

set /p choice="Kies optie (1-4): "

if "%choice%"=="1" (
    echo.
    echo Running test suite...
    echo.
    python test_pipelinebible.py
    echo.
    echo ============================================================
    echo Tests voltooid!
    echo ============================================================
    goto end
)

if "%choice%"=="2" (
    echo.
    echo Running demo...
    echo.
    python PipelineBible.py
    echo.
    echo ============================================================
    echo Demo voltooid!
    echo ============================================================
    goto end
)

if "%choice%"=="3" (
    echo.
    echo Starting Python console...
    echo Importeer modules met: from PipelineBible import PipeLookup, FlangeLookup
    echo.
    python -i -c "from PipelineBible import *; print('PipelineBible modules geladen! Type help(PipeLookup) voor hulp.')"
    goto end
)

if "%choice%"=="4" (
    exit /b 0
)

echo Ongeldige keuze!

:end
echo.
echo Druk op een toets om af te sluiten...
pause >nul
