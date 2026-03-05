#!/usr/bin/env python3
"""
PipelineBible GUI Launcher
Simpele GUI die niet afsluit - blijft open voor interactief gebruik
"""

import sys

# Check if tkinter is available
try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    print("ERROR: tkinter niet beschikbaar!")
    print("Installeer met: pip install tk")
    input("Druk op Enter om af te sluiten...")
    sys.exit(1)

from PipelineBible import (
    PipeLookup, FlangeLookup, PrettyPrint, DataExport,
    ASME_PIPES, DIN_PIPES, ASME_FL, DIN_FL
)

class PipelineBibleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PipelineBible v1.1 - Pipeline Standards Tool")
        self.root.geometry("900x700")
        
        # Styling
        style = ttk.Style()
        style.theme_use('clam')
        
        # Header
        header = tk.Frame(root, bg="#1a1a1a", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="PipelineBible v1.1", 
                        font=("Arial", 18, "bold"), 
                        bg="#1a1a1a", fg="#f0a500")
        title.pack(pady=15)
        
        # Main container
        main = ttk.Frame(root, padding="10")
        main.pack(fill=tk.BOTH, expand=True)
        
        # Tabs
        notebook = ttk.Notebook(main)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Pipe Lookup
        pipe_frame = ttk.Frame(notebook)
        notebook.add(pipe_frame, text="Pipe Lookup")
        self.create_pipe_lookup_tab(pipe_frame)
        
        # Tab 2: Flange Lookup
        flange_frame = ttk.Frame(notebook)
        notebook.add(flange_frame, text="Flange Lookup")
        self.create_flange_lookup_tab(flange_frame)
        
        # Tab 3: Info
        info_frame = ttk.Frame(notebook)
        notebook.add(info_frame, text="Info & Help")
        self.create_info_tab(info_frame)
        
        # Output area (bottom)
        output_label = ttk.Label(main, text="Output:", font=("Arial", 10, "bold"))
        output_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.output = scrolledtext.ScrolledText(main, height=10, 
                                                 font=("Courier", 9),
                                                 bg="#f5f5f5")
        self.output.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status = tk.Label(root, text="Klaar", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.print_welcome()
    
    def create_pipe_lookup_tab(self, parent):
        """Tab voor pipe lookup"""
        frame = ttk.Frame(parent, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Standard selection
        ttk.Label(frame, text="Standard:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.pipe_std = tk.StringVar(value="ASME")
        ttk.Radiobutton(frame, text="ASME", variable=self.pipe_std, value="ASME").grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(frame, text="DIN", variable=self.pipe_std, value="DIN").grid(row=0, column=2, sticky=tk.W)
        
        # Size selection
        ttk.Label(frame, text="Size (NPS/DN):", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.pipe_size = ttk.Combobox(frame, width=15)
        self.pipe_size.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=5)
        self.update_pipe_sizes()
        
        # Schedule selection
        ttk.Label(frame, text="Schedule/WT:", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.pipe_schedule = ttk.Combobox(frame, width=15)
        self.pipe_schedule.grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        # Update schedules when size changes
        self.pipe_size.bind('<<ComboboxSelected>>', self.update_pipe_schedules)
        self.pipe_std.trace('w', lambda *args: self.update_pipe_sizes())
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        ttk.Button(btn_frame, text="Zoek Pipe", command=self.lookup_pipe).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Pretty Print", command=self.pretty_print_pipe).pack(side=tk.LEFT, padx=5)
        
    def create_flange_lookup_tab(self, parent):
        """Tab voor flange lookup"""
        frame = ttk.Frame(parent, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Standard selection
        ttk.Label(frame, text="Standard:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.flange_std = tk.StringVar(value="ASME")
        ttk.Radiobutton(frame, text="ASME", variable=self.flange_std, value="ASME").grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(frame, text="DIN", variable=self.flange_std, value="DIN").grid(row=0, column=2, sticky=tk.W)
        
        # Size selection
        ttk.Label(frame, text="Size (NPS/DN):", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.flange_size = ttk.Combobox(frame, width=15)
        self.flange_size.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=5)
        self.update_flange_sizes()
        
        # Class selection
        ttk.Label(frame, text="Class/PN:", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.flange_class = ttk.Combobox(frame, width=15)
        self.flange_class.grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        # Update classes when size changes
        self.flange_size.bind('<<ComboboxSelected>>', self.update_flange_classes)
        self.flange_std.trace('w', lambda *args: self.update_flange_sizes())
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        ttk.Button(btn_frame, text="Zoek Flens", command=self.lookup_flange).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Pretty Print", command=self.pretty_print_flange).pack(side=tk.LEFT, padx=5)
    
    def create_info_tab(self, parent):
        """Info tab"""
        frame = ttk.Frame(parent, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        info = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=("Arial", 10))
        info.pack(fill=tk.BOTH, expand=True)
        
        info_text = f"""
PipelineBible v1.1
Professional Pipeline & Piping Standards Tool

DATABASE COVERAGE:
• ASME Pipes: {len(ASME_PIPES)} sizes (NPS 1/2" tot 56")
• DIN Pipes: {len(DIN_PIPES)} sizes (DN15 tot DN600)
• ASME Flanges: {len(ASME_FL)} configuraties
• DIN Flanges: {len(DIN_FL)} configuraties

FEATURES:
✓ Pipe dimensies (OD, WT, ID, gewicht)
✓ Flens specificaties (alle classes)
✓ Bend berekeningen (1D tot 10D)
✓ Bolt length calculator
✓ Data export (CSV, JSON)
✓ Pretty print formatters

GEBRUIK:
1. Kies een tab (Pipe of Flange)
2. Selecteer standard (ASME of DIN)
3. Kies size en schedule/class
4. Klik op "Zoek" of "Pretty Print"

COMMAND LINE:
Je kunt ook via command line werken:
  python3 test_pipelinebible.py  (test alles)
  python3 PipelineBible.py       (demo)

DOCUMENTATIE:
• README.md - Volledige documentatie
• QUICKSTART.md - Nederlandse snelgids
• test_pipelinebible.py - Test voorbeelden

VERSIE GESCHIEDENIS:
v1.1 - Helper classes, export, pretty print
v1.0 - Initiele release

© 2026 PipelineBible
        """
        
        info.insert(1.0, info_text)
        info.config(state=tk.DISABLED)
    
    def update_pipe_sizes(self):
        """Update pipe size dropdown"""
        std = self.pipe_std.get()
        pipes = ASME_PIPES if std == "ASME" else DIN_PIPES
        sizes = [p[0] for p in pipes]
        self.pipe_size['values'] = sizes
        if sizes:
            self.pipe_size.set(sizes[0])
        self.update_pipe_schedules(None)
    
    def update_pipe_schedules(self, event):
        """Update schedule dropdown"""
        size = self.pipe_size.get()
        std = self.pipe_std.get()
        if size:
            schedules = PipeLookup.list_schedules(size, std)
            self.pipe_schedule['values'] = schedules
            if schedules:
                self.pipe_schedule.set(schedules[0])
    
    def update_flange_sizes(self):
        """Update flange size dropdown"""
        std = self.flange_std.get()
        flanges = ASME_FL if std == "ASME" else DIN_FL
        sizes = sorted(list(set([f[0] for f in flanges])), key=lambda x: float(x.replace("DN", "").replace("-", ".")) if x.replace("DN", "").replace("-", ".").replace("/", "").replace(".", "").isdigit() else 999)
        self.flange_size['values'] = sizes
        if sizes:
            self.flange_size.set(sizes[0])
        self.update_flange_classes(None)
    
    def update_flange_classes(self, event):
        """Update class dropdown"""
        size = self.flange_size.get()
        std = self.flange_std.get()
        if size:
            classes = FlangeLookup.list_classes(size, std)
            self.flange_class['values'] = classes
            if classes:
                self.flange_class.set(classes[0])
    
    def lookup_pipe(self):
        """Lookup pipe dimensions"""
        size = self.pipe_size.get()
        schedule = self.pipe_schedule.get()
        std = self.pipe_std.get()
        
        self.clear_output()
        dims = PipeLookup.get_pipe_dimension(size, schedule, std)
        
        if dims:
            self.output.insert(tk.END, f"═══════════════════════════════════════════\n")
            self.output.insert(tk.END, f"{std} Pipe: {size} Schedule {schedule}\n")
            self.output.insert(tk.END, f"═══════════════════════════════════════════\n\n")
            self.output.insert(tk.END, f"Outside Diameter: {dims['od']:.2f} mm ({dims['oi']:.3f}\")\n")
            if dims['wt']:
                self.output.insert(tk.END, f"Wall Thickness:   {dims['wt']:.2f} mm ({dims['wi']:.3f}\")\n")
                self.output.insert(tk.END, f"Inside Diameter:  {dims['id']:.2f} mm ({dims['ii']:.3f}\")\n")
                self.output.insert(tk.END, f"Inside Radius:    {dims['ir']:.2f} mm ({dims['ri']:.3f}\")\n")
                self.output.insert(tk.END, f"Weight per meter: {dims['kg']:.2f} kg/m\n")
            else:
                self.output.insert(tk.END, "Wall thickness niet beschikbaar in database\n")
            
            self.status.config(text=f"Gevonden: {std} {size} {schedule}")
        else:
            self.output.insert(tk.END, f"✗ Pipe niet gevonden: {std} {size} {schedule}\n")
            self.status.config(text="Niet gevonden")
    
    def pretty_print_pipe(self):
        """Pretty print pipe"""
        size = self.pipe_size.get()
        schedule = self.pipe_schedule.get()
        std = self.pipe_std.get()
        
        self.clear_output()
        
        # Capture print output
        import io
        import contextlib
        
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            PrettyPrint.print_pipe(size, schedule, std)
        
        output = f.getvalue()
        self.output.insert(tk.END, output)
        self.status.config(text=f"Pretty print: {std} {size} {schedule}")
    
    def lookup_flange(self):
        """Lookup flange data"""
        size = self.flange_size.get()
        try:
            cls = int(self.flange_class.get())
        except:
            messagebox.showerror("Error", "Selecteer een geldige class/PN")
            return
        
        std = self.flange_std.get()
        
        self.clear_output()
        flange = FlangeLookup.get_flange_data(size, cls, std)
        
        if flange:
            self.output.insert(tk.END, f"═══════════════════════════════════════════\n")
            if std == "ASME":
                self.output.insert(tk.END, f"ASME Flange: {flange['nps']}\" Class {flange['class']}\n")
                self.output.insert(tk.END, f"Series: {flange['series']}\n")
            else:
                self.output.insert(tk.END, f"DIN Flange: {flange['dn']} PN {flange['pn']}\n")
            self.output.insert(tk.END, f"═══════════════════════════════════════════\n\n")
            self.output.insert(tk.END, f"Flange OD:       {flange['flange_od']:.1f} mm\n")
            self.output.insert(tk.END, f"Thickness:       {flange['thickness']:.1f} mm\n")
            self.output.insert(tk.END, f"Bolt Circle:     {flange['bolt_circle']:.1f} mm\n")
            self.output.insert(tk.END, f"Bolt Holes:      {flange['bolt_holes']}\n")
            self.output.insert(tk.END, f"Bolt Size:       {flange['bolt_size']}\n")
            self.output.insert(tk.END, f"Raised Face OD:  {flange['rf_od']:.1f} mm\n")
            self.output.insert(tk.END, f"Bore:            {flange['bore']:.1f} mm\n")
            
            self.status.config(text=f"Gevonden: {std} {size} Class {cls}")
        else:
            self.output.insert(tk.END, f"✗ Flange niet gevonden: {std} {size} Class {cls}\n")
            self.status.config(text="Niet gevonden")
    
    def pretty_print_flange(self):
        """Pretty print flange"""
        size = self.flange_size.get()
        try:
            cls = int(self.flange_class.get())
        except:
            messagebox.showerror("Error", "Selecteer een geldige class/PN")
            return
        
        std = self.flange_std.get()
        
        self.clear_output()
        
        import io
        import contextlib
        
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            PrettyPrint.print_flange(size, cls, std)
        
        output = f.getvalue()
        self.output.insert(tk.END, output)
        self.status.config(text=f"Pretty print: {std} {size} Class {cls}")
    
    def clear_output(self):
        """Clear output area"""
        self.output.delete(1.0, tk.END)
    
    def print_welcome(self):
        """Print welcome message"""
        welcome = """
╔═══════════════════════════════════════════════════════════════╗
║         Welkom bij PipelineBible v1.1                         ║
║         Professional Pipeline & Piping Standards Tool         ║
╚═══════════════════════════════════════════════════════════════╝

Gebruik de tabs hierboven om pipes en flanges op te zoeken.
Kies standard (ASME/DIN), selecteer size en schedule/class.
Resultaten verschijnen hier in het output venster.

Deze GUI blijft open - sluit het venster om af te sluiten.
        """
        self.output.insert(tk.END, welcome)


def main():
    """Start GUI"""
    root = tk.Tk()
    app = PipelineBibleGUI(root)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()
