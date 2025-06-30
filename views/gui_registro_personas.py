# views/gui_registro_personas.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
import re
import logging
from datetime import datetime

# Importación compatible con ambas versiones
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
logger = logging.getLogger('personas')

from utils.ui import BaseWindow

class RegistroWindow(BaseWindow):
    def __init__(self, master, title, geometry):
        super().__init__(master, title, geometry)
        self.foto_persona_path = ""
        self.directorio_imagenes = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "imagenes_personas")
        if not os.path.exists(self.directorio_imagenes):
            try:
                os.makedirs(self.directorio_imagenes)
                logger.info(f"Directorio de imágenes creado: {self.directorio_imagenes}")
            except Exception as e:
                logger.error(f"Error al crear directorio de imágenes: {e}")
        self.grado_entry.focus_set()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            main_frame,
            text="Registro de Personal",
            font=("Helvetica", 14, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=10, sticky=tk.W)

        self.crear_formulario(main_frame)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=12, column=0, columnspan=2, pady=20, sticky=tk.EW)

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
    
    def configurar_estilos(self):
        """Configura estilos personalizados para widgets."""
        style = ttk.Style()
        
        # Estilo para botones de acción primaria
        style.configure(
            "Accent.TButton",
            background="#4CAF50",
            foreground="white",
            font=("Helvetica", 10, "bold")
        )
        
        # Mejorar otros estilos
        style.configure("TLabel", font=("Helvetica", 10))
        style.configure("TEntry", font=("Helvetica", 10))
    
    def crear_formulario(self, parent):
        """Crea todos los campos del formulario con mejor organización."""
        # Definición de campos
        campos = [
            ("GRADO:", "grado_entry", 1),
            ("NOMBRE:", "nombre_entry", 2),
            ("APELLIDOS:", "apellidos_entry", 3),
            ("CÉDULA:", "cedula_entry", 4),
            ("DEPENDENCIA:", "dependencia_entry", 5),
            ("TELÉFONO:", "telefono_entry", 6),
            ("LICENCIA CONDUCCIÓN:", "licencia_cond_entry", 7),
            ("VIGENCIA LICENCIA:", "vigencia_lic_entry", 8)
        ]
        
        # Crear los campos
        for etiqueta, nombre_campo, fila in campos:
            ttk.Label(parent, text=etiqueta).grid(
                row=fila, column=0, padx=5, pady=5, sticky=tk.E
            )
            
            entry = ttk.Entry(parent, width=30)
            entry.grid(row=fila, column=1, padx=5, pady=5, sticky=tk.W)
            
            # Guardar referencia al campo
            setattr(self, nombre_campo, entry)
        
        # Campo para foto de la persona
        ttk.Label(parent, text="FOTO DEL PERSONAL:").grid(
            row=9, column=0, padx=5, pady=5, sticky=tk.E
        )
        
        photo_frame = ttk.Frame(parent)
        photo_frame.grid(row=9, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.label_foto_persona = ttk.Label(
            photo_frame, 
            text="No seleccionado",
            foreground="red"
        )
        self.label_foto_persona.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            photo_frame,
            text="Seleccionar foto",
            command=self.cargar_foto_persona
        ).pack(side=tk.LEFT)
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def cargar_foto_persona(self):
        """Abre un cuadro de diálogo para seleccionar una foto de la persona."""
        try:
            # Asegurar que la ventana tenga el foco
            self.lift()
            self.focus_force()
            
            # Abrir diálogo para seleccionar archivo
            ruta = filedialog.askopenfilename(
                parent=self,
                title="Seleccionar Foto del Personal", 
                filetypes=[
                    ("Imágenes", "*.jpg *.jpeg *.png *.gif"),
                    ("Todos los archivos", "*.*")
                ]
            )

            if ruta:
                # Validar la imagen
                valida, mensaje = self.validar_imagen(ruta)
                if not valida:
                    messagebox.showwarning("Imagen inválida", mensaje)
                    return
                
                self.foto_persona_path = ruta
                self.label_foto_persona.config(
                    text=f"✓ {os.path.basename(ruta)}",
                    foreground="green"
                )
            
        except Exception as e:
            logger.error(f"Error al cargar foto: {e}")
            messagebox.showerror("Error", f"Error al cargar la foto: {str(e)}")

    def validar_imagen(self, ruta):
        """Valida que el archivo sea una imagen válida y no sea demasiado grande."""
        try:
            # Verificar que el archivo existe
            if not os.path.exists(ruta):
                return False, "El archivo no existe."
            
            # Verificar tamaño (máximo 5MB)
            tamaño = os.path.getsize(ruta)
            if tamaño > 5 * 1024 * 1024:
                return False, "La imagen es demasiado grande (máximo 5MB)"
            
            # Verificar extensión
            ext = os.path.splitext(ruta)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
                return False, "El archivo no es una imagen válida."
            
            return True, ""
            
        except Exception as e:
            logger.error(f"Error al validar imagen: {e}")
            return False, f"Error al validar la imagen: {str(e)}"

    def copiar_imagen(self, ruta_origen, cedula):
        """Copia la imagen a una carpeta del programa y devuelve la nueva ruta."""
        try:
            # Crear nombre único basado en cédula y timestamp
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            _, extension = os.path.splitext(ruta_origen)
            nuevo_nombre = f"{cedula}_{timestamp}{extension}"
            ruta_destino = os.path.join(self.directorio_imagenes, nuevo_nombre)
            
            # Copiar archivo
            shutil.copy2(ruta_origen, ruta_destino)
            logger.info(f"Imagen copiada: {ruta_destino}")
            
            return ruta_destino
            
        except Exception as e:
            logger.error(f"Error al copiar imagen: {e}")
            raise Exception(f"Error al copiar la imagen: {str(e)}")

    def registrar_datos(self):
        """Registra los datos de la persona en la base de datos."""
        try:
            # Obtener datos de los campos
            grado = self.grado_entry.get().strip()
            nombre = self.nombre_entry.get().strip()
            apellidos = self.apellidos_entry.get().strip()
            cedula = self.cedula_entry.get().strip()
            dependencia = self.dependencia_entry.get().strip()
            telefono = self.telefono_entry.get().strip()
            licencia_cond = self.licencia_cond_entry.get().strip()
            vigencia_lic = self.vigencia_lic_entry.get().strip()

            # Validar campos requeridos
            campos_requeridos = [
                ("NOMBRE", nombre),
                ("APELLIDOS", apellidos),
                ("CÉDULA", cedula)
            ]
            
            for campo, valor in campos_requeridos:
                if not valor:
                    messagebox.showwarning("Campos incompletos", f"El campo {campo} es obligatorio.")
                    return

            # Validar formato de cédula (solo números)
            if not cedula.isdigit():
                messagebox.showwarning(
                    "Formato incorrecto", 
                    "La cédula debe contener solo números."
                )
                return

            # Verificar la foto de la persona
            if not self.foto_persona_path:
                messagebox.showwarning("Advertencia", "Por favor selecciona una foto de la persona.")
                return
            
            # Depuración
            print(f"Intentando registrar persona: {nombre} {apellidos} - Cédula: {cedula}")
            
            # Usar el administrador de contexto si está disponible
            try:
                # Intentar usar la nueva función
                print("Usando get_connection()")
                with get_connection() as conn:
                    cursor = conn.cursor()
                    
                    # Verificar si la cédula ya existe
                    cursor.execute("SELECT cedula FROM usuarios WHERE cedula = ?", (cedula,))
                    if cursor.fetchone():
                        messagebox.showwarning("Duplicado", f"Ya existe una persona registrada con la cédula {cedula}.")
                        return
                    
                    # Copiar la imagen
                    nueva_ruta_imagen = self.copiar_imagen(self.foto_persona_path, cedula)
                    
                    # Insertar en la base de datos
                    cursor.execute("""
                        INSERT INTO usuarios (
                            grado, nombre, apellidos, cedula, dependencia, 
                            telefono, licencia_conduccion, vigencia_licencia, foto_persona
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        grado, nombre, apellidos, cedula, dependencia, 
                        telefono, licencia_cond, vigencia_lic, nueva_ruta_imagen
                    ))
                    
                    # CORRECCIÓN: Commit explícito necesario
                    conn.commit()
                    print("Commit realizado exitosamente con get_connection()")
                    
            except NameError:
                # Usar la función original
                print("Usando create_connection()")
                conn = create_connection()
                cursor = conn.cursor()
                
                try:
                    # Verificar si la cédula ya existe
                    cursor.execute("SELECT cedula FROM usuarios WHERE cedula = ?", (cedula,))
                    if cursor.fetchone():
                        messagebox.showwarning("Duplicado", f"Ya existe una persona registrada con la cédula {cedula}.")
                        conn.close()
                        return
                    
                    # Copiar la imagen
                    nueva_ruta_imagen = self.copiar_imagen(self.foto_persona_path, cedula)
                    
                    # Insertar en la base de datos
                    cursor.execute("""
                        INSERT INTO usuarios (
                            grado, nombre, apellidos, cedula, dependencia, 
                            telefono, licencia_conduccion, vigencia_licencia, foto_persona
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        grado, nombre, apellidos, cedula, dependencia, 
                        telefono, licencia_cond, vigencia_lic, nueva_ruta_imagen
                    ))
                    
                    conn.commit()
                    print("Commit realizado exitosamente con create_connection()")
                finally:
                    conn.close()
            
            logger.info(f"Persona registrada: {nombre} {apellidos} - Cédula: {cedula}")
            messagebox.showinfo("Éxito", f"Persona con cédula {cedula} registrada con éxito.")
            
            # Verificar que se guardó correctamente
            self.verificar_registro(cedula)
            
            # Limpiar los campos después de registrar
            self.limpiar_campos()
            
        except Exception as e:
            logger.error(f"Error al registrar persona: {e}")
            messagebox.showerror("Error", f"Error al registrar la persona: {str(e)}")
    
    def verificar_registro(self, cedula):
        """Verifica que el registro se haya guardado correctamente."""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT cedula, nombre, apellidos FROM usuarios WHERE cedula = ?", (cedula,))
                resultado = cursor.fetchone()
                
                if resultado:
                    print(f"¡Verificación exitosa! Usuario encontrado en la base de datos: {dict(resultado)}")
                else:
                    print(f"¡ERROR! No se encontró el usuario recién registrado con cédula {cedula}")
        except Exception as e:
            print(f"Error en la verificación: {e}")

    def limpiar_campos(self):
        """Limpia todos los campos del formulario."""
        campos = [
            self.grado_entry,
            self.nombre_entry,
            self.apellidos_entry,
            self.cedula_entry,
            self.dependencia_entry,
            self.telefono_entry,
            self.licencia_cond_entry,
            self.vigencia_lic_entry
        ]
        
        for campo in campos:
            campo.delete(0, tk.END)
        
        self.foto_persona_path = ""
        self.label_foto_persona.config(text="No seleccionado", foreground="red")
        
        # Devolver el foco al primer campo
        self.grado_entry.focus_set()

    def volver(self):
        """Cierra la ventana de registro y regresa a la ventana principal."""
        try:
            self.grab_release()  # Libera el modo modal
            self.destroy()
        except Exception as e:
            logger.error(f"Error al cerrar ventana: {e}")