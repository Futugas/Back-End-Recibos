# Proyecto Backend - Python Flask

Este proyecto es una aplicación backend desarrollada con Python y Flask.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente en tu sistema:

- **Python** (versión 3.8 o superior recomendada)
- **pip** (gestor de paquetes de Python, incluido con Python)
- **virtualenv** o **venv** (para crear entornos virtuales)

Puedes verificar las versiones instaladas ejecutando:

```bash
python --version
pip --version
```

## Instalación

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_PROYECTO>
```

### 2. Crear un entorno virtual

Es altamente recomendable usar un entorno virtual para aislar las dependencias del proyecto.

**En Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**En macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

Deberías ver `(venv)` al inicio de tu línea de comandos, indicando que el entorno virtual está activo.

### 3. Instalar dependencias

Con el entorno virtual activado, instala todas las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

Este comando instalará Flask y todas las bibliotecas necesarias listadas en el archivo `requirements.txt`.

### 4. Configurar variables de entorno (opcional)

Si el proyecto requiere variables de entorno, crea un archivo `.env` en la raíz del proyecto:

```bash
touch .env
```

Ejemplo de contenido del archivo `.env`:

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=tu_clave_secreta_aqui
DATABASE_URL=sqlite:///database.db
```

Para cargar automáticamente las variables de entorno, asegúrate de tener instalado `python-dotenv`:

```bash
pip install python-dotenv
```

## Ejecución del Proyecto

### Modo Desarrollo

Para levantar el servidor de desarrollo de Flask, ejecuta:

```bash
flask run
```

O también puedes usar:

```bash
python run.py
```

El servidor se ejecutará por defecto en `http://127.0.0.1:5000/` o `http://localhost:5000/`.

### Opciones adicionales de ejecución

Para ejecutar en un puerto específico:

```bash
flask run --port 8000
```

Para permitir conexiones externas (útil para pruebas en red local):

```bash
flask run --host=0.0.0.0
```

Para habilitar el modo debug (recarga automática y mensajes de error detallados):

```bash
flask run --debug
```

O configura la variable de entorno:

```bash
export FLASK_ENV=development  # macOS/Linux
set FLASK_ENV=development     # Windows
flask run
```

## Estructura del Proyecto

```
├── app.py                # Punto de entrada principal de la aplicación
├── requirements.txt      # Lista de dependencias del proyecto
├── .env                  # Variables de entorno (no incluir en git)
├── config.py             # Configuraciones de la aplicación
├── models/               # Modelos de base de datos
├── routes/               # Rutas/endpoints de la API
├── services/             # Lógica de negocio
├── utils/                # Funciones auxiliares
├── static/               # Archivos estáticos (CSS, JS, imágenes)
├── templates/            # Plantillas HTML (si se usa renderizado del lado del servidor)
└── tests/                # Pruebas unitarias e integración
```

## Comandos Útiles

| Comando | Descripción |
|---------|-------------|
| `pip install -r requirements.txt` | Instala todas las dependencias |
| `flask run` | Inicia el servidor de desarrollo |
| `flask run --debug` | Inicia el servidor en modo debug |
| `pip freeze > requirements.txt` | Actualiza el archivo de dependencias |
| `python -m pytest` | Ejecuta las pruebas (si usa pytest) |
| `deactivate` | Desactiva el entorno virtual |

## Migraciones de Base de Datos (si usa Flask-Migrate)

Si el proyecto utiliza Flask-Migrate para manejar migraciones de base de datos:

```bash
# Inicializar migraciones (solo la primera vez)
flask db init

# Crear una nueva migración
flask db migrate -m "Descripción de los cambios"

# Aplicar las migraciones
flask db upgrade
```

## Ejecución de Pruebas

Si el proyecto incluye pruebas unitarias con pytest:

```bash
pip install pytest
pytest
```

O con unittest (biblioteca estándar de Python):

```bash
python -m unittest discover tests
```

## Solución de Problemas

### Error: "flask: command not found"

Asegúrate de que el entorno virtual esté activado y Flask esté instalado:

```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install flask
```

### Error: "ModuleNotFoundError"

Verifica que todas las dependencias estén instaladas:

```bash
pip install -r requirements.txt
```

### Puerto en uso

Si el puerto 5000 está ocupado, especifica otro puerto:

```bash
flask run --port 8000
```

### Problemas con el entorno virtual

Si experimentas problemas, recrea el entorno virtual:

```bash
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Despliegue a Producción

Para desplegar en producción, se recomienda usar un servidor WSGI como Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

También puedes usar otros servidores como uWSGI o desplegar en plataformas como:
- Heroku
- AWS Elastic Beanstalk
- Google Cloud Run
- DigitalOcean App Platform

## Recursos Adicionales

- [Documentación oficial de Flask](https://flask.palletsprojects.com/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Guía de mejores prácticas de Flask](https://flask.palletsprojects.com/en/latest/patterns/)

## Soporte

Si encuentras algún problema o tienes preguntas, por favor abre un issue en el repositorio.