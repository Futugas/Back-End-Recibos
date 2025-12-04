import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(app):
    """Configurar sistema de logging"""

    # Crear directorio de logs si no existe
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Configurar formato de logs
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    # Handler para archivo con rotación
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10240000,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Agregar handlers al logger de la app
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))

    # Log de inicio
    app.logger.info('='*50)
    app.logger.info(f'Aplicación iniciada en modo: {app.config["ENV"]}')
    app.logger.info(f'Nivel de log: {app.config["LOG_LEVEL"]}')
    app.logger.info('='*50)
