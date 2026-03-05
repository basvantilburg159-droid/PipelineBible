#!/bin/bash
# ==================================================
# PipelineBible - SIMPELE LAUNCHER (Mac/Linux)
# Run dit bestand om PipelineBible te starten
# Dit script blijft ALTIJD open!
# ==================================================

clear

echo ""
echo "========================================================"
echo " PipelineBible v1.1 - Pipeline Standards Database"
echo "========================================================"
echo ""
echo " Welkom! Dit script test je PipelineBible installatie."
echo ""
echo "========================================================"
echo ""

# Check Python3
if ! command -v python3 &> /dev/null; then
    echo "[X] FOUT: Python3 is niet gevonden!"
    echo ""
    echo "    Installatie instructies:"
    echo "      - Mac:    brew install python3"
    echo "      - Ubuntu: sudo apt install python3"
    echo "      - Fedora: sudo dnf install python3"
    echo ""
    echo "========================================================"
    read -p "Druk op Enter om af te sluiten..."
    exit 1
fi

echo "[OK] Python gevonden:"
python3 --version
echo ""

# Run de test suite
echo "========================================================"
echo " Test Suite wordt uitgevoerd..."
echo "========================================================"
echo ""

python3 test_pipelinebible.py

echo ""
echo "========================================================"
echo " Script voltooid!"
echo "========================================================"
echo ""
echo " Dit venster blijft open zodat je de output kunt lezen."
echo " Sluit het venster handmatig."
echo ""
read -p "Druk op Enter om af te sluiten..."
