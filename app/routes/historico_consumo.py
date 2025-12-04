from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import HistoricoConsumo

historico_bp = Blueprint('historico_consumo', __name__)

@historico_bp.route('', methods=['GET'])
def get_historicos():
    historicos = HistoricoConsumo.query.all()
    return jsonify([h.to_dict() for h in historicos]), 200

@historico_bp.route('/<int:id>', methods=['GET'])
def get_historico(id):
    historico = HistoricoConsumo.query.get_or_404(id)
    return jsonify(historico.to_dict()), 200

@historico_bp.route('', methods=['POST'])
def create_historico():
    data = request.get_json()

    if not data or not data.get('recibo_id'):
        return jsonify({'error': 'El recibo_id es requerido'}), 400

    historico = HistoricoConsumo(
        recibo_id=data.get('recibo_id'),
        periodo_inicio=datetime.strptime(data['periodo_inicio'], '%Y-%m-%d').date() if data.get('periodo_inicio') else None,
        periodo_fin=datetime.strptime(data['periodo_fin'], '%Y-%m-%d').date() if data.get('periodo_fin') else None,
        litros=data.get('litros')
    )

    try:
        db.session.add(historico)
        db.session.commit()
        return jsonify(historico.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@historico_bp.route('/<int:id>', methods=['PUT'])
def update_historico(id):
    historico = HistoricoConsumo.query.get_or_404(id)
    data = request.get_json()

    if 'recibo_id' in data:
        historico.recibo_id = data['recibo_id']
    if 'periodo_inicio' in data:
        historico.periodo_inicio = datetime.strptime(data['periodo_inicio'], '%Y-%m-%d').date()
    if 'periodo_fin' in data:
        historico.periodo_fin = datetime.strptime(data['periodo_fin'], '%Y-%m-%d').date()
    if 'litros' in data:
        historico.litros = data['litros']

    try:
        db.session.commit()
        return jsonify(historico.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@historico_bp.route('/<int:id>', methods=['DELETE'])
def delete_historico(id):
    historico = HistoricoConsumo.query.get_or_404(id)

    try:
        db.session.delete(historico)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
