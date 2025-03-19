# main.py
import tkinter as tk
from database import create_tables

# Importamos con nombres distintos para evitar choque de nombres
from views.gui_registro_personas import RegistroWindow as RegistroPersonasWindow
from views.gui_registro_vehiculos import RegistroWindow as RegistroVehiculosWindow
from views.gui_principal import PrincipalWindow

# (Opcional) Si tienes un gui_login.py:
# from views.gui_login import LoginWindow

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Control de Acceso")

        # Crea las tablas si no existen
        create_tables()

        # Botones principales
        # (Descomenta la línea de login si ya tienes gui_login.py y un método abrir_login)
        # tk.Button(self, text="Iniciar Sesión", command=self.abrir_login).pack(pady=5)

        tk.Button(self, text="Registrar Persona", command=self.abrir_registro_persona).pack(pady=5)
        tk.Button(self, text="Registrar Vehículo", command=self.abrir_registro_vehiculo).pack(pady=5)
        tk.Button(self, text="Panel Principal (Búsqueda)", command=self.abrir_principal).pack(pady=5)

    # (Opcional) Método para abrir la ventana de Login
    # def abrir_login(self):
    #     login_window = LoginWindow(self)
    #     login_window.grab_set()

    def abrir_registro_persona(self):
        """Abre la ventana para registrar personas."""
        registro_window = RegistroPersonasWindow(self)
        registro_window.grab_set()  # Ventana modal

    def abrir_registro_vehiculo(self):
        """Abre la ventana para registrar vehículos."""
        registro_window = RegistroVehiculosWindow(self)
        registro_window.grab_set()  # Ventana modal

    def abrir_principal(self):
        """Abre la ventana principal (búsqueda, reportes, etc.)."""
        principal_window = PrincipalWindow(self)
        principal_window.grab_set()

if __name__ == "__main__":
    app = App()
    app.mainloop()