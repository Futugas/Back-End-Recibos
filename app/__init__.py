from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    # Registrar blueprints
    from app.routes.clientes import clientes_bp
    from app.routes.recibos import recibos_bp
    from app.routes.consumo import consumo_bp
    from app.routes.cargos import cargos_bp
    from app.routes.historico_consumo import historico_bp

    app.register_blueprint(clientes_bp, url_prefix='/api/clientes')
    app.register_blueprint(recibos_bp, url_prefix='/api/recibos')
    app.register_blueprint(consumo_bp, url_prefix='/api/consumo')
    app.register_blueprint(cargos_bp, url_prefix='/api/cargos')
    app.register_blueprint(historico_bp, url_prefix='/api/historico-consumo')

    # Manejadores de errores
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Recurso no encontrado'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Error interno del servidor'}, 500

    return app
