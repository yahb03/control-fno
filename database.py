import sqlite3

def create_connection():
    """Retorna la conexión a la base de datos (crea el archivo si no existe)."""
    return sqlite3.connect("control_acceso.db")

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grado TEXT,
            nombre TEXT,
            apellidos TEXT,
            cedula TEXT UNIQUE,
            dependencia TEXT,
            telefono TEXT,
            licencia_conduccion TEXT,
            vigencia_licencia TEXT,
            password TEXT,
            foto_persona TEXT
        );
    ''')

    # Tabla de vehiculos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT UNIQUE,
            marca TEXT,
            modelo TEXT,
            color TEXT,
            tipo TEXT,
            licencia_transito TEXT,
            componente_vehiculo TEXT,
            responsable_vehiculo TEXT,
            vigencia_soat TEXT,
            vigencia_revision TEXT,
            foto_vehiculo TEXT
        );
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()