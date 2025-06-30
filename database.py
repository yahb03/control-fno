import sqlite3
import os
import logging
from contextlib import contextmanager
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='database.log'
)
logger = logging.getLogger('database')

# Constante para el nombre de la base de datos (con ruta absoluta)
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "control_acceso.db")

def create_connection():
    """
    Función de compatibilidad para mantener el código existente funcionando.
    Retorna la conexión a la base de datos.
    """
    logger.info(f"Conectando a la base de datos en: {os.path.abspath(DATABASE_PATH)}")
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def get_connection():
    """
    Administrador de contexto para manejar conexiones a la base de datos.
    Garantiza que las conexiones se cierren correctamente incluso si hay excepciones.
    """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        # Habilitar claves foráneas
        conn.execute("PRAGMA foreign_keys = ON")
        # Convertir filas a diccionarios
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Error de conexión a la base de datos: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def backup_database():
    """Crea una copia de seguridad de la base de datos actual."""
    if not os.path.exists(DATABASE_PATH):
        logger.warning("No se puede hacer backup: la base de datos no existe")
        return False
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups")
    backup_path = os.path.join(backup_dir, f"control_acceso_{timestamp}.db")
    
    # Asegurar que exista el directorio de backups
    os.makedirs(backup_dir, exist_ok=True)
    
    try:
        # Copia de seguridad usando la API de SQLite
        with get_connection() as conn:
            backup_conn = sqlite3.connect(backup_path)
            conn.backup(backup_conn)
            backup_conn.close()
        logger.info(f"Backup creado exitosamente: {backup_path}")
        return True
    except sqlite3.Error as e:
        logger.error(f"Error al crear backup: {e}")
        return False

def create_tables():
    """Crea las tablas en la base de datos si no existen."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Definiciones de tablas (SQL mejorado y corregido)
            tables = [
                '''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    grado TEXT,
                    nombre TEXT NOT NULL,
                    apellidos TEXT NOT NULL,
                    cedula TEXT UNIQUE NOT NULL,
                    dependencia TEXT,
                    telefono TEXT,
                    licencia_conduccion TEXT,
                    vigencia_licencia TEXT,
                    foto_persona TEXT,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                ''',
                '''
                CREATE TABLE IF NOT EXISTS vehiculos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    placa TEXT UNIQUE NOT NULL,
                    marca TEXT NOT NULL,
                    modelo TEXT,
                    color TEXT,
                    tipo TEXT,
                    licencia_transito TEXT,
                    componente_vehiculo TEXT,
                    responsable_vehiculo TEXT,
                    vigencia_soat TEXT,
                    vigencia_revision TEXT,
                    foto_vehiculo TEXT,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                ''',
                '''
                CREATE TABLE IF NOT EXISTS visitantes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellidos TEXT NOT NULL,
                    cedula TEXT UNIQUE NOT NULL,
                    telefono TEXT,
                    motivo_visita TEXT,
                    fecha_ingreso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    hora_salida TIMESTAMP,
                    responsable_ingreso TEXT,
                    foto_visitante TEXT
                )
                ''',
                '''
                CREATE TABLE IF NOT EXISTS historial_acceso (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo_entidad TEXT NOT NULL,
                    entidad_id INTEGER NOT NULL,
                    fecha_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_salida TIMESTAMP,
                    observaciones TEXT
                )
                '''
            ]
            
            # Ejecutar las consultas de creación de tablas
            for table_sql in tables:
                cursor.execute(table_sql)
            
            # Confirmar los cambios
            conn.commit()
            logger.info("Tablas creadas exitosamente")
            
    except sqlite3.Error as e:
        logger.error(f"Error al crear tablas: {e}")
        raise

def execute_query(query, params=None, fetch=False):
    """
    Ejecuta una consulta SQL y opcionalmente devuelve los resultados.
    
    Args:
        query (str): Consulta SQL a ejecutar
        params (tuple, optional): Parámetros para la consulta
        fetch (bool, optional): Si es True, devuelve los resultados
        
    Returns:
        list/None: Resultados de la consulta si fetch=True, None en caso contrario
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            if fetch:
                return cursor.fetchall()
            else:
                conn.commit()
                return cursor.lastrowid
                
    except sqlite3.Error as e:
        logger.error(f"Error en la consulta: {query} - Error: {e}")
        raise

def get_by_id(table, id):
    """Obtiene un registro por su ID."""
    query = f"SELECT * FROM {table} WHERE id = ?"
    results = execute_query(query, (id,), fetch=True)
    return dict(results[0]) if results else None

def diagnosticar_base_datos():
    """Función de diagnóstico para verificar el estado de la base de datos."""
    try:
        print(f"Ruta de la base de datos: {os.path.abspath(DATABASE_PATH)}")
        
        # Verificar si existe el archivo
        if not os.path.exists(DATABASE_PATH):
            print("La base de datos NO existe en la ruta especificada.")
            return
        
        print(f"La base de datos existe. Tamaño: {os.path.getsize(DATABASE_PATH) / 1024:.2f} KB")
        
        # Conectar y examinar
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Obtener lista de tablas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tablas = cursor.fetchall()
            
            print("\nTablas en la base de datos:")
            for tabla in tablas:
                nombre_tabla = tabla[0]
                print(f"- {nombre_tabla}")
                
                # Contar registros
                cursor.execute(f"SELECT COUNT(*) FROM {nombre_tabla}")
                count = cursor.fetchone()[0]
                print(f"  Registros: {count}")
                
                # Ver estructura
                cursor.execute(f"PRAGMA table_info({nombre_tabla})")
                columnas = cursor.fetchall()
                print(f"  Columnas: {', '.join(col[1] for col in columnas)}")
                
                # Mostrar algunos registros si existen
                if count > 0:
                    cursor.execute(f"SELECT * FROM {nombre_tabla} LIMIT 2")
                    registros = cursor.fetchall()
                    for reg in registros:
                        print(f"  Muestra: {dict(reg)}")
    
    except Exception as e:
        print(f"Error en diagnóstico: {e}")

def initialize_database():
    """Inicializa la base de datos y crea una copia de seguridad si existe."""
    if os.path.exists(DATABASE_PATH):
        backup_database()
    create_tables()

if __name__ == "__main__":
    initialize_database()
    # Ejecutar diagnóstico
    diagnosticar_base_datos()