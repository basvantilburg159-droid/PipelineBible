"""
Pipe Standards Pro v12 - GUI Components
Reusable dark-themed UI widgets and components
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Optional
from constants import *


class DarkTheme:
    """Apply dark theme to tkinter widgets"""
    
    @staticmethod
    def configure_style():
        """Configure ttk styles for dark theme"""
        style = ttk.Style()
        
        # Configure base theme
        style.theme_use('clam')
        
        # Main theme colors
        style.configure('.',
                       background=BG_PRIMARY,
                       foreground=TEXT_PRIMARY,
                       fieldbackground=BG_SECONDARY,
                       bordercolor=BG_TERTIARY,
                       darkcolor=BG_SECONDARY,
                       lightcolor=BG_TERTIARY)
        
        # Button style
        style.configure('TButton',
                       background=BG_SECONDARY,
                       foreground=TEXT_PRIMARY,
                       borderwidth=1,
                       focuscolor=ACCENT_CYAN,
                       padding=10)
        style.map('TButton',
                 background=[('active', BG_TERTIARY), ('pressed', ACCENT_CYAN)],
                 foreground=[('active', TEXT_PRIMARY)])
        
        # Accent button style
        style.configure('Accent.TButton',
                       background=ACCENT_CYAN,
                       foreground=BG_PRIMARY,
                       borderwidth=0,
                       padding=10)
        style.map('Accent.TButton',
                 background=[('active', ACCENT_GOLD), ('pressed', '#00a888')],
                 foreground=[('active', BG_PRIMARY)])
        
        # Entry style
        style.configure('TEntry',
                       fieldbackground=BG_SECONDARY,
                       foreground=TEXT_PRIMARY,
                       bordercolor=BG_TERTIARY,
                       insertcolor=TEXT_PRIMARY)
        
        # Label style
        style.configure('TLabel',
                       background=BG_PRIMARY,
                       foreground=TEXT_PRIMARY)
        
        # Header label
        style.configure('Header.TLabel',
                       background=BG_PRIMARY,
                       foreground=TEXT_PRIMARY,
                       font=(FONT_FAMILY, FONT_SIZE_HEADER, 'bold'))
        
        # Subheader label
        style.configure('Subheader.TLabel',
                       background=BG_PRIMARY,
                       foreground=TEXT_SECONDARY,
                       font=(FONT_FAMILY, FONT_SIZE_SUBHEADER))
        
        # Frame style
        style.configure('TFrame',
                       background=BG_PRIMARY)
        
        # Card frame style (elevated background)
        style.configure('Card.TFrame',
                       background=BG_SECONDARY,
                       relief='flat')
        
        # Treeview style
        style.configure('Treeview',
                       background=BG_SECONDARY,
                       foreground=TEXT_PRIMARY,
                       fieldbackground=BG_SECONDARY,
                       borderwidth=0)
        style.map('Treeview',
                 background=[('selected', ACCENT_CYAN)],
                 foreground=[('selected', BG_PRIMARY)])
        
        # Treeview heading
        style.configure('Treeview.Heading',
                       background=BG_TERTIARY,
                       foreground=TEXT_PRIMARY,
                       relief='flat')
        style.map('Treeview.Heading',
                 background=[('active', ACCENT_CYAN)])
        
        # Combobox
        style.configure('TCombobox',
                       fieldbackground=BG_SECONDARY,
                       background=BG_SECONDARY,
                       foreground=TEXT_PRIMARY,
                       bordercolor=BG_TERTIARY,
                       arrowcolor=TEXT_PRIMARY)
        
        # Notebook (tabs)
        style.configure('TNotebook',
                       background=BG_PRIMARY,
                       borderwidth=0,
                       tabmargins=[2, 5, 2, 0])
        
        style.configure('TNotebook.Tab',
                       background=BG_SECONDARY,
                       foreground=TEXT_SECONDARY,
                       padding=[20, 10],
                       borderwidth=0)
        style.map('TNotebook.Tab',
                 background=[('selected', BG_PRIMARY)],
                 foreground=[('selected', ACCENT_CYAN)],
                 expand=[('selected', [1, 1, 1, 0])])


class CardFrame(ttk.Frame):
    """Elevated card-style frame"""
    
    def __init__(self, parent, title: str = "", **kwargs):
        super().__init__(parent, style='Card.TFrame', **kwargs)
        self.configure(padding=PADDING_LARGE)
        
        if title:
            title_label = ttk.Label(self, text=title,
                                   font=(FONT_FAMILY, FONT_SIZE_SUBHEADER, 'bold'),
                                   foreground=ACCENT_CYAN)
            title_label.pack(anchor='w', pady=(0, PADDING_MEDIUM))


class SearchBar(ttk.Frame):
    """Search bar with live filtering"""
    
    def __init__(self, parent, on_search: Callable[[str], None], 
                 placeholder: str = "Search...", **kwargs):
        super().__init__(parent, **kwargs)
        self.on_search = on_search
        self.placeholder = placeholder
        
        # Search icon label (using text for simplicity)
        icon_label = ttk.Label(self, text="🔍", 
                              font=(FONT_FAMILY, 12))
        icon_label.pack(side='left', padx=(5, 5))
        
        # Search entry
        self.entry = ttk.Entry(self, font=(FONT_FAMILY, FONT_SIZE_NORMAL))
        self.entry.pack(side='left', fill='x', expand=True, padx=5)
        self.entry.bind('<KeyRelease>', self._on_key_release)
        
        # Show placeholder
        self._show_placeholder()
        self.entry.bind('<FocusIn>', self._on_focus_in)
        self.entry.bind('<FocusOut>', self._on_focus_out)
    
    def _show_placeholder(self):
        """Show placeholder text"""
        self.entry.insert(0, self.placeholder)
        self.entry.config(foreground=TEXT_DISABLED)
    
    def _on_focus_in(self, event):
        """Remove placeholder on focus"""
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, 'end')
            self.entry.config(foreground=TEXT_PRIMARY)
    
    def _on_focus_out(self, event):
        """Restore placeholder if empty"""
        if not self.entry.get():
            self._show_placeholder()
    
    def _on_key_release(self, event):
        """Trigger search on key release"""
        query = self.entry.get()
        if query != self.placeholder:
            self.on_search(query)


class ViewModeSelector(ttk.Frame):
    """Toggle buttons for 2D/ISO/3D view modes"""
    
    def __init__(self, parent, on_change: Callable[[str], None], **kwargs):
        super().__init__(parent, **kwargs)
        self.on_change = on_change
        self.current_mode = VIEW_MODE_2D
        self.buttons = {}
        
        # Create toggle buttons
        modes = [
            (VIEW_MODE_2D, "2D Cross-Section"),
            (VIEW_MODE_ISO, "Isometric"),
            (VIEW_MODE_3D, "3D View")
        ]
        
        for mode, label in modes:
            btn = tk.Button(self, text=label,
                          font=(FONT_FAMILY, FONT_SIZE_NORMAL),
                          relief='flat',
                          bd=0,
                          padx=20,
                          pady=8,
                          command=lambda m=mode: self._set_mode(m))
            btn.pack(side='left', padx=2)
            self.buttons[mode] = btn
        
        # Set initial state
        self._update_button_styles()
    
    def _set_mode(self, mode: str):
        """Set active view mode"""
        if mode != self.current_mode:
            self.current_mode = mode
            self._update_button_styles()
            self.on_change(mode)
    
    def _update_button_styles(self):
        """Update button appearance based on active mode"""
        for mode, btn in self.buttons.items():
            if mode == self.current_mode:
                btn.config(bg=ACCENT_CYAN, fg=BG_PRIMARY,
                          font=(FONT_FAMILY, FONT_SIZE_NORMAL, 'bold'))
            else:
                btn.config(bg=BG_SECONDARY, fg=TEXT_SECONDARY,
                          font=(FONT_FAMILY, FONT_SIZE_NORMAL))


class StatusBar(ttk.Frame):
    """Status bar at bottom of window"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(padding=5)
        
        # Left status text
        self.status_label = ttk.Label(self, text="Ready",
                                     foreground=TEXT_SECONDARY,
                                     font=(FONT_FAMILY, FONT_SIZE_SMALL))
        self.status_label.pack(side='left')
        
        # Right info text
        self.info_label = ttk.Label(self, text="",
                                   foreground=TEXT_SECONDARY,
                                   font=(FONT_FAMILY, FONT_SIZE_SMALL))
        self.info_label.pack(side='right')
    
    def set_status(self, text: str, color: str = TEXT_SECONDARY):
        """Update status text"""
        self.status_label.config(text=text, foreground=color)
    
    def set_info(self, text: str):
        """Update info text"""
        self.info_label.config(text=text)


class DataTable(ttk.Frame):
    """Styled data table with Treeview"""
    
    def __init__(self, parent, columns: List[tuple], **kwargs):
        """
        Initialize data table
        
        Args:
            parent: Parent widget
            columns: List of (column_id, column_name, width) tuples
        """
        super().__init__(parent, **kwargs)
        
        # Create treeview with scrollbars
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(self.tree_frame, orient='vertical')
        hsb = ttk.Scrollbar(self.tree_frame, orient='horizontal')
        
        # Treeview
        self.tree = ttk.Treeview(self.tree_frame,
                                columns=[col[0] for col in columns],
                                show='tree headings',
                                yscrollcommand=vsb.set,
                                xscrollcommand=hsb.set)
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        
        # Configure columns
        self.tree.column('#0', width=0, stretch=False)  # Hide tree column
        for col_id, col_name, width in columns:
            self.tree.heading(col_id, text=col_name)
            self.tree.column(col_id, width=width, anchor='center')
        
        # Alternating row colors
        self.tree.tag_configure('oddrow', background=BG_SECONDARY)
        self.tree.tag_configure('evenrow', background=BG_TERTIARY)
    
    def insert_row(self, values: List, tags: tuple = ()):
        """Insert a row into the table"""
        row_count = len(self.tree.get_children())
        row_tags = ('oddrow' if row_count % 2 == 0 else 'evenrow',) + tags
        self.tree.insert('', 'end', values=values, tags=row_tags)
    
    def clear(self):
        """Clear all rows"""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def get_selection(self) -> Optional[List]:
        """Get selected row values"""
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0])['values']
        return None


class LoadingIndicator(ttk.Frame):
    """Simple loading indicator"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.label = ttk.Label(self, text="⏳ Loading...",
                              foreground=ACCENT_CYAN,
                              font=(FONT_FAMILY, FONT_SIZE_NORMAL))
        self.label.pack(pady=20)
        self.visible = False
    
    def show(self):
        """Show loading indicator"""
        if not self.visible:
            self.pack(fill='both', expand=True)
            self.visible = True
    
    def hide(self):
        """Hide loading indicator"""
        if self.visible:
            self.pack_forget()
            self.visible = False


class ToolTip:
    """Tooltip for widgets"""
    
    def __init__(self, widget, text: str):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind('<Enter>', self._show)
        self.widget.bind('<Leave>', self._hide)
    
    def _show(self, event=None):
        """Show tooltip"""
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=self.text,
                        background=BG_TERTIARY,
                        foreground=TEXT_PRIMARY,
                        relief='solid',
                        borderwidth=1,
                        font=(FONT_FAMILY, FONT_SIZE_SMALL),
                        padx=10, pady=5)
        label.pack()
    
    def _hide(self, event=None):
        """Hide tooltip"""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
