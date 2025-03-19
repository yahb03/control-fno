import tkinter as tk
from tkinter import messagebox, filedialog
import bcrypt
from database import create_connection

class RegistroWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Registro de Usuario")

        # Variables para almacenar las rutas de las fotos
        self.foto_persona_path = ""

        # --- Datos del Personal ---
        tk.Label(self, text="GRADO:").grid(row=0, column=0, padx=5, pady=5)
        self.grado_entry = tk.Entry(self)
        self.grado_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="NOMBRE:").grid(row=1, column=0, padx=5, pady=5)
        self.nombre_entry = tk.Entry(self)
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="APELLIDOS:").grid(row=2, column=0, padx=5, pady=5)
        self.apellidos_entry = tk.Entry(self)
        self.apellidos_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self, text="CÉDULA:").grid(row=3, column=0, padx=5, pady=5)
        self.cedula_entry = tk.Entry(self)
        self.cedula_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self, text="DEPENDENCIA:").grid(row=4, column=0, padx=5, pady=5)
        self.dependencia_entry = tk.Entry(self)
        self.dependencia_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self, text="LICENCIA CONDUCCIÓN:").grid(row=5, column=0, padx=5, pady=5)
        self.licencia_cond_entry = tk.Entry(self)
        self.licencia_cond_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self, text="VIGENCIA LICENCIA:").grid(row=6, column=0, padx=5, pady=5)
        self.vigencia_lic_entry = tk.Entry(self)
        self.vigencia_lic_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(self, text="TELÉFONO:").grid(row=7, column=0, padx=5, pady=5)
        self.telefono_entry = tk.Entry(self)
        self.telefono_entry.grid(row=7, column=1, padx=5, pady=5)

        tk.Label(self, text="CONTRASEÑA:").grid(row=8, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=8, column=1, padx=5, pady=5)

        # Botón para cargar foto de la persona
        tk.Button(self, text="Cargar Foto Persona", command=self.cargar_foto_persona).grid(row=9, column=0, columnspan=2, pady=5)
        self.label_foto_persona = tk.Label(self, text="No seleccionado")
        self.label_foto_persona.grid(row=9, column=2, columnspan=2, pady=5)

# Botones de acción: Registrar y Volver
        tk.Button(self, text="REGISTRAR", command=self.registrar_datos).grid(row=10, column=0, columnspan=2, pady=10)
        tk.Button(self, text="VOLVER", command=self.volver).grid(row=10, column=2, columnspan=2, pady=10)

    def cargar_foto_persona(self):
        """Abre un diálogo para seleccionar la foto de la persona."""
        ruta = filedialog.askopenfilename(title="Selecciona la foto de la persona", 
                                          filetypes=[("Archivos de imagen", "*.png *.jpg *.jpeg *.gif")])
        if ruta:
            self.foto_persona_path = ruta
            self.label_foto_persona.config(text="Foto seleccionada")

    def registrar_datos(self):
        # Recolecta los datos del personal
        grado = self.grado_entry.get()
        nombre = self.nombre_entry.get()
        apellidos = self.apellidos_entry.get()
        cedula = self.cedula_entry.get()
        dependencia = self.dependencia_entry.get()
        licencia_cond = self.licencia_cond_entry.get()
        vigencia_lic = self.vigencia_lic_entry.get()
        telefono = self.telefono_entry.get()
        password = self.password_entry.get().encode('utf-8')    
        # Validar que la contraseña no esté vacía
        if not password:
            messagebox.showerror("Error", "La contraseña no puede estar vacía.")
            return
        # Validar que la foto de la persona esté seleccionada
        if not self.foto_persona_path:
            messagebox.showerror("Error", "Debes seleccionar una foto de la persona.")

        # Hashear la contraseña
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

          # Inserta en la base de datos (asegúrate de que en tus tablas existan los campos para las fotos)
        conn = create_connection()
        cursor = conn.cursor()

        
        try:
            # Insertar usuario (se asume que la tabla 'usuarios' tiene una columna extra, por ejemplo 'foto_persona')
            cursor.execute('''
                INSERT INTO usuarios (grado, nombre, apellidos, cedula, dependencia, telefono,
                                      licencia_conduccion, vigencia_licencia, password, foto_persona)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (grado, nombre, apellidos, cedula, dependencia, telefono,
                  licencia_cond, vigencia_lic, hashed.decode('utf-8'), self.foto_persona_path))
            conn.commit()
            messagebox.showinfo("Éxito", "Registro realizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
        finally:
            conn.close()

    def volver(self):
        """Cierra la ventana de registro y regresa a la ventana anterior."""
        self.destroy()


