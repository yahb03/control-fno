# views/gui_principal.py

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import logging

# Importación compatible con ambas versiones
try:
    from database import create_connection, get_connection, DATABASE_PATH
except ImportError:
    from database import create_connection

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger('principal')

from utils.ui import BaseWindow

class PrincipalWindow(BaseWindow):
    def __init__(self, master, title, geometry):
        super().__init__(master, title, geometry)
        self.cargar_imagen_por_defecto()
        self.mostrar_resultado("Seleccione una pestaña y realice una búsqueda.", "black")

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            main_frame,
            text="Panel de Control y Búsqueda",
            font=("Helvetica", 16, "bold")
        ).grid(row=0, column=0, columnspan=4, pady=10, sticky=tk.W)

        try:
            db_info = f"Base de datos: {os.path.abspath(DATABASE_PATH)}"
            ttk.Label(
                main_frame,
                text=db_info,
                font=("Helvetica", 9),
                foreground="gray"
            ).grid(row=0, column=3, pady=5, sticky=tk.E)
        except:
            pass

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=10)

        personal_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(personal_frame, text="Personal")
        self.crear_tab_personal(personal_frame)

        visitantes_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(visitantes_frame, text="Visitantes")
        self.crear_tab_visitantes(visitantes_frame)

        vehiculos_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(vehiculos_frame, text="Vehículos")
        self.crear_tab_vehiculos(vehiculos_frame)

        results_container = ttk.Frame(main_frame)
        results_container.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=10)
        results_container.columnconfigure(0, weight=3)
        results_container.columnconfigure(1, weight=2)

        self.text_panel = ttk.LabelFrame(results_container, text="Información", padding=10)
        self.text_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        self.result_text = tk.Text(self.text_panel, height=8, width=50, wrap=tk.WORD)
        self.result_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5)
        self.result_text.config(state=tk.DISABLED)

        self.image_panel = ttk.LabelFrame(results_container, text="Fotografía", padding=10)
        self.image_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        self.image_label = ttk.Label(self.image_panel)
        self.image_label.pack(fill=tk.BOTH, expand=True, pady=5)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10, sticky="ew")

        ttk.Button(
            button_frame,
            text="Diagnosticar Base de Datos",
            command=self.diagnosticar_db
        ).pack(side=tk.LEFT, padx=10)

        ttk.Button(
            button_frame,
            text="Volver al Menú Principal",
            command=self.volver
        ).pack(side=tk.RIGHT, padx=10)

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
    
    def configurar_estilos(self):
        """Configura estilos personalizados para widgets."""
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 10))
        style.configure("TButton", font=("Helvetica", 10))
        style.configure("TEntry", font=("Helvetica", 10))
        style.configure("Heading.TLabel", font=("Helvetica", 12, "bold"))
        style.configure("TLabelframe", borderwidth=2)
        style.configure("TLabelframe.Label", font=("Helvetica", 10, "bold"))
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def crear_tab_personal(self, parent):
        """Crea la pestaña de búsqueda de personal."""
        # Búsqueda por cédula
        ttk.Label(parent, text="Cédula:").grid(row=0, column=0, padx=5, pady=10, sticky=tk.W)
        self.cedula_personal_entry = ttk.Entry(parent, width=20)
        self.cedula_personal_entry.grid(row=0, column=1, padx=5, pady=10, sticky=tk.W)
        
        ttk.Button(
            parent,
            text="Buscar",
            command=self.buscar_por_cedula
        ).grid(row=0, column=2, padx=5, pady=10)
        
        # Opciones adicionales de búsqueda
        ttk.Label(parent, text="Apellido:").grid(row=1, column=0, padx=5, pady=10, sticky=tk.W)
        self.apellido_personal_entry = ttk.Entry(parent, width=20)
        self.apellido_personal_entry.grid(row=1, column=1, padx=5, pady=10, sticky=tk.W)
        
        ttk.Button(
            parent,
            text="Buscar por Apellido",
            command=self.buscar_por_apellido_personal
        ).grid(row=1, column=2, padx=5, pady=10)
    
    def crear_tab_visitantes(self, parent):
        """Crea la pestaña de búsqueda de visitantes."""
        # Búsqueda por cédula
        ttk.Label(parent, text="Cédula:").grid(row=0, column=0, padx=5, pady=10, sticky=tk.W)
        self.cedula_visitante_entry = ttk.Entry(parent, width=20)
        self.cedula_visitante_entry.grid(row=0, column=1, padx=5, pady=10, sticky=tk.W)
        
        ttk.Button(
            parent,
            text="Buscar",
            command=self.buscar_visitante
        ).grid(row=0, column=2, padx=5, pady=10)
        
        # Búsqueda por fecha
        ttk.Label(parent, text="Fecha (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=10, sticky=tk.W)
        self.fecha_visitante_entry = ttk.Entry(parent, width=20)
        self.fecha_visitante_entry.grid(row=1, column=1, padx=5, pady=10, sticky=tk.W)
        
        ttk.Button(
            parent,
            text="Buscar por Fecha",
            command=self.buscar_por_fecha_visitante
        ).grid(row=1, column=2, padx=5, pady=10)
    
    def crear_tab_vehiculos(self, parent):
        """Crea la pestaña de búsqueda de vehículos."""
        # Búsqueda por placa
        ttk.Label(parent, text="Placa:").grid(row=0, column=0, padx=5, pady=10, sticky=tk.W)
        self.placa_entry = ttk.Entry(parent, width=20)
        self.placa_entry.grid(row=0, column=1, padx=5, pady=10, sticky=tk.W)
        
        ttk.Button(
            parent,
            text="Buscar",
            command=self.buscar_por_placa
        ).grid(row=0, column=2, padx=5, pady=10)
        
        # Búsqueda por marca
        ttk.Label(parent, text="Marca:").grid(row=1, column=0, padx=5, pady=10, sticky=tk.W)
        self.marca_entry = ttk.Entry(parent, width=20)
        self.marca_entry.grid(row=1, column=1, padx=5, pady=10, sticky=tk.W)
        
        ttk.Button(
            parent,
            text="Buscar por Marca",
            command=self.buscar_por_marca
        ).grid(row=1, column=2, padx=5, pady=10)

    def mostrar_resultado(self, texto, color="blue"):
        """Muestra el resultado en el área de texto."""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, texto)
        self.result_text.tag_configure("color", foreground=color)
        self.result_text.tag_add("color", 1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        
        # Asegurar que el texto sea visible cambiando el título del panel
        if color == "red":
            self.text_panel.configure(text="Información - Sin resultados")
        else:
            self.text_panel.configure(text="Información")

    def buscar_por_cedula(self):
        """Busca un usuario en la base de datos por su cédula."""
        cedula = self.cedula_personal_entry.get().strip()
        
        if not cedula:
            self.mostrar_resultado("Por favor ingresa una cédula.", "red")
            self.cargar_imagen_por_defecto()
            return
        
        try:
            print(f"\n--- Buscando persona con cédula: {cedula} ---")
            
            # Intentar usar el administrador de contexto
            try:
                with get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT id, grado, nombre, apellidos, cedula, dependencia, telefono, 
                               licencia_conduccion, vigencia_licencia, foto_persona, fecha_registro
                        FROM usuarios
                        WHERE cedula = ?
                    """, (cedula,))
                    result = cursor.fetchone()
            except NameError:
                # Usar la conexión tradicional
                conn = create_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        SELECT id, grado, nombre, apellidos, cedula, dependencia, telefono, 
                               licencia_conduccion, vigencia_licencia, foto_persona, fecha_registro
                        FROM usuarios
                        WHERE cedula = ?
                    """, (cedula,))
                    result = cursor.fetchone()
                finally:
                    conn.close()
            
            if result:
                # Convertir a diccionario para fácil acceso
                if isinstance(result, dict):
                    resultado = result
                else:
                    # Si es una tupla o Row, convertir a diccionario
                    try:
                        resultado = dict(result)
                    except:
                        # Crear manualmente el diccionario
                        campos = ["id", "grado", "nombre", "apellidos", "cedula", "dependencia", 
                                  "telefono", "licencia_conduccion", "vigencia_licencia", 
                                  "foto_persona", "fecha_registro"]
                        resultado = {campos[i]: result[i] for i in range(min(len(campos), len(result)))}
                
                print(f"Persona encontrada: {resultado}")
                
                # Formatear texto con toda la información disponible
                texto = (
                    f"INFORMACIÓN DEL PERSONAL\n"
                    f"========================\n"
                    f"ID: {resultado.get('id', 'N/A')}\n"
                    f"Grado: {resultado.get('grado', 'N/A')}\n"
                    f"Nombre completo: {resultado.get('nombre', 'N/A')} {resultado.get('apellidos', 'N/A')}\n"
                    f"Cédula: {resultado.get('cedula', 'N/A')}\n"
                    f"Dependencia: {resultado.get('dependencia', 'N/A')}\n"
                    f"Teléfono: {resultado.get('telefono', 'N/A')}\n"
                    f"Licencia de conducción: {resultado.get('licencia_conduccion', 'N/A')}\n"
                    f"Vigencia licencia: {resultado.get('vigencia_licencia', 'N/A')}\n"
                    f"Registro: {resultado.get('fecha_registro', 'N/A')}\n"
                )
                
                # Actualizar la interfaz
                self.mostrar_resultado(texto, "blue")
                self.mostrar_imagen(resultado.get('foto_persona'))
                self.image_panel.configure(text=f"Fotografía - Personal: {resultado.get('nombre', '')} {resultado.get('apellidos', '')}")
                
                logger.info(f"Búsqueda de personal exitosa para cédula: {cedula}")
            else:
                self.mostrar_resultado(f"No se encontró ningún usuario con la cédula {cedula}.", "red")
                self.cargar_imagen_por_defecto()
                self.image_panel.configure(text="Fotografía - Sin resultados")
                logger.info(f"Búsqueda sin resultados para cédula: {cedula}")
                
        except Exception as e:
            print(f"Error en búsqueda: {e}")
            self.mostrar_resultado(f"Error al buscar en la base de datos: {str(e)}", "red")
            self.cargar_imagen_por_defecto()
            self.image_panel.configure(text="Fotografía - Error")
            logger.error(f"Error en búsqueda de personal: {e}")
    
    def buscar_por_apellido_personal(self):
        """Busca usuarios por apellido."""
        apellido = self.apellido_personal_entry.get().strip()
        
        if not apellido:
            self.mostrar_resultado("Por favor ingresa un apellido.", "red")
            self.cargar_imagen_por_defecto()
            return
        
        try:
            print(f"\n--- Buscando personas con apellido: {apellido} ---")
            
            # Intentar usar el administrador de contexto
            try:
                with get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT id, grado, nombre, apellidos, cedula, dependencia, telefono
                        FROM usuarios
                        WHERE apellidos LIKE ?
                        ORDER BY apellidos, nombre
                    """, (f"%{apellido}%",))
                    results = cursor.fetchall()
            except NameError:
                # Usar la conexión tradicional
                conn = create_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        SELECT id, grado, nombre, apellidos, cedula, dependencia, telefono
                        FROM usuarios
                        WHERE apellidos LIKE ?
                        ORDER BY apellidos, nombre
                    """, (f"%{apellido}%",))
                    results = cursor.fetchall()
                finally:
                    conn.close()
            
            if results:
                texto = f"PERSONAL CON APELLIDO: '{apellido}'\n"
                texto += "===============================\n\n"
                texto += f"Se encontraron {len(results)} usuarios:\n\n"
                
                for i, result in enumerate(results):
                    # Convertir resultado a diccionario si es posible
                    try:
                        user = dict(result)
                    except:
                        # Crear manualmente el diccionario
                        campos = ["id", "grado", "nombre", "apellidos", "cedula", "dependencia", "telefono"]
                        user = {campos[i]: result[i] for i in range(min(len(campos), len(result)))}
                    
                    texto += f"{i+1}. {user.get('grado', '')} {user.get('apellidos', '')}, {user.get('nombre', '')}\n"
                    texto += f"   Cédula: {user.get('cedula', 'N/A')}\n"
                    texto += f"   Dependencia: {user.get('dependencia', 'N/A')}\n"
                    texto += f"   Teléfono: {user.get('telefono', 'N/A')}\n\n"
                
                self.mostrar_resultado(texto, "blue")
                self.cargar_imagen_por_defecto()
                self.image_panel.configure(text=f"Fotografía - Listado de personal")
                logger.info(f"Búsqueda por apellido exitosa para: {apellido}")
            else:
                self.mostrar_resultado(f"No se encontraron usuarios con apellidos que contengan '{apellido}'.", "red")
                self.cargar_imagen_por_defecto()
                self.image_panel.configure(text="Fotografía - Sin resultados")
                logger.info(f"Búsqueda por apellido sin resultados para: {apellido}")
                
        except Exception as e:
            print(f"Error en búsqueda: {e}")
            self.mostrar_resultado(f"Error al buscar en la base de datos: {str(e)}", "red")
            self.cargar_imagen_por_defecto()
            self.image_panel.configure(text="Fotografía - Error")
            logger.error(f"Error en búsqueda por apellido: {e}")
    
    def buscar_visitante(self):
        """Busca un visitante en la base de datos por su cédula."""
        cedula = self.cedula_visitante_entry.get().strip()
        
        if not cedula:
            self.mostrar_resultado("Por favor ingresa una cédula.", "red")
            self.cargar_imagen_por_defecto()
            return
        
        try:
            print(f"\n--- Buscando visitante con cédula: {cedula} ---")
            
            # Intentar usar el administrador de contexto
            try:
                with get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT id, nombre, apellidos, cedula, telefono, motivo_visita, 
                               fecha_ingreso, hora_salida, responsable_ingreso, foto_visitante
                        FROM visitantes
                        WHERE cedula = ?
                    """, (cedula,))
                    result = cursor.fetchone()
            except NameError:
                # Usar la conexión tradicional
                conn = create_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        SELECT id, nombre, apellidos, cedula, telefono, motivo_visita, 
                               fecha_ingreso, hora_salida, responsable_ingreso, foto_visitante
                        FROM visitantes
                        WHERE cedula = ?
                    """, (cedula,))
                    result = cursor.fetchone()
                finally:
                    conn.close()
            
            if result:
                # Convertir a diccionario para fácil acceso
                try:
                    resultado = dict(result)
                except:
                    # Crear manualmente el diccionario
                    campos = ["id", "nombre", "apellidos", "cedula", "telefono", "motivo_visita", 
                              "fecha_ingreso", "hora_salida", "responsable_ingreso", "foto_visitante"]
                    resultado = {campos[i]: result[i] for i in range(min(len(campos), len(result)))}
                
                print(f"Visitante encontrado: {resultado}")
                
                texto = (
                    f"INFORMACIÓN DEL VISITANTE\n"
                    f"========================\n"
                    f"ID: {resultado.get('id', 'N/A')}\n"
                    f"Nombre completo: {resultado.get('nombre', 'N/A')} {resultado.get('apellidos', 'N/A')}\n"
                    f"Cédula: {resultado.get('cedula', 'N/A')}\n"
                    f"Teléfono: {resultado.get('telefono', 'N/A')}\n"
                    f"Motivo de visita: {resultado.get('motivo_visita', 'N/A')}\n"
                    f"Fecha de ingreso: {resultado.get('fecha_ingreso', 'N/A')}\n"
                    f"Hora de salida: {resultado.get('hora_salida', 'No registrada')}\n"
                    f"Responsable de ingreso: {resultado.get('responsable_ingreso', 'N/A')}\n"
                )
                
                self.mostrar_resultado(texto, "blue")
                self.mostrar_imagen(resultado.get('foto_visitante'))
                self.image_panel.configure(text=f"Fotografía - Visitante: {resultado.get('nombre', '')} {resultado.get('apellidos', '')}")
                logger.info(f"Búsqueda de visitante exitosa para cédula: {cedula}")
            else:
                self.mostrar_resultado(f"No se encontró ningún visitante con la cédula {cedula}.", "red")
                self.cargar_imagen_por_defecto()
                self.image_panel.configure(text="Fotografía - Sin resultados")
                logger.info(f"Búsqueda de visitante sin resultados para cédula: {cedula}")
                
        except Exception as e:
            print(f"Error en búsqueda: {e}")
            self.mostrar_resultado(f"Error al buscar en la base de datos: {str(e)}", "red")
            self.cargar_imagen_por_defecto()
            self.image_panel.configure(text="Fotografía - Error")
            logger.error(f"Error en búsqueda de visitante: {e}")
    
    def buscar_por_fecha_visitante(self):
        """Busca visitantes por fecha de ingreso."""
        fecha = self.fecha_visitante_entry.get().strip()
        
        if not fecha:
            self.mostrar_resultado("Por favor ingresa una fecha (YYYY-MM-DD).", "red")
            self.cargar_imagen_por_defecto()
            return
        
        try:
            print(f"\n--- Buscando visitantes por fecha: {fecha} ---")
            
            # Intentar usar el administrador de contexto
            try:
                with get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT id, nombre, apellidos, cedula, fecha_ingreso, motivo_visita, responsable_ingreso
                        FROM visitantes
                        WHERE fecha_ingreso LIKE ?
                        ORDER BY fecha_ingreso DESC
                    """, (f"{fecha}%",))
                    results = cursor.fetchall()
            except NameError:
                # Usar la conexión tradicional
                conn = create_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        SELECT id, nombre, apellidos, cedula, fecha_ingreso, motivo_visita, responsable_ingreso
                        FROM visitantes
                        WHERE fecha_ingreso LIKE ?
                        ORDER BY fecha_ingreso DESC
                    """, (f"{fecha}%",))
                    results = cursor.fetchall()
                finally:
                    conn.close()
            
            if results:
                texto = f"VISITANTES EN FECHA: {fecha}\n"
                texto += "==============================\n\n"
                texto += f"Se encontraron {len(results)} visitantes:\n\n"
                
                for i, result in enumerate(results):
                    try:
                        visitante = dict(result) 
                    except:
                        campos = ["id", "nombre", "apellidos", "cedula", "fecha_ingreso", "motivo_visita", "responsable_ingreso"]
                        visitante = {campos[i]: result[i] for i in range(min(len(campos), len(result)))}
                    
                    texto += f"{i+1}. {visitante.get('nombre', '')} {visitante.get('apellidos', '')}\n"
                    texto += f"   Cédula: {visitante.get('cedula', 'N/A')}\n"
                    texto += f"   Ingreso: {visitante.get('fecha_ingreso', 'N/A')}\n"
                    texto += f"   Motivo: {visitante.get('motivo_visita', 'N/A')}\n"
                    texto += f"   Responsable: {visitante.get('responsable_ingreso', 'N/A')}\n\n"
                
                self.mostrar_resultado(texto, "blue")
                self.cargar_imagen_por_defecto()
                self.image_panel.configure(text=f"Fotografía - Listado de visitantes")
                logger.info(f"Búsqueda por fecha exitosa para: {fecha}")
            else:
                self.mostrar_resultado(f"No se encontraron visitantes en la fecha {fecha}.", "red")
                self.cargar_imagen_por_defecto()
                self.image_panel.configure(text="Fotografía - Sin resultados")
                logger.info(f"Búsqueda por fecha sin resultados para: {fecha}")
                
        except Exception as e:
            print(f"Error en búsqueda: {e}")
            self.mostrar_resultado(f"Error al buscar en la base de datos: {str(e)}", "red")
            self.cargar_imagen_por_defecto()
            self.image_panel.configure(text="Fotografía - Error")
            logger.error(f"Error en búsqueda por fecha: {e}")
    
    def buscar_por_placa(self):
        """Busca un vehículo en la base de datos por su placa."""
        placa = self.placa_entry.get().strip().upper()
        
        if not placa:
            self.mostrar_resultado("Por favor ingresa una placa.", "red")
            self.cargar_imagen_por_defecto()
            return
        
        try:
            print(f"\n--- Buscando vehículo con placa: {placa} ---")
            
            # Intentar usar el administrador de contexto
            try:
                with get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT id, placa, marca, modelo, color, tipo, licencia_transito, 
                               componente_vehiculo, responsable_vehiculo, vigencia_soat, 
                               vigencia_revision, foto_vehiculo, fecha_registro
                        FROM vehiculos
                        WHERE placa = ?
                    """, (placa,))
                    result = cursor.fetchone()
            except NameError:
                # Usar la conexión tradicional
                conn = create_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        SELECT id, placa, marca, modelo, color, tipo, licencia_transito, 
                               componente_vehiculo, responsable_vehiculo, vigencia_soat, 
                               vigencia_revision, foto_vehiculo, fecha_registro
                        FROM vehiculos
                        WHERE placa = ?
                    """, (placa,))
                    result = cursor.fetchone()
                finally:
                    conn.close()
            
            if result:
                # Convertir a diccionario para fácil acceso
                try:
                    resultado = dict(result)
                except:
                    campos = ["id", "placa", "marca", "modelo", "color", "tipo", "licencia_transito", 
                              "componente_vehiculo", "responsable_vehiculo", "vigencia_soat", 
                              "vigencia_revision", "foto_vehiculo", "fecha_registro"]
                    resultado = {campos[i]: result[i] for i in range(min(len(campos), len(result)))}
                
                print(f"Vehículo encontrado: {resultado}")
                
                texto = (
                 
                    f"INFORMACIÓN DEL VEHÍCULO\n"
                    f"========================\n"
                    f"ID: {resultado.get('id', 'N/A')}\n"
                    f"Placa: {resultado.get('placa', 'N/A')}\n"
                    f"Marca: {resultado.get('marca', 'N/A')}\n"
                    f"Modelo: {resultado.get('modelo', 'N/A')}\n"
                    f"Color: {resultado.get('color', 'N/A')}\n"
                    f"Tipo: {resultado.get('tipo', 'N/A')}\n"
                    f"Licencia de tránsito: {resultado.get('licencia_transito', 'N/A')}\n"
                    f"Componente: {resultado.get('componente_vehiculo', 'N/A')}\n"
                    f"Responsable: {resultado.get('responsable_vehiculo', 'N/A')}\n"
                    f"Vigencia SOAT: {resultado.get('vigencia_soat', 'N/A')}\n"
                    f"Vigencia revisión: {resultado.get('vigencia_revision', 'N/A')}\n"
                    f"Registro: {resultado.get('fecha_registro', 'N/A')}"
                )
                
                self.mostrar_resultado(texto, "blue")
                self.mostrar_imagen(resultado.get('foto_vehiculo'))
                self.image_panel.configure(text=f"Fotografía - Vehículo: {resultado.get('placa')} ({resultado.get('marca')})")
                logger.info(f"Búsqueda de vehículo exitosa para placa: {placa}")
            else:
                self.mostrar_resultado(f"No se encontró ningún vehículo con la placa {placa}.", "red")
                self.cargar_imagen_por_defecto()
                self.image_panel.configure(text="Fotografía - Sin resultados")
                logger.info(f"Búsqueda de vehículo sin resultados para placa: {placa}")
                
        except Exception as e:
            print(f"Error en búsqueda: {e}")
            self.mostrar_resultado(f"Error al buscar en la base de datos: {str(e)}", "red")
            self.cargar_imagen_por_defecto()
            self.image_panel.configure(text="Fotografía - Error")
            logger.error(f"Error en búsqueda de vehículo: {e}")
    
    def buscar_por_marca(self):
        """Busca vehículos por marca."""
        marca = self.marca_entry.get().strip()
        
        if not marca:
            self.mostrar_resultado("Por favor ingresa una marca.", "red")
            self.cargar_imagen_por_defecto()
            return
        
        try:
            print(f"\n--- Buscando vehículos por marca: {marca} ---")
            
            # Intentar usar el administrador de contexto
            try:
                with get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT id, placa, marca, modelo, color, tipo, responsable_vehiculo
                        FROM vehiculos
                        WHERE marca LIKE ?
                        ORDER BY marca, modelo
                    """, (f"%{marca}%",))
                    results = cursor.fetchall()
            except NameError:
                # Usar la conexión tradicional
                conn = create_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        SELECT id, placa, marca, modelo, color, tipo, responsable_vehiculo
                        FROM vehiculos
                        WHERE marca LIKE ?
                        ORDER BY marca, modelo
                    """, (f"%{marca}%",))
                    results = cursor.fetchall()
                finally:
                    conn.close()
            
            if results:
                texto = f"VEHÍCULOS DE MARCA: '{marca}'\n"
                texto += "============================\n\n"
                texto += f"Se encontraron {len(results)} vehículos:\n\n"
                
                for i, result in enumerate(results):
                    try:
                        vehiculo = dict(result)
                    except:
                        campos = ["id", "placa", "marca", "modelo", "color", "tipo", "responsable_vehiculo"]
                        vehiculo = {campos[i]: result[i] for i in range(min(len(campos), len(result)))}
                    
                    texto += f"{i+1}. {vehiculo.get('marca', '')} {vehiculo.get('modelo', 'N/A')}\n"
                    texto += f"   Placa: {vehiculo.get('placa', 'N/A')}\n"
                    texto += f"   Color: {vehiculo.get('color', 'N/A')}\n"
                    texto += f"   Tipo: {vehiculo.get('tipo', 'N/A')}\n"
                    texto += f"   Responsable: {vehiculo.get('responsable_vehiculo', 'N/A')}\n\n"
                
                self.mostrar_resultado(texto, "blue")
                self.cargar_imagen_por_defecto()
                self.image_panel.configure(text=f"Fotografía - Listado de vehículos")
                logger.info(f"Búsqueda por marca exitosa para: {marca}")
            else:
                self.mostrar_resultado(f"No se encontraron vehículos de marca similar a '{marca}'.", "red")
                self.cargar_imagen_por_defecto()
                self.image_panel.configure(text="Fotografía - Sin resultados")
                logger.info(f"Búsqueda por marca sin resultados para: {marca}")
                
        except Exception as e:
            print(f"Error en búsqueda: {e}")
            self.mostrar_resultado(f"Error al buscar en la base de datos: {str(e)}", "red")
            self.cargar_imagen_por_defecto()
            self.image_panel.configure(text="Fotografía - Error")
            logger.error(f"Error en búsqueda por marca: {e}")
    
    def mostrar_imagen(self, foto_path):
        """Muestra la imagen (persona, visitante o vehículo) en la interfaz."""
        if foto_path and os.path.exists(foto_path):
            try:
                # Carga la imagen en la ruta dada
                img = Image.open(foto_path)
                
                # Redimensiona la imagen manteniendo la proporción
                img.thumbnail((300, 300))  # Tamaño más grande para mejor visualización
                img_tk = ImageTk.PhotoImage(img)
                
                self.image_label.config(image=img_tk)
                # Mantener una referencia para evitar que el GC la elimine
                self.image_label.image = img_tk
                
            except Exception as e:
                logger.error(f"Error al cargar imagen {foto_path}: {e}")
                self.cargar_imagen_por_defecto()
        else:
            # Si no hay imagen o la ruta no existe, mostrar la imagen por defecto
            self.cargar_imagen_por_defecto()
    
    def cargar_imagen_por_defecto(self):
        """Carga una imagen por defecto cuando no hay una disponible."""
        # Ruta a la imagen por defecto
        default_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "sin_foto.png")
        
        try:
            if os.path.exists(default_path):
                img = Image.open(default_path)
                img.thumbnail((250, 250))
                img_tk = ImageTk.PhotoImage(img)
                
                self.image_label.config(image=img_tk)
                self.image_label.image = img_tk
            else:
                # Si no existe la imagen por defecto, mostrar un mensaje
                self.image_label.config(image='', text="Sin imagen disponible")
                self.image_label.image = None
        except Exception as e:
            logger.error(f"Error al cargar imagen por defecto: {e}")
            self.image_label.config(image='', text="Error al cargar imagen")
            self.image_label.image = None
    
    def diagnosticar_db(self):
        """Función para diagnosticar el estado de la base de datos."""
        try:
            mensaje = "Diagnóstico de la Base de Datos\n"
            mensaje += "=============================\n\n"
            
            # Obtener ruta de la base de datos
            try:
                mensaje += f"Ruta: {os.path.abspath(DATABASE_PATH)}\n"
                mensaje += f"Tamaño: {os.path.getsize(DATABASE_PATH) / 1024:.2f} KB\n\n"
            except:
                mensaje += "No se pudo determinar la ruta o tamaño de la base de datos.\n\n"
            
            # Obtener tablas y registros
            try:
                with get_connection() as conn:
                    cursor = conn.cursor()
                    
                    # Listar tablas
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tablas = cursor.fetchall()
                    
                    mensaje += "Tablas encontradas:\n"
                    
                    for tabla in tablas:
                        nombre_tabla = tabla[0]
                        cursor.execute(f"SELECT COUNT(*) FROM {nombre_tabla}")
                        count = cursor.fetchone()[0]
                        
                        mensaje += f"- {nombre_tabla}: {count} registros\n"
            except Exception as e:
                mensaje += f"Error al consultar tablas: {e}\n"
            
            # Mostrar el diagnóstico
            self.mostrar_resultado(mensaje, "black")
            
        except Exception as e:
            self.mostrar_resultado(f"Error en el diagnóstico: {str(e)}", "red")
            logger.error(f"Error en diagnóstico de base de datos: {e}")
    
    def volver(self):
        """Cierra la ventana y regresa a la ventana principal."""
        try:
            self.grab_release()  # Libera el modo modal
            self.destroy()
        except Exception as e:
            logger.error(f"Error al cerrar ventana: {e}")