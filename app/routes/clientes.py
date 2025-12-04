from flask import Blueprint, request, jsonify
from app import db
from app.models import Cliente

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('', methods=['GET'])
def get_clientes():
    """Obtener todos los clientes"""
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes]), 200

@clientes_bp.route('/<int:id>', methods=['GET'])
def get_cliente(id):
    """Obtener un cliente por ID"""
    cliente = Cliente.query.get_or_404(id)
    return jsonify(cliente.to_dict()), 200

@clientes_bp.route('', methods=['POST'])
def create_cliente():
    """Crear un nuevo cliente"""
    data = request.get_json()

    if not data or not data.get('nombre'):
        return jsonify({'error': 'El nombre es requerido'}), 400

    cliente = Cliente(
        nombre=data.get('nombre'),
        direccion=data.get('direccion'),
        referencia=data.get('referencia'),
        codigo_postal=data.get('codigo_postal')
    )

    try:
        db.session.add(cliente)
        db.session.commit()
        return jsonify(cliente.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@clientes_bp.route('/<int:id>', methods=['PUT'])
def update_cliente(id):
    """Actualizar un cliente"""
    cliente = Cliente.query.get_or_404(id)
    data = request.get_json()

    cliente.nombre = data.get('nombre', cliente.nombre)
    cliente.direccion = data.get('direccion', cliente.direccion)
    cliente.referencia = data.get('referencia', cliente.referencia)
    cliente.codigo_postal = data.get('codigo_postal', cliente.codigo_postal)

    try:
        db.session.commit()
        return jsonify(cliente.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@clientes_bp.route('/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    """Eliminar un cliente"""
    cliente = Cliente.query.get_or_404(id)

    try:
        db.session.delete(cliente)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@clientes_bp.route('/<int:id>/recibos', methods=['GET'])
def get_recibos_cliente(id):
    """Obtener todos los recibos de un cliente"""
    cliente = Cliente.query.get_or_404(id)
    return jsonify([r.to_dict() for r in cliente.recibos]), 200
