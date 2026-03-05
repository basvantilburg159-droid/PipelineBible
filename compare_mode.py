"""
Pipe Standards Pro v12 - Compare Mode
Side-by-side comparison of two pipes/bends/flanges
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Optional, Tuple

from constants import *
from gui_components import *
from data_models import PipeSpec, BendSpec, FlangeSpec
from visualization_2d import *


class CompareWindow:
    """Window for comparing two pipe components"""
    
    def __init__(self, parent, pipe_db):
        self.window = tk.Toplevel(parent)
        self.window.title("Compare Mode - Pipe Standards Pro v12")
        self.window.geometry("1600x900")
        self.window.configure(bg=BG_PRIMARY)
        
        self.pipe_db = pipe_db
        self.item_type = "Pipes"
        self.standard = "ASME"
        
        self.item_a: Optional[PipeSpec] = None
        self.item_b: Optional[PipeSpec] = None
        
        self._build_ui()
    
    def _build_ui(self):
        """Build comparison UI"""
        # Header
        header = ttk.Frame(self.window)
        header.pack(fill='x', padx=PADDING_LARGE, pady=PADDING_LARGE)
        
        title = ttk.Label(header, text="Compare Mode",
                         style='Header.TLabel')
        title.pack(side='left')
        
        # Type selector
        type_frame = ttk.Frame(header)
        type_frame.pack(side='right')
        
        ttk.Label(type_frame, text="Type:").pack(side='left', padx=(0, 5))
        self.type_var = tk.StringVar(value="Pipes")
        type_combo = ttk.Combobox(type_frame, textvariable=self.type_var,
                                  values=["Pipes", "Bends", "Flanges"],
                                  state='readonly', width=10)
        type_combo.pack(side='left', padx=5)
        
        ttk.Label(type_frame, text="Standard:").pack(side='left', padx=(20, 5))
        self.standard_var = tk.StringVar(value="ASME")
        standard_combo = ttk.Combobox(type_frame, textvariable=self.standard_var,
                                     values=["ASME", "DIN"],
                                     state='readonly', width=8)
        standard_combo.pack(side='left')
        
        # Main content
        content = ttk.Frame(self.window)
        content.pack(fill='both', expand=True, padx=PADDING_LARGE)
        
        # Left panel (Item A)
        left_panel = CardFrame(content, "Item A")
        left_panel.pack(side='left', fill='both', expand=True, 
                       padx=(0, PADDING_SMALL))
        
        self.selector_a = self._create_selector(left_panel, 'A')
        self.viz_a = self._create_visualization(left_panel)
        self.info_a = self._create_info_box(left_panel)
        
        # Right panel (Item B)
        right_panel = CardFrame(content, "Item B")
        right_panel.pack(side='right', fill='both', expand=True,
                        padx=(PADDING_SMALL, 0))
        
        self.selector_b = self._create_selector(right_panel, 'B')
        self.viz_b = self._create_visualization(right_panel)
        self.info_b = self._create_info_box(right_panel)
        
        # Comparison summary at bottom
        self.summary_frame = CardFrame(self.window, "Comparison Summary")
        self.summary_frame.pack(fill='x', padx=PADDING_LARGE, pady=PADDING_MEDIUM)
        
        self.summary_text = tk.Text(self.summary_frame, height=6,
                                    bg=BG_TERTIARY, fg=TEXT_PRIMARY,
                                    font=(FONT_FAMILY, FONT_SIZE_NORMAL),
                                    relief='flat', padx=PADDING_MEDIUM,
                                    pady=PADDING_MEDIUM)
        self.summary_text.pack(fill='both', expand=True)
    
    def _create_selector(self, parent, side: str):
        """Create item selector dropdown"""
        frame = ttk.Frame(parent)
        frame.pack(fill='x', pady=(0, PADDING_MEDIUM))
        
        ttk.Label(frame, text="Select:").pack(side='left', padx=(0, 5))
        
        var = tk.StringVar()
        combo = ttk.Combobox(frame, textvariable=var, state='readonly',
                            width=30)
        combo.pack(side='left', fill='x', expand=True)
        
        # Bind selection
        combo.bind('<<ComboboxSelected>>',
                  lambda e: self._on_select(side, var.get()))
        
        # Store for later access
        setattr(self, f'combo_{side.lower()}', combo)
        setattr(self, f'var_{side.lower()}', var)
        
        return frame
    
    def _create_visualization(self, parent):
        """Create matplotlib canvas"""
        viz_frame = ttk.Frame(parent)
        viz_frame.pack(fill='both', expand=True, pady=(0, PADDING_MEDIUM))
        
        figure = Figure(figsize=(6, 5), dpi=80)
        canvas = FigureCanvasTkAgg(figure, viz_frame)
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        return {'figure': figure, 'canvas': canvas}
    
    def _create_info_box(self, parent):
        """Create info text box"""
        text = tk.Text(parent, height=8,
                      bg=BG_TERTIARY, fg=TEXT_PRIMARY,
                      font=(FONT_FAMILY, FONT_SIZE_SMALL),
                      relief='flat', padx=PADDING_MEDIUM,
                      pady=PADDING_MEDIUM)
        text.pack(fill='x')
        return text
    
    def _on_select(self, side: str, value: str):
        """Handle item selection"""
        # Parse selection and create spec
        # For now, just show info
        if side == 'A':
            self.info_a.delete('1.0', 'end')
            self.info_a.insert('1.0', f"Selected: {value}")
        else:
            self.info_b.delete('1.0', 'end')
            self.info_b.insert('1.0', f"Selected: {value}")
        
        # Update comparison
        self._update_comparison()
    
    def _update_comparison(self):
        """Update comparison summary"""
        if self.item_a and self.item_b:
            # Calculate differences
            summary = "=== Comparison Summary ===\n\n"
            summary += f"Item A: {self.item_a.nps_or_dn}\n"
            summary += f"Item B: {self.item_b.nps_or_dn}\n"
            
            self.summary_text.delete('1.0', 'end')
            self.summary_text.insert('1.0', summary)
