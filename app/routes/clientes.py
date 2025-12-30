from flask import Blueprint, request, jsonify
from app import db
from app.models import Cliente
from flask_jwt_extended import jwt_required

clientes_bp = Blueprint('clientes', __name__)

# Helper para respuestas uniformes
def response(status=200, message="OK", data=None):
    return jsonify({
        "status": status,
        "message": message,
        "data": data
    }), status

# GET /api/clientes
@clientes_bp.get('')
@jwt_required()
def get_clientes():
    clientes = Cliente.query.all()
    return response(
        status=200,
        message="Lista de clientes obtenida",
        data=[c.to_dict() for c in clientes]
    )

# GET /api/clientes/<id>
@clientes_bp.get('/<int:id>')
@jwt_required()
def get_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return response(
        status=200,
        message="Cliente obtenido correctamente",
        data=cliente.to_dict()
    )

# POST /api/clientes
@clientes_bp.post('')
@jwt_required()
def create_cliente():
    data = request.get_json() or {}

    if not data.get('nombre'):
        return response(400, "El nombre es obligatorio")

    cliente = Cliente(
        nombre=data.get('nombre'),
        direccion=data.get('direccion'),
        referencia=data.get('referencia'),
        codigo_postal=data.get('codigo_postal'),
        zona_id=data.get('zona_id'),
        area_id=data.get('area_id'),
        edificio_id=data.get('edificio_id'),
        departamento_id=data.get('departamento_id')
    )

    try:
        db.session.add(cliente)
        db.session.commit()
        return response(201, "Cliente creado exitosamente", cliente.to_dict())
    except Exception as e:
        db.session.rollback()
        return response(500, f"Error al crear cliente: {str(e)}")

@clientes_bp.put('/<int:id>')
@jwt_required()
def update_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    data = request.get_json() or {}

    fields = [
        "nombre",
        "direccion",
        "referencia",
        "codigo_postal",
        "zona_id",
        "area_id",
        "edificio_id",
        "departamento_id",
        "cargo",
        "estado",
        "precio",
        "fecha"
    ]

    for field in fields:
        if field in data:
            setattr(cliente, field, data[field])

    # 🔥 REGLA DE NEGOCIO CLAVE
    # La lectura actual pasa a ser lectura_anterior
    if "lectura_actual" in data:
        cliente.lectura_anterior = data["lectura_actual"]

    try:
        db.session.commit()
        return response(
            200,
            "Cliente actualizado correctamente",
            cliente.to_dict()
        )
    except Exception as e:
        db.session.rollback()
        return response(
            500,
            f"Error al actualizar cliente: {str(e)}"
        )


# DELETE /api/clientes/<id>
@clientes_bp.delete('/<int:id>')
@jwt_required()
def delete_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    try:
        db.session.delete(cliente)
        db.session.commit()
        return response(204, "Cliente eliminado", None)
    except Exception as e:
        db.session.rollback()
        return response(500, f"Error al eliminar cliente: {str(e)}")

# GET /api/clientes/<id>/recibos
@clientes_bp.get('/<int:id>/recibos')
@jwt_required()
def get_recibos_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return response(
        status=200,
        message="Recibos del cliente obtenidos",
        data=[r.to_dict() for r in cliente.recibos]
    )

# GET /api/clientes/por-zona-area/<zona_id>/<area_id>
@clientes_bp.get('/por-zona-area/<int:zona_id>/<int:area_id>')
@jwt_required()
def get_clientes_por_zona_area(zona_id, area_id):
    clientes = Cliente.query.filter(
        Cliente.zona_id == zona_id,
        Cliente.area_id == area_id
    ).all()

    return response(
        status=200,
        message="Clientes filtrados por zona y área",
        data=[c.to_dict() for c in clientes]
    )

# GET /api/clientes/por-jerarquia-completa/<zona_id>/<area_id>/<edificio_id>/<depto_id>
@clientes_bp.get('/por-jerarquia-completa/<int:zona_id>/<int:area_id>/<int:edificio_id>/<int:depto_id>')
@jwt_required()
def get_clientes_full_path(zona_id, area_id, edificio_id, depto_id):
    """Obtiene los clientes filtrando por toda la cadena jerárquica"""
    try:
        clientes = Cliente.query.filter(
            Cliente.zona_id == zona_id,
            Cliente.area_id == area_id,
            Cliente.edificio_id == edificio_id,
            Cliente.departamento_id == depto_id
        ).all()

        return response(
            status=200,
            message="Clientes filtrados por la jerarquía completa",
            data=[c.to_dict() for c in clientes]
        )
    except Exception as e:
        return response(500, f"Error al filtrar clientes: {str(e)}")