# PipelineBible v1.1

**Professional Pipeline & Piping Standards Tool**

## Overview

PipelineBible is a comprehensive engineering tool providing industry-standard piping and pipeline data for mechanical and pipeline engineers.

## Features

### Pipe Standards
- **ASME B36.10M** - NPS 1/2" to 56" (full schedule range)
- **DIN EN 10220 / ISO 4200** - DN15 to DN600

### Flange Standards
- **ASME B16.5** - Class 150, 300, 600, 900, 1500
- **ASME B16.47 Series A & B** - Large diameter flanges (NPS 26"-56")
- **DIN EN 1092-1** - PN 10, 16, 25, 40

### Calculations
- Pipe dimensions (OD, ID, wall thickness, weight/meter)
- Bend calculations (1D to 10D radius)
- Flange bolt length calculations
- Gasket specifications (Spiral Wound, RTJ, Kammprofile, etc.)
- ASME & DIN bolt/stud specifications

### Unit Support
- Full metric (mm) and imperial (inch) unit support
- Automatic unit conversion throughout

## Data Coverage

- **40+ pipe OD sizes** from NPS 1/8" to NPS 56"
- **15+ schedule types** (5S, 10S, 20, 30, STD, XS, XXS, etc.)
- **250+ flange configurations**
- **6 bend radius types**
- **Multiple gasket types** for all pressure classes

## Technical Specifications

- ASME standards for North American markets
- DIN/EN standards for European/international markets
- Material calculations based on carbon steel (density 7850 kg/m³)
- Comprehensive bolt length calculations including thread protrusion

## Usage (v1.1)

### Basic Pipe Lookup

```python
from PipelineBible import PipeLookup

# Get pipe dimensions
dims = PipeLookup.get_pipe_dimension('6', 'STD', 'ASME')
print(f"OD: {dims['od']} mm")
print(f"WT: {dims['wt']} mm")
print(f"ID: {dims['id']} mm")
print(f"Weight: {dims['kg']} kg/m")

# List available schedules
schedules = PipeLookup.list_schedules('6', 'ASME')
print(schedules)  # ['5S', '10S', '40/STD', '80/XS', ...]

# Validate pipe size
exists = PipeLookup.validate_nps('6', 'ASME')
```

### Flange Lookup

```python
from PipelineBible import FlangeLookup

# Get flange data
flange = FlangeLookup.get_flange_data('6', 150, 'ASME')
print(f"Flange OD: {flange['flange_od']} mm")
print(f"Bolt Circle: {flange['bolt_circle']} mm")
print(f"Bolt Holes: {flange['bolt_holes']}")
print(f"Series: {flange['series']}")  # B16.5 or B16.47 A/B

# List available classes
classes = FlangeLookup.list_classes('6', 'ASME')
print(classes)  # [150, 300, 600, 900, 1500]
```

### Pretty Printing

```python
from PipelineBible import PrettyPrint

# Print formatted pipe info
PrettyPrint.print_pipe('6', 'STD', 'ASME')

# Print formatted flange info
PrettyPrint.print_flange('6', 150, 'ASME')

# List all available pipe sizes
PrettyPrint.list_all_pipes('ASME')
```

### Data Export

```python
from PipelineBible import DataExport

# Export pipes to CSV
DataExport.export_pipes_csv('asme_pipes.csv', 'ASME')

# Export flanges to CSV
DataExport.export_flanges_csv('asme_flanges.csv', 'ASME')

# Export all data to JSON
DataExport.export_to_json('pipelinebible_asme.json', 'ASME')
```

### Direct Data Access

```python
from PipelineBible import ASME_PIPES, DIN_PIPES, ASME_FL, DIN_FL

# Access raw pipe data
for nps, od, schedules in ASME_PIPES:
    print(f"{nps}: OD={od} mm")
    for sch_name, wt in schedules:
        print(f"  {sch_name}: WT={wt} mm")
```

## Version History

### v1.1 (2026-03-05)
**New Features:**
- 🆕 `PipeLookup` class for simplified pipe data access
- 🆕 `FlangeLookup` class for flange data queries
- 🆕 `DataExport` utilities (CSV and JSON export)
- 🆕 `PrettyPrint` console formatters
- ✨ Enhanced validation functions
- ✨ Helper methods for listing available sizes/schedules/classes
- 📚 Comprehensive usage examples in README

**Improvements:**
- Better error handling
- More intuitive API
- Easier data access patterns

### v1.0 (2026-03-05)
- Initial release
- Complete ASME B36.10M pipe database
- Complete DIN EN 10220 pipe database  
- ASME B16.5 flange data (Class 150-1500)
- ASME B16.47 Series A/B large diameter flanges
- DIN EN 1092-1 flange data
- Bend, gasket, and bolt calculations

## License

Professional engineering tool for educational and commercial use.

## Author

Engineering standards database compiled and maintained by pipeline engineering specialists.