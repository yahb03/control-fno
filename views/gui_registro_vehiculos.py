import tkinter as tk
from tkinter import messagebox, filedialog
import os
import shutil
from database import create_connection

class RegistroWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Registro de Vehículo")
        self.protocol("WM_DELETE_WINDOW", self.volver)  # Manejo seguro del cierre de ventana
        
        # Configuración de la ventana
        self.resizable(False, False)
        self.configure(padx=10, pady=10)
        
        # Variables para almacenar las rutas de las fotos
        self.foto_vehiculo_path = ""

        # --- Datos del Vehículo ---
        tk.Label(self, text="PLACA:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.placa_entry = tk.Entry(self)
        self.placa_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="MARCA:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.marca_entry = tk.Entry(self)
        self.marca_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="MODELO:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.modelo_entry = tk.Entry(self)
        self.modelo_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="COLOR:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.color_entry = tk.Entry(self)
        self.color_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="TIPO DE VEHÍCULO:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.tipo_entry = tk.Entry(self)
        self.tipo_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="LICENCIA DE TRÁNSITO:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.licencia_transito_entry = tk.Entry(self)
        self.licencia_transito_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="COMPONENTE DEL VEHÍCULO:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.componente_vehiculo_entry = tk.Entry(self)
        self.componente_vehiculo_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="RESPONSABLE DEL VEHÍCULO:").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.responsable_vehiculo_entry = tk.Entry(self)
        self.responsable_vehiculo_entry.grid(row=7, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="VIGENCIA SOAT:").grid(row=8, column=0, padx=5, pady=5, sticky="e")
        self.vigencia_soat_entry = tk.Entry(self)
        self.vigencia_soat_entry.grid(row=8, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="VIGENCIA REVISIÓN:").grid(row=9, column=0, padx=5, pady=5, sticky="e")
        self.vigencia_revision_entry = tk.Entry(self)
        self.vigencia_revision_entry.grid(row=9, column=1, padx=5, pady=5, sticky="w")

        # --- Botón para cargar foto del vehículo ---
        self.btn_cargar_foto = tk.Button(self, text="Cargar Foto Vehículo", command=self.cargar_foto_vehiculo)
        self.btn_cargar_foto.grid(row=10, column=0, columnspan=2, pady=5)
        
        self.label_foto_vehiculo = tk.Label(self, text="No seleccionado", fg="red")
        self.label_foto_vehiculo.grid(row=11, column=0, columnspan=2, pady=5)

        # --- Botones de acción: Registrar y Volver ---
        self.btn_registrar = tk.Button(self, text="REGISTRAR", command=self.registrar_datos, bg="#4CAF50", fg="white")
        self.btn_registrar.grid(row=12, column=0, padx=5, pady=10)
        
        self.btn_volver = tk.Button(self, text="VOLVER", command=self.volver, bg="#f44336", fg="white")
        self.btn_volver.grid(row=12, column=1, padx=5, pady=10)
        
        # Asegurar que la aplicación no se cierre inesperadamente
        self.grab_set()  # Hace que esta ventana sea modal
        
        # Crear directorio para imágenes si no existe
        self.directorio_imagenes = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagenes_vehiculos")
        if not os.path.exists(self.directorio_imagenes):
            try:
                os.makedirs(self.directorio_imagenes)
            except Exception as e:
                print(f"Error al crear directorio de imágenes: {e}")

    def cargar_foto_vehiculo(self):
        """Abre un cuadro de diálogo para seleccionar una foto del vehículo."""
        try:
            # Asegurar que la ventana tenga el foco antes de abrir el diálogo
            self.lift()
            self.focus_force()
            
            # Guardar referencia a la ventana actual para evitar que se cierre
            self.update()
            
            # FIX: Separar cada tipo de archivo correctamente para macOS
            ruta = filedialog.askopenfilename(
                parent=self,  # Especifica el padre explícitamente
                title="Seleccionar Foto Vehículo", 
                filetypes=[
                    ("JPEG", "*.jpg"),
                    ("JPEG", "*.jpeg"),
                    ("PNG", "*.png"),
                    ("GIF", "*.gif"),
                    ("Todos los archivos", "*.*")
                ]
            )

            if ruta:  # Asegura que el usuario seleccionó un archivo
                # Validar la imagen
                valida, mensaje = self.validar_imagen(ruta)
                if not valida:
                    messagebox.showwarning("Imagen inválida", mensaje)
                    return
                
                self.foto_vehiculo_path = ruta
                self.label_foto_vehiculo.config(
                    text=f"Foto seleccionada: {os.path.basename(ruta)}", 
                    fg="green"
                )
            else:
                # Solo mostrar advertencia si se canceló explícitamente
                if self.foto_vehiculo_path == "":  # Solo si no había una foto seleccionada antes
                    messagebox.showinfo("Información", "No se seleccionó ninguna foto.")
        except Exception as e:
            # Captura cualquier excepción y muestra un mensaje
            messagebox.showerror("Error", f"Error al cargar la foto: {str(e)}")
            print(f"Error en cargar_foto_vehiculo: {str(e)}")

    def validar_imagen(self, ruta):
        """Valida que el archivo sea una imagen válida y no sea demasiado grande."""
        try:
            # Verificar que el archivo existe
            if not os.path.exists(ruta):
                return False, "El archivo no existe."
            
            # Verificar tamaño (ejemplo: no más de 5MB)
            tamaño = os.path.getsize(ruta)
            if tamaño > 5 * 1024 * 1024:  # 5MB
                return False, "La imagen es demasiado grande (máximo 5MB)"
            
            # Verificar que es una imagen válida
            # Para una validación más estricta, puedes usar PIL
            ext = os.path.splitext(ruta)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
                return False, "El archivo no es una imagen válida."
            
            return True, ""
        except Exception as e:
            return False, f"Error al validar la imagen: {str(e)}"

    def copiar_imagen(self, ruta_origen, placa):
        """Copia la imagen a una carpeta del programa y devuelve la nueva ruta."""
        try:
            # Obtener extensión y crear nuevo nombre de archivo basado en la placa
            _, extension = os.path.splitext(ruta_origen)
            nuevo_nombre = f"{placa}{extension}"
            ruta_destino = os.path.join(self.directorio_imagenes, nuevo_nombre)
            
            # Copiar archivo
            shutil.copy2(ruta_origen, ruta_destino)
            
            return ruta_destino
        except Exception as e:
            raise Exception(f"Error al copiar la imagen: {str(e)}")

    def registrar_datos(self):
        """Registra los datos del vehículo en la base de datos."""
        try:
            # Obtener datos de los campos
            placa = self.placa_entry.get().strip().upper()
            marca = self.marca_entry.get().strip()
            modelo = self.modelo_entry.get().strip()
            color = self.color_entry.get().strip()
            tipo = self.tipo_entry.get().strip()
            licencia_transito = self.licencia_transito_entry.get().strip()
            componente_vehiculo = self.componente_vehiculo_entry.get().strip()
            responsable_vehiculo = self.responsable_vehiculo_entry.get().strip()
            vigencia_soat = self.vigencia_soat_entry.get().strip()
            vigencia_revision = self.vigencia_revision_entry.get().strip()

            # Validar campos requeridos
            campos_requeridos = [
                ("PLACA", placa),
                ("MARCA", marca),
                ("MODELO", modelo),
                ("COLOR", color),
                ("TIPO DE VEHÍCULO", tipo),
                ("LICENCIA DE TRÁNSITO", licencia_transito),
                ("RESPONSABLE DEL VEHÍCULO", responsable_vehiculo),
                ("VIGENCIA SOAT", vigencia_soat),
                ("VIGENCIA REVISIÓN", vigencia_revision)
            ]
            
            for campo, valor in campos_requeridos:
                if not valor:
                    messagebox.showwarning("Campos incompletos", f"El campo {campo} es obligatorio.")
                    return

          
            # Validar formato de placa (aceptando dos formatos)
                import re
                if not (re.match(r'^[A-Z]{3}\d{3}$', placa) or re.match(r'^[A-Z]{3}\d{2}[A-Z]$', placa)):
                    messagebox.showwarning(
                        "Formato incorrecto", 
                        "La placa debe tener formato de 3 letras seguidas de 3 números (ej: ABC123) o 3 letras, 2 números y 1 letra (ej: ABC12D)."
                    )
                    return

            # Verifica si la foto del vehículo ha sido seleccionada
            if not self.foto_vehiculo_path:
                messagebox.showwarning("Advertencia", "Por favor selecciona una foto del vehículo.")
                return
            
            # Establecer conexión con la base de datos
            conn = create_connection()
            if not conn:
                messagebox.showerror("Error de conexión", "No se pudo conectar a la base de datos.")
                return
                
            cursor = conn.cursor()
            
            # Verificar si la placa ya existe
            cursor.execute("SELECT placa FROM vehiculos WHERE placa = ?", (placa,))
            if cursor.fetchone():
                messagebox.showwarning("Duplicado", f"Ya existe un vehículo registrado con la placa {placa}.")
                conn.close()
                return
            
            # Copiar la imagen a la carpeta del programa
            nueva_ruta_imagen = self.copiar_imagen(self.foto_vehiculo_path, placa)
            
            # Insertar en la base de datos
            cursor.execute("""
                INSERT INTO vehiculos (
                    placa, marca, modelo, color, tipo, 
                    licencia_transito, componente_vehiculo, responsable_vehiculo, 
                    vigencia_soat, vigencia_revision, foto_vehiculo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                placa, marca, modelo, color, tipo, 
                licencia_transito, componente_vehiculo, responsable_vehiculo, 
                vigencia_soat, vigencia_revision, nueva_ruta_imagen
            ))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Éxito", f"Vehículo con placa {placa} registrado con éxito.")
            
            # Limpiar los campos después de registrar
            self.limpiar_campos()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar el vehículo: {str(e)}")
            print(f"Error en registrar_datos: {str(e)}")

    def limpiar_campos(self):
        """Limpia todos los campos del formulario."""
        self.placa_entry.delete(0, tk.END)
        self.marca_entry.delete(0, tk.END)
        self.modelo_entry.delete(0, tk.END)
        self.color_entry.delete(0, tk.END)
        self.tipo_entry.delete(0, tk.END)
        self.licencia_transito_entry.delete(0, tk.END)
        self.componente_vehiculo_entry.delete(0, tk.END)
        self.responsable_vehiculo_entry.delete(0, tk.END)
        self.vigencia_soat_entry.delete(0, tk.END)
        self.vigencia_revision_entry.delete(0, tk.END)
        self.foto_vehiculo_path = ""
        self.label_foto_vehiculo.config(text="No seleccionado", fg="red")

    def volver(self):
        """Cierra la ventana de registro y regresa a la ventana principal."""
        try:
            self.grab_release()  # Libera el modo modal
            self.destroy()
            if self.master:
                self.master.deiconify()  # Asegura que la ventana principal se muestre
        except Exception as e:
            print(f"Error al cerrar la ventana: {str(e)}")