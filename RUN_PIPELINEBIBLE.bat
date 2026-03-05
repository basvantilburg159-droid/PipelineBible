@echo off
REM ==================================================
REM PipelineBible - SIMPELE LAUNCHER
REM Dubbelklik dit bestand om PipelineBible te starten
REM Dit script blijft ALTIJD open!
REM ==================================================

title PipelineBible v1.1

REM Kleur en opmaak (als ondersteund)
color 0A

echo.
echo ========================================================
echo  PipelineBible v1.1 - Pipeline Standards Database
echo ========================================================
echo.
echo  Welkom! Dit script test je PipelineBible installatie.
echo.
echo ========================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] FOUT: Python is niet gevonden!
    echo.
    echo     Download Python van: https://www.python.org/downloads/
    echo     Zorg dat je "Add Python to PATH" aanvinkt!
    echo.
    echo ========================================================
    pause
    exit /b 1
)

echo [OK] Python gevonden: 
python --version
echo.

REM Run de test suite
echo ========================================================
echo  Test Suite wordt uitgevoerd...
echo ========================================================
echo.

python test_pipelinebible.py

echo.
echo ========================================================
echo  Script voltooid!
echo ========================================================
echo.
echo  Dit venster blijft open zodat je de output kunt lezen.
echo  Sluit het venster handmatig of druk op een toets.
echo.
pause
