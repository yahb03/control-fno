import tkinter as tk
from tkinter import ttk

class BaseWindow(tk.Toplevel):
    def __init__(self, master, title, geometry="600x400"):
        super().__init__(master)
        self.title(title)
        self.geometry(geometry)
        self.protocol("WM_DELETE_WINDOW", self.volver)
        self.create_widgets()
        self.setup_styles()
        self.center_window()
        self.grab_set()

    def create_widgets(self):
        """Placeholder for creating widgets in subclasses."""
        pass

    def setup_styles(self):
        """Configure styles for the window."""
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 10))
        style.configure("TButton", font=("Helvetica", 10))
        style.configure("TEntry", font=("Helvetica", 10))
        style.configure("Accent.TButton", background="#4CAF50", foreground="white", font=("Helvetica", 10, "bold"))

    def center_window(self):
        """Centers the window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def volver(self):
        """Closes the window."""
        self.grab_release()
        self.destroy()
