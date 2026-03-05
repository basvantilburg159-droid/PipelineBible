# Pipe Standards Pro v12

Modern desktop application for pipe standards (ASME B36.10 & DIN EN 10220) with 2D/Isometric/3D visualizations.

## Features

### 🎨 Modern Dark Theme GUI
- Professional dark color scheme (`#1a1b2e` background, `#00d4aa` accent)
- Card-based layout with clean typography
- Smooth transitions and visual feedback

### 📐 Multiple Visualization Modes
- **2D Cross-Section**: Technical drawings with dimensions
- **Isometric View**: 30° projection for technical clarity
- **3D Interactive**: Rotatable 3D models with cutaway views

### 🔧 Comprehensive Standards Support
- **ASME B36.10**: NPS 1/8" to 36" with multiple schedules (5S, 10S, STD, XS, XXS, etc.)
- **DIN EN 10220**: DN 6 to 600 with various wall thicknesses
- Complete data for:
  - Pipes (with wall thickness, inner diameter calculations)
  - 90° Elbows/Bends (Long Radius & Short Radius)
  - Flanges (ASME B16.5 Class 150/300/600, DIN PN 10/16/40)

### 📊 Flow Calculator
- Velocity calculations
- Reynolds number determination
- Flow regime identification (Laminar/Turbulent)
- Pressure drop calculations (Darcy-Weisbach equation)

### 💾 Export Capabilities
- PNG images (high resolution)
- PDF documents
- SVG vector graphics

### ⚡ User Experience Features
- Live search and filtering
- Keyboard shortcuts (Ctrl+1/2/3/4 for tabs)
- Status bar with context information
- Recent items tracking

## Installation

### Requirements
```bash
pip install matplotlib numpy tkinter
```

Note: `tkinter` comes pre-installed with most Python distributions.

### Running the Application
```bash
python pipe_standards_v12.py
```

## File Structure

```
PipelineBible/
├── pipe_standards_v12.py     # Main application
├── constants.py               # Color schemes, pipe/bend/flange data
├── data_models.py             # Data structures and calculations
├── gui_components.py          # Reusable UI widgets (dark theme)
├── visualization_2d.py        # 2D cross-section drawings
├── visualization_iso.py       # Isometric projections
├── visualization_3d.py        # 3D matplotlib rendering
├── utils.py                   # Helper functions
└── README.md                  # This file
```

## Usage

### Viewing Pipes
1. Select "Pipes" tab (or press `Ctrl+1`)
2. Choose standard (ASME or DIN)
3. Click on a pipe in the table
4. Switch between 2D/ISO/3D views using the toggle buttons

### Viewing Bends
1. Select "Bochten" tab (or press `Ctrl+2`)
2. Choose a bend from the table
3. View in 2D, isometric, or 3D mode

### Viewing Flanges
1. Select "Flenzen" tab (or press `Ctrl+3`)
2. Choose a flange from the table
3. Visualize bolt patterns and dimensions

### Flow Calculations
1. Select "Flow" tab (or press `Ctrl+4`)
2. Enter:
   - Pipe inner diameter (m)
   - Flow rate (m³/s)
   - Pipe length (m)
   - Roughness factor (m)
3. Click "Calculate"
4. View velocity, Reynolds number, flow regime, and pressure drop

### Exporting
- Click "Export" button in the header
- Choose format: PNG, PDF, or SVG
- Select save location

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+1` | Switch to Pipes tab |
| `Ctrl+2` | Switch to Bochten tab |
| `Ctrl+3` | Switch to Flenzen tab |
| `Ctrl+4` | Switch to Flow tab |
| `Ctrl+E` | Export current view |
| `Ctrl+F` | Focus search bar |

## Technical Details

### Pipe Data
- **ASME B36.10**: 33 nominal pipe sizes with 159 schedule variations
- **DIN EN 10220**: 23 DN sizes with 151 wall thickness options

### Bend Data
- 90° elbows for standard sizes
- Long Radius (LR) and Short Radius (SR) types
- Center-line radius calculations

### Flange Data
- **ASME B16.5**: Class 150, 300, 600 (selected sizes)
- **DIN EN 1092-1**: PN 10, 16, 40 (selected sizes)
- Bolt circle diameter, bolt count, and bolt size specifications

### Visualization Technology
- **2D**: Matplotlib patches (Circle, Rectangle, Polygon)
- **Isometric**: 30° rotation matrix transformation
- **3D**: mplot3d with surface meshes and Poly3DCollection

### Calculations
- Inner diameter: `ID = OD - 2×WT`
- Cross-sectional area: `A = π × (ID/2)²`
- Flow velocity: `v = Q / A`
- Reynolds number: `Re = (v × D) / ν`
- Darcy-Weisbach pressure drop: `ΔP = f × (L/D) × (ρv²/2)`

## Color Scheme

| Element | Color | Hex Code |
|---------|-------|----------|
| Background Primary | Dark Navy | `#1a1b2e` |
| Background Secondary | Card | `#252640` |
| Accent Primary | Turquoise | `#00d4aa` |
| Accent Secondary | Gold | `#f5c211` |
| Steel | Blue-Gray | `#8090a8` |
| Text Primary | Light Gray | `#e8eaed` |
| Text Secondary | Medium Gray | `#a8aeb8` |

## Future Enhancements

- [ ] Compare mode (side-by-side comparison)
- [ ] Favorites system with persistent storage
- [ ] Unit conversion (metric ↔ imperial)
- [ ] Custom pipe specifications
- [ ] Assembly mode (combine pipes, bends, flanges)
- [ ] PDF report generation with multiple views
- [ ] Material properties database
- [ ] Pressure rating calculations

## License

This project is for educational and professional use in pipe standards reference.

## Credits

Developed for pipeline engineering professionals requiring quick access to pipe standards and visualizations.

---

**Version**: 12.0  
**Last Updated**: March 5, 2026
