import tkinter as tk
from tkinter import ttk  # Añadir para usar widgets mejorados
from database import create_tables
from PIL import Image, ImageTk  # Importar PIL para manejar imágenes
import os

# Importaciones más limpias usando un diccionario de vistas
from views.gui_registro_personas import RegistroWindow as RegistroPersonasWindow
from views.gui_registro_visitas import RegistroWindow as RegistroVisitantesWindow
from views.gui_registro_vehiculos import RegistroWindow as RegistroVehiculosWindow
from views.gui_principal import PrincipalWindow


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Control de Acceso FNO")
        self.configure(padx=20, pady=20, bg='#333333')
        self.setup_database()
        self.setup_ui()

    def setup_database(self):
        create_tables()

    def setup_ui(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        header_frame = ttk.Frame(main_frame)
        header_frame.pack(pady=10)

        try:
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "escudo.png")
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                logo_img = logo_img.resize((100, 100))
                logo_photo = ImageTk.PhotoImage(logo_img)
                logo_label = ttk.Label(header_frame, image=logo_photo)
                logo_label.image = logo_photo
                logo_label.pack(pady=(0, 10))
        except Exception as e:
            print(f"Error al cargar el escudo: {e}")

        ttk.Label(
            header_frame,
            text="Sistema de Control de Acceso FNO",
            font=("Helvetica", 16, "bold")
        ).pack()

        buttons = [
            ("Registrar Persona", self.abrir_registro_persona),
            ("Registrar Vehículo", self.abrir_registro_vehiculo),
            ("Registrar Visitante", self.abrir_registro_visitante),
            ("Panel Principal (Búsqueda)", self.abrir_principal)
        ]

        ttk.Frame(main_frame, height=20).pack()

        style = ttk.Style()
        style.configure('TButton', background='#666666')

        for text, command in buttons:
            ttk.Button(
                main_frame,
                text=text,
                command=command,
                width=30
            ).pack(pady=5)

        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(20, 0))

        signature_label = ttk.Label(
            footer_frame,
            text="Desarrollado por Kwaltas",
            font=("Arial", 8, "italic"),
            foreground="#888888"
        )
        signature_label.pack(side=tk.RIGHT, padx=10)

    def _abrir_ventana(self, window_class, title, geometry):
        window = window_class(self, title, geometry)
        return window

    def abrir_registro_persona(self):
        return self._abrir_ventana(RegistroPersonasWindow, "Registro de Personal", "650x650")

    def abrir_registro_visitante(self):
        return self._abrir_ventana(RegistroVisitantesWindow, "Registro de Visitantes", "600x500")

    def abrir_registro_vehiculo(self):
        return self._abrir_ventana(RegistroVehiculosWindow, "Registro de Vehículo", "650x650")

    def abrir_principal(self):
        return self._abrir_ventana(PrincipalWindow, "Panel Principal - Control de Acceso", "800x700")

if __name__ == "__main__":
    app = App()
    # Centrar ventana principal
    app.update_idletasks()
    width = app.winfo_width()
    height = app.winfo_height()
    x = (app.winfo_screenwidth() // 2) - (width // 2)
    y = (app.winfo_screenheight() // 2) - (height // 2)
    app.geometry(f"{width}x{height}+{x}+{y}")
    app.mainloop()