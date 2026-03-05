#!/bin/bash
# PipelineBible Launcher voor Mac/Linux
# Dit script houdt de terminal open zodat je de output kunt lezen

clear
echo "============================================================"
echo "PipelineBible v1.1 - Pipeline Standards Tool"
echo "============================================================"
echo ""

# Check of Python geinstalleerd is
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is niet geinstalleerd!"
    echo ""
    echo "Installeer Python3:"
    echo "  - Mac: brew install python3"
    echo "  - Ubuntu/Debian: sudo apt install python3"
    echo "  - Fedora: sudo dnf install python3"
    echo ""
    read -p "Druk op Enter om af te sluiten..."
    exit 1
fi

echo "Python3 gevonden: $(python3 --version)"
echo ""

# Menu
echo "Wat wil je doen?"
echo ""
echo "1. Test PipelineBible (alle functies testen)"
echo "2. Demo (laat functionaliteit zien)"
echo "3. Interactieve Python console"
echo "4. Afsluiten"
echo ""

read -p "Kies optie (1-4): " choice

case $choice in
    1)
        echo ""
        echo "Running test suite..."
        echo ""
        python3 test_pipelinebible.py
        echo ""
        echo "============================================================"
        echo "Tests voltooid!"
        echo "============================================================"
        ;;
    2)
        echo ""
        echo "Running demo..."
        echo ""
        python3 PipelineBible.py
        echo ""
        echo "============================================================"
        echo "Demo voltooid!"
        echo "============================================================"
        ;;
    3)
        echo ""
        echo "Starting Python console..."
        echo "Importeer modules met: from PipelineBible import PipeLookup, FlangeLookup"
        echo ""
        python3 -i -c "from PipelineBible import *; print('PipelineBible modules geladen! Type help(PipeLookup) voor hulp.')"
        ;;
    4)
        exit 0
        ;;
    *)
        echo "Ongeldige keuze!"
        ;;
esac

echo ""
read -p "Druk op Enter om af te sluiten..."
