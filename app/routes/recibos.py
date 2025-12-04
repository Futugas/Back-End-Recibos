from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import Recibo

recibos_bp = Blueprint('recibos', __name__)

@recibos_bp.route('', methods=['GET'])
def get_recibos():
    """Obtener todos los recibos"""
    recibos = Recibo.query.all()
    return jsonify([r.to_dict() for r in recibos]), 200

@recibos_bp.route('/<int:id>', methods=['GET'])
def get_recibo(id):
    """Obtener un recibo por ID"""
    recibo = Recibo.query.get_or_404(id)
    return jsonify(recibo.to_dict()), 200

@recibos_bp.route('', methods=['POST'])
def create_recibo():
    """Crear un nuevo recibo"""
    data = request.get_json()

    if not data or not data.get('cliente_id'):
        return jsonify({'error': 'El cliente_id es requerido'}), 400

    recibo = Recibo(
        cliente_id=data.get('cliente_id'),
        numero_recibo=data.get('numero_recibo'),
        fecha=datetime.strptime(data['fecha'], '%Y-%m-%d').date() if data.get('fecha') else None,
        periodo_inicio=datetime.strptime(data['periodo_inicio'], '%Y-%m-%d').date() if data.get('periodo_inicio') else None,
        periodo_fin=datetime.strptime(data['periodo_fin'], '%Y-%m-%d').date() if data.get('periodo_fin') else None,
        precio_autorizado=data.get('precio_autorizado'),
        precio_apoyo=data.get('precio_apoyo'),
        total_pagar=data.get('total_pagar'),
        banco=data.get('banco'),
        clabe=data.get('clabe'),
        concepto=data.get('concepto')
    )

    try:
        db.session.add(recibo)
        db.session.commit()
        return jsonify(recibo.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@recibos_bp.route('/<int:id>', methods=['PUT'])
def update_recibo(id):
    """Actualizar un recibo"""
    recibo = Recibo.query.get_or_404(id)
    data = request.get_json()

    if 'cliente_id' in data:
        recibo.cliente_id = data['cliente_id']
    if 'numero_recibo' in data:
        recibo.numero_recibo = data['numero_recibo']
    if 'fecha' in data:
        recibo.fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
    if 'periodo_inicio' in data:
        recibo.periodo_inicio = datetime.strptime(data['periodo_inicio'], '%Y-%m-%d').date()
    if 'periodo_fin' in data:
        recibo.periodo_fin = datetime.strptime(data['periodo_fin'], '%Y-%m-%d').date()
    if 'precio_autorizado' in data:
        recibo.precio_autorizado = data['precio_autorizado']
    if 'precio_apoyo' in data:
        recibo.precio_apoyo = data['precio_apoyo']
    if 'total_pagar' in data:
        recibo.total_pagar = data['total_pagar']
    if 'banco' in data:
        recibo.banco = data['banco']
    if 'clabe' in data:
        recibo.clabe = data['clabe']
    if 'concepto' in data:
        recibo.concepto = data['concepto']

    try:
        db.session.commit()
        return jsonify(recibo.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@recibos_bp.route('/<int:id>', methods=['DELETE'])
def delete_recibo(id):
    """Eliminar un recibo"""
    recibo = Recibo.query.get_or_404(id)

    try:
        db.session.delete(recibo)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@recibos_bp.route('/<int:id>/completo', methods=['GET'])
def get_recibo_completo(id):
    """Obtener recibo con toda la información relacionada"""
    recibo = Recibo.query.get_or_404(id)
    result = recibo.to_dict()
    result['consumo'] = recibo.consumo.to_dict() if recibo.consumo else None
    result['cargos'] = [c.to_dict() for c in recibo.cargos]
    result['historico'] = [h.to_dict() for h in recibo.historico]
    return jsonify(result), 200
