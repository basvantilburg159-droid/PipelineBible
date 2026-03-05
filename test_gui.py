#!/usr/bin/env python3
"""
Quick GUI test to verify tkinter works
"""

import tkinter as tk
from tkinter import messagebox

def main():
    # Create a simple window
    root = tk.Tk()
    root.title("Tkinter Test")
    root.geometry("300x200")
    
    # Add a label
    label = tk.Label(root, text="Tkinter is working! ✓", font=("Arial", 14))
    label.pack(pady=20)
    
    # Add a button
    def on_click():
        messagebox.showinfo("Test", "GUI working correctly!")
    
    button = tk.Button(root, text="Click me", command=on_click, font=("Arial", 12))
    button.pack(pady=10)
    
    # Run
    root.mainloop()

if __name__ == "__main__":
    main()
