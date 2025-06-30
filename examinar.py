import sqlite3
import os

# Ruta a la base de datos (asegúrate de que sea la misma que estás usando en la aplicación)
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "control_acceso.db")
print(f"Examinando base de datos en: {db_path}")

# Verificar si el archivo existe
if not os.path.exists(db_path):
    print(f"¡ERROR! El archivo de base de datos no existe en: {db_path}")
    exit(1)

# Conectar a la base de datos
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Listar tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("\nTablas en la base de datos:")
for table in tables:
    table_name = table[0]
    print(f"\n- Tabla: {table_name}")
    
    # Mostrar estructura
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    print(f"  Columnas: {', '.join(col[1] for col in columns)}")
    
    # Contar registros
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"  Total de registros: {count}")
    
    # Mostrar algunos registros si hay
    if count > 0:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
        rows = cursor.fetchall()
        for i, row in enumerate(rows):
            print(f"  Registro {i+1}:")
            for col in columns:
                col_name = col[1]
                print(f"    {col_name}: {row[col_name]}")

conn.close()