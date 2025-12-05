from flask import Blueprint, request, jsonify
from app import db
from app.models.usuario import Usuario
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
import base64

bcrypt = Bcrypt()

auth_bp = Blueprint('auth', __name__)

def decode_password(encoded_password) -> str:
    """Decodifica la contraseña ofuscada"""
    try:
        decoded = base64.b64decode(encoded_password).decode('utf-8')
        salt = 'recibosApp2025_'
        password = decoded[len(salt):-len(salt)]
        return password
    except Exception as e:
        raise ValueError(f"Error al decodificar: {str(e)}")


# ============================================
#              REGISTRO
# ============================================
@auth_bp.post('/registrar')
def register():
    data = request.json
    nombre = data.get('nombre')
    email = data.get('email')
    encoded_password = data.get('password')

    if Usuario.query.filter_by(email=email).first():
        return jsonify({'error': 'El correo ya está registrado'}), 400

    try:
        password = decode_password(encoded_password)
    except Exception as _:
        return jsonify({'error': 'Error al procesar la contraseña '}), 400

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    user = Usuario(nombre=nombre, email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Usuario registrado correctamente'}), 201


# ============================================
#              LOGIN
# ============================================
@auth_bp.post('/iniciar-sesion')
def login():
    data = request.json or {}

    email = data.get('email')
    encoded_password = data.get('password')

    if not email or not encoded_password:
        return jsonify({
            "status": 400,
            "message": "Email y contraseña son obligatorios",
            "data": None
        }), 400

    try:
        password = decode_password(encoded_password)
    except Exception as _:
        return jsonify({
            "status": 400,
            "message": "Error al procesar la contraseña",
            "data": None
        }), 400

    user = Usuario.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({
            "status": 401,
            "message": "Credenciales incorrectas",
            "data": None
        }), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({
        "status": 200,
        "message": "Inicio de sesión exitoso",
        "data": {
            "token": token,
            "user": {
                "id": user.id,
                "nombre": user.nombre,
                "email": user.email
            }
        }
    }), 200
