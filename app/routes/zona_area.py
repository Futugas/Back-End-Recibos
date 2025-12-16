from flask import Blueprint, jsonify
from app.models import Zona, Area
from flask_jwt_extended import jwt_required

zonas_bp = Blueprint('zonas', __name__)


# Helper para respuestas uniformes
def response(status=200, message="OK", data=None):
    return jsonify({
        "status": status,
        "message": message,
        "data": data
    }), status


# GET /api/zonas
@zonas_bp.get('')
@jwt_required()
def get_zonas():
    """Obtiene todas las zonas disponibles"""
    try:
        zonas = Zona.query.order_by(Zona.nombre).all()
        return response(
            status=200,
            message="Lista de zonas obtenida correctamente",
            data=[z.to_dict() for z in zonas]
        )
    except Exception as e:
        return response(500, f"Error al obtener zonas: {str(e)}")


# GET /api/zonas/<id>/areas
@zonas_bp.get('/<int:id>/areas')
@jwt_required()
def get_areas_por_zona(id):
    """Obtiene todas las áreas de una zona específica"""
    zona = Zona.query.get_or_404(id)

    try:
        areas = Area.query.filter_by(zona_id=id).order_by(Area.nombre).all()

        return response(
            status=200,
            message=f"Áreas de la zona {zona.nombre} obtenidas correctamente",
            data=[a.to_dict() for a in areas]
        )
    except Exception as e:
        return response(500, f"Error al obtener áreas: {str(e)}")
