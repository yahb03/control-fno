# views/gui_registro_visitantes.py

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import tkinter.filedialog as fd
import os
import logging

# Importar desde database.py (ambas opciones para compatibilidad)
try:
    from database import create_connection, get_connection
except ImportError:
    from database import create_connection

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger('visitantes')

from utils.ui import BaseWindow

class RegistroWindow(BaseWindow):
    def __init__(self, master, title, geometry):
        super().__init__(master, title, geometry)
        self.foto_path = tk.StringVar()
        self.nombre_entry.focus_set()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            main_frame,
            text="Registro de Visitantes",
            font=("Helvetica", 14, "bold")
        ).grid(row=0, column=0, columnspan=3, pady=10, sticky=tk.W)

        self.create_form_fields(main_frame)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=11, column=0, columnspan=3, pady=20, sticky=tk.EW)

        ttk.Button(
            button_frame,
            text="REGISTRAR",
            command=self.registrar_datos,
            style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=10)

        ttk.Button(
            button_frame,
            text="LIMPIAR",
            command=self.limpiar_campos
        ).pack(side=tk.LEFT, padx=10)

        ttk.Button(
            button_frame,
            text="VOLVER",
            command=self.volver
        ).pack(side=tk.RIGHT, padx=10)
    
    def create_form_fields(self, parent):
        """Crea todos los campos del formulario con mejor organización."""
        # Definir los campos del formulario
        fields = [
            ("Nombre:", "nombre_entry", 0),
            ("Apellidos:", "apellidos_entry", 1),
            ("Cédula:", "cedula_entry", 2),
            ("Teléfono:", "telefono_entry", 3),
            ("Motivo de Visita:", "motivo_entry", 4),
            ("Responsable de Ingreso:", "responsable_entry", 5)
        ]
        
        # Crear los campos
        for i, (label_text, entry_name, row) in enumerate(fields):
            ttk.Label(parent, text=label_text).grid(
                row=row+1, column=0, padx=5, pady=5, sticky=tk.W
            )
            
            # Campo más ancho para motivo de visita
            width = 40 if entry_name == "motivo_entry" else 20
            
            entry = ttk.Entry(parent, width=width)
            entry.grid(row=row+1, column=1, padx=5, pady=5, sticky=tk.EW)
            
            # Guardar referencia al campo
            setattr(self, entry_name, entry)
        
        # Campo de fecha con valor predeterminado (hoy)
        ttk.Label(parent, text="Fecha de Ingreso:").grid(
            row=6, column=0, padx=5, pady=5, sticky=tk.W
        )
        self.fecha_entry = ttk.Entry(parent)
        self.fecha_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.EW)
        self.fecha_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # Campo para la foto
        ttk.Label(parent, text="Foto Visitante:").grid(
            row=7, column=0, padx=5, pady=5, sticky=tk.W
        )
        
        photo_frame = ttk.Frame(parent)
        photo_frame.grid(row=7, column=1, padx=5, pady=5, sticky=tk.EW)
        
        self.foto_entry = ttk.Entry(photo_frame, textvariable=self.foto_path)
        self.foto_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        ttk.Button(
            photo_frame, 
            text="Examinar...", 
            command=self.cargar_foto
        ).pack(side=tk.RIGHT, padx=5)
        
        # Configurar expansión de columnas
        parent.columnconfigure(1, weight=1)

    def cargar_foto(self):
        """Abre un cuadro de diálogo para seleccionar la foto y guarda la ruta."""
        ruta_foto = fd.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.gif")]
        )
        if ruta_foto:
            self.foto_path.set(ruta_foto)

    def limpiar_campos(self):
        """Limpia todos los campos del formulario."""
        fields = [
            self.nombre_entry,
            self.apellidos_entry,
            self.cedula_entry,
            self.telefono_entry,
            self.motivo_entry,
            self.responsable_entry,
            self.foto_entry
        ]
        
        for field in fields:
            field.delete(0, tk.END)
        
        # Restaurar fecha actual
        self.fecha_entry.delete(0, tk.END)
        self.fecha_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # Devolver foco al primer campo
        self.nombre_entry.focus_set()

    def volver(self):
        """Cierra la ventana actual y regresa a la anterior."""
        self.destroy()

    def registrar_datos(self):
        """Recopila los datos de los campos y los inserta en la tabla 'visitantes'."""
        # Recopilamos datos
        try:
            nombre = self.nombre_entry.get().strip()
            apellidos = self.apellidos_entry.get().strip()
            cedula = self.cedula_entry.get().strip()
            telefono = self.telefono_entry.get().strip()
            motivo = self.motivo_entry.get().strip()
            fecha_ingreso = self.fecha_entry.get().strip()
            responsable_ingreso = self.responsable_entry.get().strip()
            foto_visitante = self.foto_path.get().strip()

            # Validación sencilla
            if not nombre or not apellidos or not cedula:
                messagebox.showwarning("Atención", "Faltan datos obligatorios (Nombre, Apellidos o Cédula).")
                return
            
            # Depuración
            print(f"Intentando registrar visitante: {nombre} {apellidos} - Cédula: {cedula}")
            
            # Usar la función adecuada según esté disponible
            try:
                # Intentar usar la nueva función (con manager de contexto)
                print("Usando get_connection()")
                with get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO visitantes 
                        (nombre, apellidos, cedula, telefono, motivo_visita, fecha_ingreso, responsable_ingreso, foto_visitante)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        nombre, 
                        apellidos, 
                        cedula, 
                        telefono, 
                        motivo, 
                        fecha_ingreso, 
                        responsable_ingreso, 
                        foto_visitante
                    ))
                    # CORRECCIÓN: Commit explícito necesario
                    conn.commit()
                    print("Commit realizado exitosamente con get_connection()")
                    
            except NameError:
                # Usar la función original si la nueva no está disponible
                print("Usando create_connection()")
                conn = create_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute('''
                        INSERT INTO visitantes 
                        (nombre, apellidos, cedula, telefono, motivo_visita, fecha_ingreso, responsable_ingreso, foto_visitante)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        nombre, 
                        apellidos, 
                        cedula, 
                        telefono, 
                        motivo, 
                        fecha_ingreso, 
                        responsable_ingreso, 
                        foto_visitante
                    ))
                    conn.commit()
                    print("Commit realizado exitosamente con create_connection()")
                finally:
                    conn.close()
            
            # Verificar que se guardó correctamente
            self.verificar_registro(cedula)
                    
            # Registro exitoso
            logger.info(f"Visitante registrado: {nombre} {apellidos} - Cédula: {cedula}")
            messagebox.showinfo("Éxito", "Visitante registrado correctamente.")
            self.limpiar_campos()

        except Exception as e:
            logger.error(f"Error al registrar visitante: {e}")
            messagebox.showerror("Error", f"Ocurrió un error al registrar el visitante:\n{e}")
            
    def verificar_registro(self, cedula):
        """Verifica que el registro se haya guardado correctamente."""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT cedula, nombre, apellidos FROM visitantes WHERE cedula = ?", (cedula,))
                resultado = cursor.fetchone()
                
                if resultado:
                    print(f"¡Verificación exitosa! Visitante encontrado en la base de datos: {dict(resultado)}")
                else:
                    print(f"¡ERROR! No se encontró el visitante recién registrado con cédula {cedula}")
        except Exception as e:
            print(f"Error en la verificación: {e}")