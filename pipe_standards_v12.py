"""
Pipe Standards Pro v12 - Main Application
Modern GUI for pipe standards with 2D/ISO/3D visualizations
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import json
from typing import Optional, Dict, List

# Import local modules
from constants import *
from gui_components import *
from data_models import *
from visualization_2d import *
from visualization_iso import *
from visualization_3d import *


class PipeStandardsApp:
    """Main application class"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BG_PRIMARY)
        
        # Configure dark theme
        DarkTheme.configure_style()
        
        # Initialize data
        self.pipe_db = PipeDatabase(ASME_PIPES, DIN_PIPES)
        self.current_view_mode = VIEW_MODE_2D
        self.current_standard = "ASME"
        self.current_tab = "Pipes"
        
        # Selection state
        self.selected_pipe: Optional[PipeSpec] = None
        self.selected_bend: Optional[BendSpec] = None
        self.selected_flange: Optional[FlangeSpec] = None
        
        # Favorites and recent (simple lists for now)
        self.favorites: List[Dict] = []
        self.recent: List[Dict] = []
        
        # Build UI
        self._build_ui()
        
        # Keyboard shortcuts
        self._setup_shortcuts()
        
        # Load initial data
        self._load_initial_data()
    
    def _build_ui(self):
        """Build the main UI structure"""
        # Header
        self._build_header()
        
        # Main content area
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(fill='both', expand=True, padx=PADDING_LARGE, pady=PADDING_MEDIUM)
        
        # Tab navigation
        self._build_tab_navigation()
        
        # Content area (left: data, right: visualization)
        self.main_content = ttk.Frame(self.content_frame)
        self.main_content.pack(fill='both', expand=True, pady=PADDING_MEDIUM)
        
        # Left panel (40% width)
        self.left_panel = CardFrame(self.main_content)
        self.left_panel.pack(side='left', fill='both', expand=False, 
                            ipadx=PADDING_LARGE, ipady=PADDING_LARGE)
        self.left_panel.configure(width=int(WINDOW_WIDTH * 0.4))
        
        # Right panel (60% width)
        self.right_panel = CardFrame(self.main_content)
        self.right_panel.pack(side='right', fill='both', expand=True, 
                             padx=(PADDING_MEDIUM, 0))
        
        # Build panels
        self._build_left_panel()
        self._build_right_panel()
        
        # Status bar
        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(side='bottom', fill='x')
        self.status_bar.set_status("Ready")
    
    def _build_header(self):
        """Build application header"""
        header = ttk.Frame(self.root)
        header.pack(fill='x', padx=PADDING_LARGE, pady=PADDING_LARGE)
        
        # Title
        title_label = ttk.Label(header, text="Pipe Standards Pro",
                               style='Header.TLabel')
        title_label.pack(side='left')
        
        # Subtitle
        subtitle = ttk.Label(header, text="v12 | ASME & DIN Standards",
                            style='Subheader.TLabel')
        subtitle.pack(side='left', padx=(PADDING_MEDIUM, 0))
        
        # Quick actions on the right
        actions_frame = ttk.Frame(header)
        actions_frame.pack(side='right')
        
        export_btn = ttk.Button(actions_frame, text="Export",
                               command=self._export_data)
        export_btn.pack(side='left', padx=PADDING_SMALL)
        
        compare_btn = ttk.Button(actions_frame, text="Compare",
                                command=self._show_compare_mode)
        compare_btn.pack(side='left', padx=PADDING_SMALL)
    
    def _build_tab_navigation(self):
        """Build tab navigation bar"""
        tab_frame = ttk.Frame(self.content_frame)
        tab_frame.pack(fill='x', pady=(0, PADDING_MEDIUM))
        
        tabs = ["Pipes", "Bochten", "Flenzen", "Flow"]
        self.tab_buttons = {}
        
        for tab in tabs:
            btn = tk.Button(tab_frame, text=tab,
                          font=(FONT_FAMILY, FONT_SIZE_NORMAL),
                          relief='flat',
                          bd=0,
                          padx=20,
                          pady=10,
                          command=lambda t=tab: self._switch_tab(t))
            btn.pack(side='left', padx=2)
            self.tab_buttons[tab] = btn
        
        # Standard selector (ASME/DIN)
        standard_frame = ttk.Frame(tab_frame)
        standard_frame.pack(side='right')
        
        ttk.Label(standard_frame, text="Standard:").pack(side='left', padx=(0, 5))
        
        self.standard_var = tk.StringVar(value="ASME")
        standard_combo = ttk.Combobox(standard_frame, textvariable=self.standard_var,
                                     values=["ASME", "DIN"], state='readonly',
                                     width=8)
        standard_combo.pack(side='left')
        standard_combo.bind('<<ComboboxSelected>>', self._on_standard_change)
        
        # Update initial tab
        self._update_tab_buttons()
    
    def _build_left_panel(self):
        """Build left panel with data table and controls"""
        # Search bar
        self.search_bar = SearchBar(self.left_panel, self._on_search,
                                    placeholder="Search pipes...")
        self.search_bar.pack(fill='x', pady=(0, PADDING_MEDIUM))
        
        # Data table container
        table_container = ttk.Frame(self.left_panel)
        table_container.pack(fill='both', expand=True)
        
        # Table will be built based on active tab
        self.data_table: Optional[DataTable] = None
        self.table_container = table_container
    
    def _build_right_panel(self):
        """Build right panel with visualization"""
        # View mode selector
        self.view_selector = ViewModeSelector(self.right_panel, self._on_view_mode_change)
        self.view_selector.pack(fill='x', pady=(0, PADDING_MEDIUM))
        
        # Matplotlib canvas container
        self.viz_container = ttk.Frame(self.right_panel)
        self.viz_container.pack(fill='both', expand=True)
        
        # Create initial figure
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self.viz_container)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Navigation toolbar
        toolbar_frame = ttk.Frame(self.viz_container)
        toolbar_frame.pack(fill='x')
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        
        # Loading indicator
        self.loading = LoadingIndicator(self.viz_container)
    
    def _setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-Key-1>', lambda e: self._switch_tab("Pipes"))
        self.root.bind('<Control-Key-2>', lambda e: self._switch_tab("Bochten"))
        self.root.bind('<Control-Key-3>', lambda e: self._switch_tab("Flenzen"))
        self.root.bind('<Control-Key-4>', lambda e: self._switch_tab("Flow"))
        self.root.bind('<Control-e>', lambda e: self._export_data())
        self.root.bind('<Control-f>', lambda e: self.search_bar.entry.focus())
    
    def _load_initial_data(self):
        """Load initial pipe data"""
        self._switch_tab("Pipes")
    
    # ==================== TAB SWITCHING ====================
    
    def _switch_tab(self, tab_name: str):
        """Switch to a different tab"""
        self.current_tab = tab_name
        self._update_tab_buttons()
        self._rebuild_data_table()
        self._clear_visualization()
        self.status_bar.set_status(f"Viewing {tab_name}")
    
    def _update_tab_buttons(self):
        """Update tab button styles"""
        for tab, btn in self.tab_buttons.items():
            if tab == self.current_tab:
                btn.config(bg=ACCENT_CYAN, fg=BG_PRIMARY,
                          font=(FONT_FAMILY, FONT_SIZE_NORMAL, 'bold'))
            else:
                btn.config(bg=BG_SECONDARY, fg=TEXT_SECONDARY,
                          font=(FONT_FAMILY, FONT_SIZE_NORMAL))
    
    def _on_standard_change(self, event=None):
        """Handle standard change"""
        self.current_standard = self.standard_var.get()
        self._rebuild_data_table()
        self.status_bar.set_status(f"Standard changed to {self.current_standard}")
    
    # ==================== DATA TABLE ====================
    
    def _rebuild_data_table(self):
        """Rebuild data table based on current tab"""
        # Clear existing table
        if self.data_table:
            self.data_table.destroy()
        
        if self.current_tab == "Pipes":
            self._build_pipes_table()
        elif self.current_tab == "Bochten":
            self._build_bends_table()
        elif self.current_tab == "Flenzen":
            self._build_flanges_table()
        elif self.current_tab == "Flow":
            self._build_flow_calculator()
    
    def _build_pipes_table(self):
        """Build pipes data table"""
        columns = [
            ('nps', 'NPS/DN', 80),
            ('od', 'OD', 80),
            ('schedule', 'Schedule', 80),
            ('wt', 'Wall Thickness', 120),
            ('id', 'ID', 80),
        ]
        
        self.data_table = DataTable(self.table_container, columns)
        self.data_table.pack(fill='both', expand=True)
        
        # Populate with data
        sizes = self.pipe_db.get_all_sizes(self.current_standard)
        for size in sizes:
            schedules = self.pipe_db.get_available_schedules(size, self.current_standard)
            for schedule in schedules:
                pipe = self.pipe_db.get_pipe_spec(size, schedule, self.current_standard)
                if pipe:
                    unit = "in" if self.current_standard == "ASME" else "mm"
                    self.data_table.insert_row([
                        size,
                        f"{pipe.od:.3f}",
                        schedule,
                        f"{pipe.wall_thickness:.3f}",
                        f"{pipe.id:.3f}"
                    ])
        
        # Bind selection event
        self.data_table.tree.bind('<<TreeviewSelect>>', self._on_pipe_select)
    
    def _build_bends_table(self):
        """Build bends data table"""
        columns = [
            ('nps', 'NPS/DN', 80),
            ('type', 'Type', 80),
            ('radius', 'Radius', 100),
            ('angle', 'Angle', 80),
        ]
        
        self.data_table = DataTable(self.table_container, columns)
        self.data_table.pack(fill='both', expand=True)
        
        # Populate with bend data
        for size, radii in BENDS.items():
            for radius_type, radius in radii.items():
                unit = "in" if self.current_standard == "ASME" else "mm"
                self.data_table.insert_row([
                    size,
                    radius_type,
                    f"{radius:.2f} {unit}",
                    "90°"
                ])
        
        # Bind selection event
        self.data_table.tree.bind('<<TreeviewSelect>>', self._on_bend_select)
    
    def _build_flanges_table(self):
        """Build flanges data table"""
        columns = [
            ('nps', 'NPS/DN', 80),
            ('class', 'Class/PN', 80),
            ('od', 'OD', 80),
            ('thickness', 'Thickness', 100),
            ('bolts', 'Bolts', 80),
        ]
        
        self.data_table = DataTable(self.table_container, columns)
        self.data_table.pack(fill='both', expand=True)
        
        # Populate with flange data
        data = ASME_FLANGES if self.current_standard == "ASME" else DIN_FLANGES
        for size, classes in data.items():
            for pressure_class, specs in classes.items():
                od, thickness, bcd, num_bolts, bolt_size = specs
                unit = "in" if self.current_standard == "ASME" else "mm"
                self.data_table.insert_row([
                    size,
                    pressure_class,
                    f"{od:.2f} {unit}",
                    f"{thickness:.2f} {unit}",
                    f"{num_bolts}×M{bolt_size:.0f}"
                ])
        
        # Bind selection event
        self.data_table.tree.bind('<<TreeviewSelect>>', self._on_flange_select)
    
    def _build_flow_calculator(self):
        """Build flow calculator interface"""
        # Create form instead of table
        form_frame = CardFrame(self.table_container, "Flow Calculator")
        form_frame.pack(fill='both', expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Input fields
        fields = [
            ("Pipe ID (m):", "pipe_id"),
            ("Flow Rate (m³/s):", "flow_rate"),
            ("Pipe Length (m):", "length"),
            ("Roughness (m):", "roughness"),
        ]
        
        self.flow_entries = {}
        for i, (label_text, field_name) in enumerate(fields):
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, 
                                                        sticky='w', pady=PADDING_SMALL)
            entry = ttk.Entry(form_frame)
            entry.grid(row=i, column=1, sticky='ew', padx=(PADDING_SMALL, 0), 
                      pady=PADDING_SMALL)
            self.flow_entries[field_name] = entry
        
        # Set defaults
        self.flow_entries['pipe_id'].insert(0, "0.1")
        self.flow_entries['flow_rate'].insert(0, "0.01")
        self.flow_entries['length'].insert(0, "100")
        self.flow_entries['roughness'].insert(0, "0.000045")
        
        form_frame.columnconfigure(1, weight=1)
        
        # Calculate button
        calc_btn = ttk.Button(form_frame, text="Calculate", 
                             style='Accent.TButton',
                             command=self._calculate_flow)
        calc_btn.grid(row=len(fields), column=0, columnspan=2, 
                     pady=PADDING_LARGE, sticky='ew')
        
        # Results display
        self.flow_results = tk.Text(form_frame, height=10, 
                                    bg=BG_TERTIARY, fg=TEXT_PRIMARY,
                                    font=(FONT_FAMILY, FONT_SIZE_NORMAL),
                                    relief='flat', padx=PADDING_MEDIUM,
                                    pady=PADDING_MEDIUM)
        self.flow_results.grid(row=len(fields)+1, column=0, columnspan=2, 
                              sticky='nsew', pady=(PADDING_MEDIUM, 0))
        form_frame.rowconfigure(len(fields)+1, weight=1)
    
    # ==================== SELECTION HANDLERS ====================
    
    def _on_pipe_select(self, event=None):
        """Handle pipe selection"""
        selection = self.data_table.get_selection()
        if selection:
            nps, od, schedule, wt, id_val = selection
            self.selected_pipe = self.pipe_db.get_pipe_spec(
                nps, schedule, self.current_standard
            )
            
            if self.selected_pipe:
                self._update_visualization()
                self.status_bar.set_info(f"Pipe: {nps} Sch {schedule}")
                self._add_to_recent("pipe", nps, schedule)
    
    def _on_bend_select(self, event=None):
        """Handle bend selection"""
        selection = self.data_table.get_selection()
        if selection:
            size, radius_type, radius, angle = selection
            
            # Get pipe OD for this size
            if size in ASME_PIPES:
                od, schedules = ASME_PIPES[size]
                # Use STD schedule for wall thickness
                wt = schedules.get('STD', list(schedules.values())[0])
            else:
                od = 1.0  # Default
                wt = 0.1
            
            radius_value = BENDS.get(size, {}).get(radius_type, 0)
            
            self.selected_bend = BendSpec(
                nps_or_dn=size,
                angle=90,
                radius_type=radius_type,
                radius=radius_value,
                od=od,
                wall_thickness=wt,
                standard=self.current_standard
            )
            
            self._update_visualization()
            self.status_bar.set_info(f"Bend: {size} {radius_type}")
    
    def _on_flange_select(self, event=None):
        """Handle flange selection"""
        selection = self.data_table.get_selection()
        if selection:
            size, pressure_class, od, thickness, bolts = selection
            
            # Parse values
            od_val = float(od.split()[0])
            thickness_val = float(thickness.split()[0])
            
            # Get full specs
            data = ASME_FLANGES if self.current_standard == "ASME" else DIN_FLANGES
            specs = data.get(size, {}).get(pressure_class, None)
            
            if specs:
                od, thickness, bcd, num_bolts, bolt_size = specs
                
                self.selected_flange = FlangeSpec(
                    nps_or_dn=size,
                    pressure_class=pressure_class,
                    od=od,
                    thickness=thickness,
                    bolt_circle_dia=bcd,
                    num_bolts=num_bolts,
                    bolt_size=bolt_size,
                    standard=self.current_standard
                )
                
                self._update_visualization()
                self.status_bar.set_info(f"Flange: {size} Class {pressure_class}")
    
    # ==================== VISUALIZATION ====================
    
    def _update_visualization(self):
        """Update visualization based on current selection and view mode"""
        self.figure.clear()
        
        try:
            if self.current_tab == "Pipes" and self.selected_pipe:
                if self.current_view_mode == VIEW_MODE_2D:
                    draw_pipe_cross_section(self.figure, self.selected_pipe)
                elif self.current_view_mode == VIEW_MODE_ISO:
                    draw_pipe_isometric(self.figure, self.selected_pipe)
                elif self.current_view_mode == VIEW_MODE_3D:
                    draw_pipe_3d(self.figure, self.selected_pipe)
            
            elif self.current_tab == "Bochten" and self.selected_bend:
                if self.current_view_mode == VIEW_MODE_2D:
                    draw_bend(self.figure, self.selected_bend)
                elif self.current_view_mode == VIEW_MODE_ISO:
                    draw_bend_isometric(self.figure, self.selected_bend)
                elif self.current_view_mode == VIEW_MODE_3D:
                    draw_bend_3d(self.figure, self.selected_bend)
            
            elif self.current_tab == "Flenzen" and self.selected_flange:
                if self.current_view_mode == VIEW_MODE_2D:
                    draw_flange(self.figure, self.selected_flange)
                elif self.current_view_mode == VIEW_MODE_ISO:
                    draw_flange_isometric(self.figure, self.selected_flange)
                elif self.current_view_mode == VIEW_MODE_3D:
                    draw_flange_3d(self.figure, self.selected_flange)
            
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Visualization Error", f"Error rendering: {str(e)}")
    
    def _clear_visualization(self):
        """Clear the visualization canvas"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, f"Select a {self.current_tab[:-1]} to visualize",
               ha='center', va='center', fontsize=14, color=TEXT_SECONDARY,
               transform=ax.transAxes)
        ax.set_facecolor(BG_SECONDARY)
        ax.axis('off')
        self.canvas.draw()
    
    def _on_view_mode_change(self, mode: str):
        """Handle view mode change"""
        self.current_view_mode = mode
        self._update_visualization()
        self.status_bar.set_status(f"View mode: {mode}")
    
    # ==================== SEARCH & FILTER ====================
    
    def _on_search(self, query: str):
        """Handle search query"""
        if not query or query.strip() == "":
            self._rebuild_data_table()
            return
        
        # Simple search - rebuild table with filtered results
        # (Could be optimized with better filtering)
        self.status_bar.set_status(f"Searching: {query}")
    
    # ==================== FLOW CALCULATOR ====================
    
    def _calculate_flow(self):
        """Calculate flow parameters"""
        try:
            # Get input values
            pipe_id = float(self.flow_entries['pipe_id'].get())
            flow_rate = float(self.flow_entries['flow_rate'].get())
            length = float(self.flow_entries['length'].get())
            roughness = float(self.flow_entries['roughness'].get())
            
            # Calculate parameters
            velocity = calculate_flow_velocity(flow_rate, pipe_id)
            reynolds = calculate_reynolds_number(velocity, pipe_id)
            regime = get_flow_regime(reynolds)
            pressure_drop = calculate_pressure_drop(velocity, pipe_id, length, roughness)
            
            # Display results
            results = f"""
Flow Calculation Results
{'='*40}

Velocity:        {velocity:.3f} m/s
Reynolds Number: {reynolds:.0f}
Flow Regime:     {regime}
Pressure Drop:   {pressure_drop:.2f} Pa ({pressure_drop/1000:.2f} kPa)

Cross-Section Area: {np.pi * (pipe_id/2)**2:.6f} m²
            """
            
            self.flow_results.delete('1.0', 'end')
            self.flow_results.insert('1.0', results)
            
            # Update visualization
            flow_data = {
                'pipe_id': pipe_id,
                'velocity': velocity,
                'reynolds': reynolds,
                'regime': regime
            }
            self.figure.clear()
            draw_flow_diagram(self.figure, flow_data)
            self.canvas.draw()
            
            self.status_bar.set_status("Flow calculated successfully", SUCCESS)
            
        except ValueError as e:
            messagebox.showerror("Input Error", "Please enter valid numbers")
        except Exception as e:
            messagebox.showerror("Calculation Error", f"Error: {str(e)}")
    
    # ==================== EXPORT & UTILITIES ====================
    
    def _export_data(self):
        """Export current view to file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("PDF Document", "*.pdf"),
                ("SVG Vector", "*.svg"),
            ]
        )
        
        if file_path:
            try:
                self.figure.savefig(file_path, dpi=300, bbox_inches='tight',
                                   facecolor=BG_PRIMARY)
                self.status_bar.set_status(f"Exported to {file_path}", SUCCESS)
                messagebox.showinfo("Export Success", f"Saved to: {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
    
    def _show_compare_mode(self):
        """Show comparison mode (placeholder)"""
        messagebox.showinfo("Compare Mode", 
                           "Compare mode coming soon!\n"
                           "This will allow side-by-side comparison of two pipes.")
    
    def _add_to_recent(self, item_type: str, *args):
        """Add item to recent list"""
        recent_item = {"type": item_type, "args": args}
        if recent_item not in self.recent:
            self.recent.insert(0, recent_item)
            self.recent = self.recent[:10]  # Keep last 10


def main():
    """Main entry point"""
    root = tk.Tk()
    app = PipeStandardsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
