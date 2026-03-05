# PipelineBible - Installatie & Gebruik Instructies

## 🔧 Installatie

### Optie 1: Eenvoudig (met launcher scripts)

#### Windows
1. Download of clone de repository
2. Dubbelklik op **`start_windows.bat`**
3. Kies optie uit het menu

#### Mac / Linux
1. Download of clone de repository
2. Open terminal in de PipelineBible map
3. Run: `bash start.sh` of `./start.sh`
4. Kies optie uit het menu

#### GUI Interface (alle platforms)
1. Run: `python3 gui_launcher.py`
2. GUI blijft open - gebruik tabs voor lookup
3. Sluit venster om af te sluiten

### Optie 2: Command Line (voor gevorderden)

```bash
# Clone repository
git clone https://github.com/basvantilburg159-droid/PipelineBible.git
cd PipelineBible

# Test alles
python3 test_pipelinebible.py

# Demo
python3 PipelineBible.py

# Interactief
python3
>>> from PipelineBible import PipeLookup
```

## ❓ Problemen Oplossen

### Probleem: Script sluit direct af (Windows)

**Oplossing 1: Gebruik de launcher**
- Dubbelklik op `start_windows.bat` in plaats van het Python bestand
- De launcher houdt de console open

**Oplossing 2: Run via Command Prompt**
1. Open Command Prompt (cmd)
2. Navigeer naar de map: `cd pad\naar\PipelineBible`
3. Run: `python test_pipelinebible.py`

**Oplossing 3: Gebruik GUI**
- Run: `python gui_launcher.py`
- GUI blijft open totdat je het sluit

### Probleem: "Python is niet gevonden"

**Windows:**
1. Download Python van https://www.python.org/downloads/
2. **Belangrijk**: Vink "Add Python to PATH" aan tijdens installatie!
3. Herstart computer na installatie
4. Test: open cmd en type `python --version`

**Mac:**
```bash
# Installeer via Homebrew
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3
```

### Probleem: "tkinter niet gevonden" (voor GUI)

**Windows:**
- Tkinter is normaal geïnstalleerd met Python
- Herinstalleer Python en vink alle opties aan

**Mac:**
```bash
brew install python-tk
```

**Linux:**
```bash
sudo apt install python3-tk
```

### Probleem: Script geeft errors

**Check Python versie:**
```bash
python --version  # of python3 --version
```
Minimaal Python 3.7 vereist

**Check modules:**
```python
python3 -c "import csv, json, math; print('Basis modules OK')"
```

## 📦 Verschillende Manieren om te Gebruiken

### 1. Launcher Scripts (Gemakkelijkst)
- **Windows**: Dubbelklik `start_windows.bat`
- **Mac/Linux**: Run `bash start.sh`
- Menu verschijnt met opties

### 2. GUI Interface
```bash
python3 gui_launcher.py
```
- Grafische interface
- Blijft open
- Tabs voor pipe en flange lookup
- Output venster onderaan

### 3. Test Script
```bash
python3 test_pipelinebible.py
```
- Test alle functionaliteit
- Toont of alles werkt
- Geschikt voor eerste test

### 4. Demo Script
```bash
python3 PipelineBible.py
```
- Toont wat mogelijk is
- Voorbeelden van queries
- Sluit af aan het einde

### 5. Interactieve Python
```bash
python3
```
```python
from PipelineBible import PipeLookup, FlangeLookup

# Zoek pipe
dims = PipeLookup.get_pipe_dimension('6', 'STD', 'ASME')
print(dims)

# Zoek flens
flange = FlangeLookup.get_flange_data('6', 150, 'ASME')
print(flange)
```

### 6. In je Eigen Script
```python
# jouw_script.py
from PipelineBible import PipeLookup

def mijn_functie():
    pipe = PipeLookup.get_pipe_dimension('8', '40', 'ASME')
    gewicht = pipe['kg'] * 100  # 100 meter
    print(f"Totaal gewicht: {gewicht} kg")

if __name__ == "__main__":
    mijn_functie()
    input("Druk op Enter om af te sluiten...")  # Houdt open!
```

## 🎯 Snelste Start (voor ongeduldig)

### Windows Power Users
```cmd
git clone https://github.com/basvantilburg159-droid/PipelineBible.git && cd PipelineBible && start_windows.bat
```

### Mac/Linux Power Users
```bash
git clone https://github.com/basvantilburg159-droid/PipelineBible.git && cd PipelineBible && bash start.sh
```

## 💡 Tips

### Script blijft open houden
Voeg aan einde van je script toe:
```python
input("Druk op Enter om af te sluiten...")
```

### GUI vs Command Line
- **GUI** (`gui_launcher.py`): Voor visueel werken, blijft open
- **Command Line**: Voor scripts, automatisering, batch processing

### Debuggen
Als iets niet werkt, run met `-v` flag:
```bash
python3 -v PipelineBible.py
```

Om errors te zien:
```python
try:
    from PipelineBible import PipeLookup
    result = PipeLookup.get_pipe_dimension('6', 'STD', 'ASME')
    print(result)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    input("Druk op Enter...")
```

## 📚 Volgende Stappen

Na installatie:
1. ✅ Run `test_pipelinebible.py` om te testen
2. 📖 Lees `QUICKSTART.md` voor voorbeelden
3. 📘 Lees `README.md` voor volledige documentatie
4. 🎨 Probeer `gui_launcher.py` voor visuele interface

## 🆘 Hulp Nodig?

Als niets werkt:
1. Check Python versie: `python --version` (min. 3.7)
2. Check Python PATH: `where python` (Windows) of `which python3` (Mac/Linux)
3. Herstart terminal/command prompt
4. Herstart computer (na Python installatie)
5. Gebruik launcher scripts - die detecteren problemen

## ✅ Test Checklist

- [ ] Python geïnstalleerd (versie 3.7+)
- [ ] Repository gedownload
- [ ] `test_pipelinebible.py` succesvol
- [ ] Launcher werkt (`start_windows.bat` of `start.sh`)
- [ ] GUI werkt (optioneel, vereist tkinter)
- [ ] Documentatie gelezen

Alles ✓? Dan ben je klaar om PipelineBible te gebruiken! 🚀
