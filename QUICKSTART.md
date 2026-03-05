# PipelineBible - Snelle Referentie

## Installatie
```bash
git clone https://github.com/basvantilburg159-droid/PipelineBible.git
cd PipelineBible
```

## Testen
```bash
# Volledige test suite
python3 test_pipelinebible.py

# Snelle demo
python3 PipelineBible.py
```

## Veelgebruikte Functies

### 1. Pipe Dimensies Opzoeken
```python
from PipelineBible import PipeLookup

# Zoek pipe dimensies
dims = PipeLookup.get_pipe_dimension('6', 'STD', 'ASME')
print(f"OD: {dims['od']} mm")
print(f"WT: {dims['wt']} mm")
print(f"ID: {dims['id']} mm")
print(f"Gewicht: {dims['kg']} kg/m")

# Lijst beschikbare schedules
schedules = PipeLookup.list_schedules('6', 'ASME')
print(schedules)  # ['5S', '10S', '40/STD', '80/XS', '120', '160']

# Check of size bestaat
exists = PipeLookup.validate_nps('24', 'ASME')  # True/False
```

### 2. Flens Informatie
```python
from PipelineBible import FlangeLookup

# Zoek flens data
flange = FlangeLookup.get_flange_data('6', 150, 'ASME')
print(f"Flange OD: {flange['flange_od']} mm")
print(f"Bolt Circle: {flange['bolt_circle']} mm")
print(f"Bouten: {flange['bolt_holes']} x {flange['bolt_size']}\"")
print(f"Serie: {flange['series']}")  # B16.5 of B16.47 A/B

# Lijst beschikbare classes
classes = FlangeLookup.list_classes('6', 'ASME')
print(classes)  # [150, 300, 600, 900, 1500]
```

### 3. Mooie Console Output
```python
from PipelineBible import PrettyPrint

# Print formatted pipe info
PrettyPrint.print_pipe('8', '40', 'ASME')

# Print formatted flange info
PrettyPrint.print_flange('8', 150, 'ASME')

# Lijst alle beschikbare pipes
PrettyPrint.list_all_pipes('ASME', max_display=20)
```

### 4. Data Exporteren
```python
from PipelineBible import DataExport

# Export naar CSV
DataExport.export_pipes_csv('mijn_pipes.csv', 'ASME')
DataExport.export_flanges_csv('mijn_flanges.csv', 'ASME')

# Export naar JSON
DataExport.export_to_json('mijn_data.json', 'ASME')
```

### 5. Berekeningen
```python
from PipelineBible import cdm, cbn, bolt_len

# Pipe dimensies berekenen
dims = cdm(od=219.1, wt=8.18)
print(f"ID: {dims['id']} mm, Gewicht: {dims['kg']} kg/m")

# Bend berekeningen (OD, WT, multiplier, angle)
bend = cbn(219.1, 8.18, 1.5, 90)  # 8" 90° 1.5D bend
print(f"Radius: {bend['R']} mm")
print(f"Tangent: {bend['T']} mm")
print(f"Arc length: {bend['ac']} mm")

# Bolt length berekenen
length = bolt_len(th=25.4, bd="3/4", gt=4.5, wr=False, ft="WN", std="ASME")
print(f"Bolt length: {length} mm")
```

### 6. Directe Database Toegang
```python
from PipelineBible import ASME_PIPES, DIN_PIPES, ASME_FL, DIN_FL

# Loop door alle ASME pipes
for nps, od, schedules in ASME_PIPES:
    print(f"{nps}: OD={od} mm")
    for sch_name, wt in schedules:
        if wt:  # Skip None values
            print(f"  {sch_name}: WT={wt} mm")

# Loop door alle flanges
for nps, cls, fod, thk, bc, nb, bs, rfo, bore in ASME_FL:
    print(f"{nps}\" Class {cls}: {nb} x {bs}\" bolts")
```

## Ondersteunde Standards

### ASME (Amerikaanse/Internationale)
- **Pipes**: NPS 1/8" tot 56" (B36.10M)
- **Schedules**: 5S, 10S, 20, 30, 40, STD, 60, 80, XS, 100, 120, 140, 160, XXS
- **Flanges**: Class 150, 300, 600, 900, 1500 (B16.5)
- **Grote Flanges**: NPS 26"-56" Serie A/B (B16.47)

### DIN (Europese)
- **Pipes**: DN15 tot DN600 (EN 10220)
- **Wanddiktes**: 1.5mm tot 14.2mm (afhankelijk van DN)
- **Flanges**: PN 10, 16, 25, 40 (EN 1092-1)

## Veel Gebruikte Sizes

### ASME Populair
```python
# Kleine sizes
PipeLookup.get_pipe_dimension('1', 'STD', 'ASME')
PipeLookup.get_pipe_dimension('2', '40', 'ASME')
PipeLookup.get_pipe_dimension('4', 'STD', 'ASME')

# Medium sizes
PipeLookup.get_pipe_dimension('6', 'STD', 'ASME')
PipeLookup.get_pipe_dimension('8', '40', 'ASME')
PipeLookup.get_pipe_dimension('10', 'STD', 'ASME')

# Grote sizes
PipeLookup.get_pipe_dimension('24', 'STD', 'ASME')
PipeLookup.get_pipe_dimension('36', '40', 'ASME')
```

### DIN Populair
```python
PipeLookup.get_pipe_dimension('DN50', '2.9', 'DIN')
PipeLookup.get_pipe_dimension('DN100', '3.6', 'DIN')
PipeLookup.get_pipe_dimension('DN200', '6.3', 'DIN')
```

## Tips & Tricks

### Schedule Namen
Schedule namen zijn flexibel:
- `'STD'` vindt `'40/STD'`
- `'XS'` vindt `'80/XS'`
- `'40'` vindt `'40/STD'` of gewoon `'40'`

### Flens Series Herkennen
```python
flange = FlangeLookup.get_flange_data('36', 150, 'ASME')
print(flange['series'])  # 'A' of 'B' voor B16.47, anders 'B16.5'
```

### Error Handling
```python
dims = PipeLookup.get_pipe_dimension('999', 'STD', 'ASME')
if dims is None:
    print("Pipe niet gevonden!")
else:
    print(f"OD: {dims['od']} mm")
```

### Export voor Excel
```python
# Export naar CSV, open in Excel
DataExport.export_pipes_csv('voor_excel.csv', 'ASME')
# Open voor_excel.csv in Excel
```

## Hulp Nodig?

1. **Test script runnen**: `python3 test_pipelinebible.py`
2. **Demo bekijken**: `python3 PipelineBible.py`
3. **README lezen**: Zie hoofdmap voor volledige documentatie
4. **Code bekijken**: Alle functies hebben docstrings

## Voorbeelden

### Complete Pipeline Assembly
```python
from PipelineBible import PipeLookup, FlangeLookup, bolt_len

# 1. Kies pipe
pipe = PipeLookup.get_pipe_dimension('6', 'STD', 'ASME')
print(f"Pipe: {pipe['od']} x {pipe['wt']} mm, {pipe['kg']} kg/m")

# 2. Kies matching flens
flange = FlangeLookup.get_flange_data('6', 150, 'ASME')
print(f"Flange: OD={flange['flange_od']}mm, BC={flange['bolt_circle']}mm")

# 3. Bereken bolt length (gasket 4.5mm spiral wound)
bolts = bolt_len(
    th=flange['thickness'],
    bd=flange['bolt_size'],
    gt=4.5,
    wr=False,
    ft='WN',
    std='ASME'
)
print(f"Bouten: {flange['bolt_holes']} x {flange['bolt_size']}\" x {bolts}mm lang")
```

### Materiaal Takeoff
```python
from PipelineBible import PipeLookup

# Bereken totaal gewicht
sizes = [
    ('6', 'STD', 100),   # 100m
    ('8', '40', 50),     # 50m
    ('12', 'STD', 25),   # 25m
]

totaal = 0
for nps, sch, meters in sizes:
    dims = PipeLookup.get_pipe_dimension(nps, sch, 'ASME')
    gewicht = dims['kg'] * meters
    totaal += gewicht
    print(f"NPS {nps} {sch}: {meters}m x {dims['kg']} kg/m = {gewicht:.1f} kg")

print(f"\nTotaal gewicht: {totaal:.1f} kg")
```
