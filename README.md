# Sistema de Control de Acceso FNO

Este es un software de escritorio desarrollado en Python con Tkinter para gestionar el control de acceso de personal, visitantes y vehículos. La aplicación permite registrar, buscar y visualizar información detallada, incluyendo fotografías, de cada entidad.

## Características

- **Registro de Personal:** Permite registrar nuevos empleados o miembros del personal, almacenando datos como nombre, cédula, dependencia, licencia de conducción y una fotografía.
- **Registro de Vehículos:** Facilita el registro de vehículos, guardando información como placa, marca, modelo, color, SOAT, revisión técnico-mecánica y una foto del vehículo.
- **Registro de Visitantes:** Permite registrar la entrada de visitantes, almacenando sus datos personales, motivo de la visita y la persona responsable de su ingreso.
- **Panel de Búsqueda:** Un panel centralizado para buscar registros por diferentes criterios:
  - **Personal:** por cédula o apellido.
  - **Visitantes:** por cédula o fecha de ingreso.
  - **Vehículos:** por placa o marca.
- **Visualización de Información:** Muestra los detalles completos de cada registro, incluyendo la fotografía asociada.
- **Base de Datos Local:** Utiliza SQLite3 para almacenar toda la información de forma local, creando un archivo `control_acceso.db` en el directorio del proyecto.

## Tecnologías Utilizadas

- **Lenguaje:** Python 3
- **Interfaz Gráfica:** Tkinter (a través de la biblioteca estándar de Python)
- **Base de Datos:** SQLite3
- **Manejo de Imágenes:** Pillow (PIL)
- **Empaquetado:** PyInstaller para generar el ejecutable.

## Instalación y Uso

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/yahb03/control-fno.git
    cd control-fno
    ```

2.  **Crear un entorno virtual e instalar dependencias:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Ejecutar la aplicación:**
    ```bash
    python main.py
    ```
    Al ejecutar la aplicación por primera vez, se creará automáticamente la base de datos `control_acceso.db`.

## Compilación

El proyecto está configurado con GitHub Actions para compilar automáticamente un ejecutable `.exe` para Windows cada vez que se realiza un `push` a la rama `main`. El ejecutable se puede descargar desde la sección "Artifacts" de la acción correspondiente en el repositorio de GitHub.

Para compilar manualmente, puedes usar PyInstaller:
```bash
pyinstaller --onefile main.py
```

## Estructura del Proyecto

```
.
├── main.py                # Punto de entrada de la aplicación
├── auth.py                # (Módulo de autenticación, si aplica)
├── database.py            # Lógica de la base de datos (SQLite)
├── requirements.txt       # Dependencias de Python
├── views/                 # Módulos de la interfaz de usuario (ventanas)
│   ├── gui_principal.py
│   ├── gui_registro_personas.py
│   └── ...
├── assets/                # Recursos como imágenes y logos
├── .github/workflows/     # Flujos de trabajo de GitHub Actions
└── ...
```

## Desarrollado por

Este software fue desarrollado por **Kwaltas**.
