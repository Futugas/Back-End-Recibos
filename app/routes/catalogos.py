from flask import Blueprint, jsonify
from app.models import Zona, Area, Edificio, Departamento  # Importamos los 4 modelos
from flask_jwt_extended import jwt_required

zonas_bp = Blueprint('zonas', __name__)

# Helper para respuestas uniformes
def response(status=200, message="OK", data=None):
    return jsonify({
        "status": status,
        "message": message,
        "data": data
    }), status

# 1. GET /api/zonas
@zonas_bp.get('')
@jwt_required()
def get_zonas():
    """Obtiene todas las zonas"""
    try:
        zonas = Zona.query.order_by(Zona.nombre).all()
        return response(200, "Zonas obtenidas", [z.to_dict() for z in zonas])
    except Exception as e:
        return response(500, f"Error al obtener zonas: {str(e)}")

# 2. GET /api/zonas/<id>/areas
@zonas_bp.get('/<int:id>/areas')
@jwt_required()
def get_areas_por_zona(id):
    """Obtiene áreas de una zona específica"""
    Zona.query.get_or_404(id) # Valida que la zona exista
    try:
        areas = Area.query.filter_by(zona_id=id).order_by(Area.nombre).all()
        return response(200, "Áreas obtenidas", [a.to_dict() for a in areas])
    except Exception as e:
        return response(500, f"Error al obtener áreas: {str(e)}")

# 3. GET /api/areas/<id>/edificios
@zonas_bp.get('/areas/<int:id>/edificios')
@jwt_required()
def get_edificios_por_area(id):
    """Obtiene edificios de una área específica"""
    Area.query.get_or_404(id) # Valida que el área exista
    try:
        edificios = Edificio.query.filter_by(area_id=id).order_by(Edificio.nombre).all()
        return response(200, "Edificios obtenidos", [e.to_dict() for e in edificios])
    except Exception as e:
        return response(500, f"Error al obtener edificios: {str(e)}")

# 4. GET /api/edificios/<id>/departamentos
@zonas_bp.get('/edificios/<int:id>/departamentos')
@jwt_required()
def get_departamentos_por_edificio(id):
    """Obtiene departamentos de un edificio específico"""
    Edificio.query.get_or_404(id) # Valida que el edificio exista
    try:
        deptos = Departamento.query.filter_by(edificio_id=id).order_by(Departamento.nombre).all()
        return response(200, "Departamentos obtenidos", [d.to_dict() for d in deptos])
    except Exception as e:
        return response(500, f"Error al obtener departamentos: {str(e)}")
