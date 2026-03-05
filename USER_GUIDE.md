# Pipe Standards Pro v12 - User Guide

## Getting Started

### Installation

1. **Prerequisites**
   - Python 3.8 or higher
   - Tkinter (usually included with Python)

2. **Quick Start**
   ```bash
   # Clone or download the project
   cd PipelineBible
   
   # Run the application (automated setup)
   ./run.sh
   ```

3. **Manual Installation**
   ```bash
   # Create virtual environment
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run application
   python pipe_standards_v12.py
   ```

## Interface Overview

### Main Window Layout

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER: Pipe Standards Pro v12                             │
│          [Export] [Compare]                                 │
├─────────────────────────────────────────────────────────────┤
│  TABS: [Pipes] [Bochten] [Flenzen] [Flow]    Standard: ASME│
├──────────────────────┬──────────────────────────────────────┤
│  DATA TABLE          │  VISUALIZATION PANEL                 │
│  ┌────────────────┐  │  [2D] [ISO] [3D]                    │
│  │ Search: ______ │  │  ┌────────────────────────────────┐ │
│  │                │  │  │                                │ │
│  │ NPS  OD  Sch   │  │  │      Rendered Drawing          │ │
│  │ 2    2.375 STD │  │  │                                │ │
│  │ 2    2.375 XS  │  │  │                                │ │
│  │ ...            │  │  │                                │ │
│  └────────────────┘  │  └────────────────────────────────┘ │
│                      │  [Matplotlib Toolbar]               │
└──────────────────────┴──────────────────────────────────────┤
│  Status: Ready                                              │
└─────────────────────────────────────────────────────────────┘
```

## Features Guide

### 1. Viewing Pipes

**ASME B36.10 Pipes**
- NPS: 1/8" to 36"
- Schedules: 5S, 10S, STD, XS, XXS, 20-160
- Displays: Outer Diameter (OD), Inner Diameter (ID), Wall Thickness (WT)

**DIN EN 10220 Pipes**
- DN: 6 to 600 mm
- Various wall thicknesses
- Metric measurements

**Steps:**
1. Click "Pipes" tab (or press `Ctrl+1`)
2. Select standard (ASME or DIN) from dropdown
3. Use search bar to filter sizes
4. Click on any pipe in the table
5. Switch between view modes:
   - **2D**: Cross-section with dimensions
   - **ISO**: Isometric projection showing 3D form
   - **3D**: Interactive rotatable view

**Visualization Details:**
- **2D Cross-Section**: Shows pipe wall with gradient shading
- **Isometric View**: 30° projection with visible depth
- **3D View**: Cutaway view revealing inner diameter
- All views include dimension annotations

### 2. Viewing Bends (Bochten)

**90° Elbows**
- Standard sizes matching pipe dimensions
- LR (Long Radius): R = 1.5 × NPS
- SR (Short Radius): R = 1.0 × NPS

**Steps:**
1. Click "Bochten" tab (or press `Ctrl+2`)
2. Select a bend from the table
3. View center-line radius and arc length
4. Switch between 2D, ISO, and 3D views

**Visualization Details:**
- Shows bend geometry with tangent lines
- Center-line radius indicated
- Wall thickness visible in 3D cutaway

### 3. Viewing Flanges (Flenzen)

**ASME B16.5 Flanges**
- Classes: 150, 300, 600
- Weld Neck (WN) type
- Includes bolt pattern specifications

**DIN EN 1092-1 Flanges**
- Pressure ratings: PN 10, 16, 40
- Metric dimensions

**Steps:**
1. Click "Flenzen" tab (or press `Ctrl+3`)
2. Select flange size and pressure class
3. View bolt circle diameter, bolt count, and flange thickness
4. Switch between view modes

**Visualization Details:**
- Face view shows bolt holes and patterns
- Raised face highlighted
- 3D view shows thickness and assembled appearance

### 4. Flow Calculator

**Calculates:**
- Flow velocity
- Reynolds number
- Flow regime (Laminar/Transitional/Turbulent)
- Pressure drop using Darcy-Weisbach equation

**Steps:**
1. Click "Flow" tab (or press `Ctrl+4`)
2. Enter parameters:
   - **Pipe ID**: Inner diameter in meters
   - **Flow Rate**: Volumetric flow in m³/s
   - **Pipe Length**: Length in meters
   - **Roughness**: Surface roughness in meters (default: 0.000045 for steel)
3. Click "Calculate"
4. View results and flow visualization

**Example Calculation:**
```
Input:
  Pipe ID: 0.1 m (100 mm)
  Flow Rate: 0.01 m³/s (10 liters/second)
  Length: 100 m
  Roughness: 0.000045 m (steel pipe)

Output:
  Velocity: 1.273 m/s
  Reynolds Number: 126,800
  Flow Regime: Turbulent
  Pressure Drop: 2,456 Pa (2.46 kPa)
```

### 5. Export Functions

**Export Formats:**
- **PNG**: High-resolution raster image (300 DPI)
- **PDF**: Vector format, ideal for reports
- **SVG**: Scalable vector graphics

**Steps:**
1. Navigate to the view you want to export
2. Click "Export" button in header (or press `Ctrl+E`)
3. Choose format and location
4. Save file

**Tips:**
- Use PNG for presentations and documents
- Use PDF for technical reports
- Use SVG for web or further editing

### 6. Search & Filter

**Search Bar:**
- Type to filter pipes by size
- Search works across NPS/DN values
- Results update in real-time

**Examples:**
- Search "2" → Shows all 2", 2-1/2", 20", 22", 24", etc.
- Search "STD" → Would need implementation to filter by schedule
- Search "100" → Shows DN 100 (DIN) or NPS sizes containing "100"

### 7. Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+1` | Switch to Pipes tab |
| `Ctrl+2` | Switch to Bochten tab |
| `Ctrl+3` | Switch to Flenzen tab |
| `Ctrl+4` | Switch to Flow tab |
| `Ctrl+E` | Export current view |
| `Ctrl+F` | Focus search bar |

## Understanding the Visualizations

### 2D Views
- **Purpose**: Technical drawings for documentation
- **Features**: Precise dimensions, clean lines
- **Best for**: Reports, specifications, printing

### Isometric Views
- **Purpose**: 3D representation on 2D plane
- **Features**: 30° projection, shows depth without perspective distortion
- **Best for**: Technical illustrations, assembly drawings

### 3D Views
- **Purpose**: Interactive exploration
- **Features**: Rotate, zoom, pan with mouse
- **Best for**: Understanding geometry, presentations

**Mouse Controls in 3D:**
- **Left-click + Drag**: Rotate view
- **Right-click + Drag**: Pan (move) view
- **Scroll**: Zoom in/out
- **Toolbar buttons**: Home, back, forward, pan, zoom, save

## Data Reference

### ASME Pipe Schedules

| Schedule | Description |
|----------|-------------|
| 5S | Extra light (stainless steel) |
| 10S | Light (stainless steel) |
| STD | Standard wall |
| XS | Extra strong |
| XXS | Double extra strong |
| 20-160 | Numbered schedules (heavier walls) |

### DIN Wall Thickness Series

Wall thicknesses range from 1.0 mm to 12.5 mm depending on DN size. Common series:
- Light: 1.8-2.3 mm
- Medium: 2.9-4.0 mm
- Heavy: 5.0-8.0 mm

### Flange Pressure Ratings

**ASME:**
- Class 150: ~20 bar at 38°C
- Class 300: ~50 bar at 38°C
- Class 600: ~100 bar at 38°C

**DIN:**
- PN 10: 10 bar
- PN 16: 16 bar
- PN 40: 40 bar

## Troubleshooting

### Application Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check for errors
python pipe_standards_v12.py
```

### Import Errors
- Ensure matplotlib and numpy are installed
- Try: `pip install matplotlib numpy`
- On Linux, you may need: `sudo apt-get install python3-tk`

### Display Issues
- If running over SSH, ensure X11 forwarding is enabled
- For headless servers, use Xvfb virtual display
- On macOS, ensure XQuartz is installed

### Performance Issues
- Large 3D renders may be slow on older hardware
- Try 2D or ISO views for faster rendering
- Close other applications to free memory

## Tips & Best Practices

1. **Start with 2D**: For quick lookups, 2D views are fastest
2. **Use ISO for technical docs**: Isometric views combine clarity with 3D information
3. **3D for presentations**: Interactive 3D views are impressive for demonstrations
4. **Export early**: Save visualizations as you work
5. **Search smartly**: Use partial matches to find multiple related sizes
6. **Check units**: Always verify if working in imperial (ASME) or metric (DIN)

## Advanced Usage

### Batch Export
For exporting multiple pipes, use Python scripting:

```python
from pipe_standards_v12 import PipeStandardsApp
from data_models import PipeDatabase
from constants import ASME_PIPES
from visualization_2d import draw_pipe_cross_section
import matplotlib.pyplot as plt

# Export all 2" pipes with different schedules
pipe_db = PipeDatabase(ASME_PIPES, {})
for schedule in ['STD', 'XS', 'XXS']:
    pipe = pipe_db.get_pipe_spec('2', schedule, 'ASME')
    if pipe:
        fig = plt.figure()
        draw_pipe_cross_section(fig, pipe)
        fig.savefig(f'pipe_2in_{schedule}.png', dpi=300)
        plt.close(fig)
```

### Custom Data
To add custom pipe specifications, edit `constants.py`:

```python
ASME_PIPES["custom-1"] = (1.500, {
    "CUSTOM": 0.125
})
```

## Support & Resources

- **Documentation**: README.md in project folder
- **Code**: All source files are commented
- **Standards**: 
  - ASME B36.10: https://www.asme.org/
  - DIN EN 10220: https://www.din.de/

## Version History

**v12.0 (Current)**
- Modern dark theme GUI
- 2D/ISO/3D visualization modes
- ASME & DIN standards support
- Flow calculator
- Export functionality

---

**Last Updated**: March 5, 2026  
**Author**: Pipeline Engineering Team
