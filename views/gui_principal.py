import tkinter as tk
from tkinter import messagebox
from database import create_connection
from PIL import Image, ImageTk
import os

class PrincipalWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Panel Principal")

        # --- Búsqueda por Cédula ---
        tk.Label(self, text="Buscar por Cédula:").grid(row=0, column=0, padx=5, pady=5)
        self.cedula_search = tk.Entry(self)
        self.cedula_search.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self, text="Buscar", command=self.buscar_por_cedula).grid(row=0, column=2, padx=5, pady=5)

        # --- Búsqueda por Placa ---
        tk.Label(self, text="Buscar por Placa:").grid(row=1, column=0, padx=5, pady=5)
        self.placa_search = tk.Entry(self)
        self.placa_search.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self, text="Buscar", command=self.buscar_por_placa).grid(row=1, column=2, padx=5, pady=5)

        # --- Resultado de Búsqueda ---
        self.result_label = tk.Label(self, text="", fg="blue", justify="left")
        self.result_label.grid(row=2, column=0, columnspan=3, pady=10)
        self.result_label.config(text="Resultados de la búsqueda aparecerán aquí.", fg="blue")
        self.result_label.grid(row=2, column=0, columnspan=3, pady=10)

        # --- Espacio para mostrar la imagen ---
        self.image_label = tk.Label(self)
        self.image_label.grid(row=3, column=0, columnspan=3, pady=10)

    def buscar_por_cedula(self):
        """Busca un usuario en la base de datos por su cédula y muestra la foto."""
        cedula = self.cedula_search.get().strip()

        if not cedula:
            self.result_label.config(text="Por favor ingresa una cédula.", fg="red")
            return

        conn = create_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT grado, nombre, apellidos, cedula, dependencia, foto_persona FROM usuarios WHERE cedula=?", (cedula,))
            result = cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar en la base de datos: {e}")
            result = None

        conn.close()

        if result:
            grado, nombre, apellidos, cedula, dependencia, foto_path = result
            self.result_label.config(
                text=f"Usuario encontrado:\n"
                     f"Grado: {grado}\n"
                     f"Nombre: {nombre} {apellidos}\n"
                     f"Cédula: {cedula}\n"
                     f"Dependencia: {dependencia}",
                fg="blue"
            )
            self.mostrar_imagen(foto_path)
        else:
            self.result_label.config(text="Usuario no encontrado o sin acceso.", fg="red")
            self.mostrar_imagen(None)

    def buscar_por_placa(self):
        """Busca un vehículo en la base de datos por su placa y muestra la foto."""
        placa = self.placa_search.get().strip()

        if not placa:
            self.result_label.config(text="Por favor ingresa una placa.", fg="red")
            return

        conn = create_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT placa, marca, modelo, componente_vehiculo, responsable_vehiculo, foto_vehiculo FROM vehiculos WHERE placa=?", (placa,))
            result = cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar en la base de datos: {e}")
            result = None

        conn.close()

        if result:
            placa, marca, modelo, componente_vehiculo, responsable_vehiculo, foto_path = result
            self.result_label.config(
                text=f"Vehículo encontrado:\n"
                     f"Placa: {placa}\n"
                     f"Marca: {marca}\n"
                     f"Modelo: {modelo}\n"
                     f"Componente: {componente_vehiculo}\n"
                     f"Responsable: {responsable_vehiculo}",
                fg="blue"
            )
            self.mostrar_imagen(foto_path)
        else:
            self.result_label.config(text="Vehículo no encontrado o sin acceso.", fg="red")
            self.mostrar_imagen(None)

    def mostrar_imagen(self, foto_path):
        """Muestra la imagen de la persona o el vehículo en la interfaz."""
        if foto_path and os.path.exists(foto_path):  # Verifica que la imagen exista
            img = Image.open(foto_path)
            img = img.resize((200, 200), Image.LANCZOS)  # Redimensiona la imagen
            img = ImageTk.PhotoImage(img)
        else:
            # Imagen por defecto si no hay foto disponible
            img = Image.open("assets/sin_foto.png")  # Debes tener una imagen "sin_foto.png"
            img = img.resize((200, 200), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)

        self.image_label.config(image=img)
        self.image_label.image = img  # Guardar referencia para que no se elimine de la memoria