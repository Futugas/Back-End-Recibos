from flask import Blueprint, request, jsonify
from app import db
from app.models import Consumo

consumo_bp = Blueprint('consumo', __name__)

@consumo_bp.route('', methods=['GET'])
def get_consumos():
    consumos = Consumo.query.all()
    return jsonify([c.to_dict() for c in consumos]), 200

@consumo_bp.route('/<int:id>', methods=['GET'])
def get_consumo(id):
    consumo = Consumo.query.get_or_404(id)
    return jsonify(consumo.to_dict()), 200

@consumo_bp.route('', methods=['POST'])
def create_consumo():
    data = request.get_json()

    if not data or not data.get('recibo_id'):
        return jsonify({'error': 'El recibo_id es requerido'}), 400

    consumo = Consumo(
        recibo_id=data.get('recibo_id'),
        lectura_inicial=data.get('lectura_inicial'),
        lectura_final=data.get('lectura_final'),
        dias_consumo=data.get('dias_consumo'),
        consumo_m3=data.get('consumo_m3'),
        factor_conversion=data.get('factor_conversion'),
        litros_consumidos=data.get('litros_consumidos'),
        precio_litro=data.get('precio_litro'),
        consumo_mes=data.get('consumo_mes')
    )

    try:
        db.session.add(consumo)
        db.session.commit()
        return jsonify(consumo.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@consumo_bp.route('/<int:id>', methods=['PUT'])
def update_consumo(id):
    consumo = Consumo.query.get_or_404(id)
    data = request.get_json()

    for key in ['recibo_id', 'lectura_inicial', 'lectura_final', 'dias_consumo', 
                'consumo_m3', 'factor_conversion', 'litros_consumidos', 
                'precio_litro', 'consumo_mes']:
        if key in data:
            setattr(consumo, key, data[key])

    try:
        db.session.commit()
        return jsonify(consumo.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@consumo_bp.route('/<int:id>', methods=['DELETE'])
def delete_consumo(id):
    consumo = Consumo.query.get_or_404(id)

    try:
        db.session.delete(consumo)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
