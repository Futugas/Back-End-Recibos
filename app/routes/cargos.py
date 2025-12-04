from flask import Blueprint, request, jsonify
from app import db
from app.models import Cargo

cargos_bp = Blueprint('cargos', __name__)

@cargos_bp.route('', methods=['GET'])
def get_cargos():
    cargos = Cargo.query.all()
    return jsonify([c.to_dict() for c in cargos]), 200

@cargos_bp.route('/<int:id>', methods=['GET'])
def get_cargo(id):
    cargo = Cargo.query.get_or_404(id)
    return jsonify(cargo.to_dict()), 200

@cargos_bp.route('', methods=['POST'])
def create_cargo():
    data = request.get_json()

    if not data or not data.get('recibo_id'):
        return jsonify({'error': 'El recibo_id es requerido'}), 400

    cargo = Cargo(
        recibo_id=data.get('recibo_id'),
        descripcion=data.get('descripcion'),
        importe=data.get('importe')
    )

    try:
        db.session.add(cargo)
        db.session.commit()
        return jsonify(cargo.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cargos_bp.route('/<int:id>', methods=['PUT'])
def update_cargo(id):
    cargo = Cargo.query.get_or_404(id)
    data = request.get_json()

    cargo.recibo_id = data.get('recibo_id', cargo.recibo_id)
    cargo.descripcion = data.get('descripcion', cargo.descripcion)
    cargo.importe = data.get('importe', cargo.importe)

    try:
        db.session.commit()
        return jsonify(cargo.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cargos_bp.route('/<int:id>', methods=['DELETE'])
def delete_cargo(id):
    cargo = Cargo.query.get_or_404(id)

    try:
        db.session.delete(cargo)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500