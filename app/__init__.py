from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    CORS(app, resources={
        r"/api/*": {
            "origins": "*",  # ← Cambio aquí
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Registrar blueprints existentes
    from app.routes.clientes import clientes_bp
    from app.routes.recibos import recibos_bp
    from app.routes.consumo import consumo_bp
    from app.routes.cargos import cargos_bp
    from app.routes.historico_consumo import historico_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(clientes_bp, url_prefix='/api/clientes')
    app.register_blueprint(recibos_bp, url_prefix='/api/recibos')
    app.register_blueprint(consumo_bp, url_prefix='/api/consumo')
    app.register_blueprint(cargos_bp, url_prefix='/api/cargos')
    app.register_blueprint(historico_bp, url_prefix='/api/historico-consumo')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app