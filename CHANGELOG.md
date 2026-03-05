# Changelog

All notable changes to Pipe Standards Pro will be documented in this file.

## [12.0] - 2026-03-05

### 🎨 Added - Modern GUI
- Complete dark theme implementation with professional color scheme
  - Primary background: `#1a1b2e`
  - Accent colors: `#00d4aa` (cyan), `#f5c211` (gold)
- Card-based layout with clean spacing
- Custom styled widgets (buttons, entries, tables)
- Smooth visual transitions

### 📐 Added - Multiple Visualization Modes
- **2D Cross-Section Views**
  - Pipe cross-sections with wall thickness visualization
  - Bend drawings with center-line radius
  - Flange face views with bolt patterns
  - Professional dimension annotations
  
- **Isometric Views (30° Projection)**
  - Pipe isometric with visible depth
  - Bend isometric showing curved geometry
  - Flange isometric with thickness detail
  - Hidden line removal
  
- **3D Interactive Views**
  - Rotatable pipe with cutaway view
  - 3D bend with torus geometry
  - 3D flange with bolt holes
  - Interactive camera controls

### 🔧 Added - Comprehensive Standards Support
- **ASME B36.10 Pipes**
  - NPS 1/8" to 36"
  - Schedules: 5S, 10S, STD, XS, XXS, 20-160
  - 159 total pipe×schedule combinations
  
- **DIN EN 10220 Pipes**
  - DN 6 to 600 mm
  - Various wall thicknesses (1.0-12.5 mm)
  - 151 total pipe×thickness combinations
  
- **Bend Data**
  - 90° elbows for 26 standard sizes
  - Long Radius (LR) and Short Radius (SR)
  
- **Flange Data**
  - ASME B16.5: Class 150, 300, 600
  - DIN EN 1092-1: PN 10, 16, 40
  - Complete bolt pattern specifications

### 📊 Added - Flow Calculator
- Velocity calculations from flow rate and diameter
- Reynolds number determination
- Flow regime identification (Laminar/Transitional/Turbulent)
- Pressure drop using Darcy-Weisbach equation
- Friction factor with Swamee-Jain approximation
- Visual flow diagram with velocity profile

### 💾 Added - Export Functionality
- PNG export (high resolution, 300 DPI)
- PDF export (vector format)
- SVG export (scalable)
- Keyboard shortcut `Ctrl+E`

### 🔍 Added - Search & Navigation
- Live search with real-time filtering
- Tab-based navigation (Pipes/Bochten/Flenzen/Flow)
- Keyboard shortcuts for all tabs (`Ctrl+1/2/3/4`)
- Status bar with context information
- Recent items tracking

### ⚙️ Added - User Experience
- View mode selector toggle (2D/ISO/3D)
- Styled data tables with alternating rows
- Loading indicators
- Tooltips
- Error handling with user-friendly messages

### 🏗️ Added - Code Architecture
- Modular structure with separate files:
  - `constants.py`: Data and configuration
  - `data_models.py`: Classes and calculations
  - `gui_components.py`: Reusable UI widgets
  - `visualization_2d.py`: 2D renderers
  - `visualization_iso.py`: Isometric renderers
  - `visualization_3d.py`: 3D renderers
  - `utils.py`: Helper functions
  - `pipe_standards_v12.py`: Main application
- Type hints for better code quality
- Comprehensive documentation

### 📚 Added - Documentation
- Complete README.md with features and usage
- Detailed USER_GUIDE.md with examples
- Inline code comments
- Requirements.txt for dependencies
- Run script for easy startup

### 🔄 Changed - From v11
- Complete GUI redesign (dark theme)
- Replaced basic 2D drawings with multi-mode visualizations
- Enhanced data models with calculated properties
- Improved navigation with tab buttons
- Better organization with modular architecture

## [11.x] - Previous Version (Historical)

### Features
- Basic tkinter GUI
- 2D pipe cross-sections
- ASME and DIN data
- Simple bend and flange drawings
- Basic flow calculations

---

## Future Roadmap

### v12.1 - Planned
- [ ] Compare mode full implementation
- [ ] Favorites system with persistence
- [ ] Recent items with quick access
- [ ] Additional keyboard shortcuts
- [ ] Customizable themes

### v12.2 - Planned
- [ ] Unit conversion (mm ↔ inch)
- [ ] Material properties database
- [ ] Pipe weight calculations
- [ ] Assembly mode
- [ ] Custom pipe specifications

### v12.3 - Planned
- [ ] PDF report generation
- [ ] Batch export
- [ ] Database export (CSV/Excel)
- [ ] Pressure rating calculations
- [ ] Temperature derating

### v13.0 - Future
- [ ] Web version
- [ ] Mobile app
- [ ] Cloud sync
- [ ] Collaboration features
- [ ] API for integration

---

**Format**: [Major.Minor.Patch]
- **Major**: Breaking changes, complete redesign
- **Minor**: New features, backwards compatible
- **Patch**: Bug fixes, minor improvements
