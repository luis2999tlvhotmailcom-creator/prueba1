# app/routes/request_status_route.py
from flask import Blueprint, jsonify, request
from app.services.request_status_service import RequestStatusService

request_status_bp = Blueprint("request_status", __name__)

# ========================================
# CREATE - Crear estado
# ========================================
@request_status_bp.route("", methods=["POST"])
def create_status():
    """
    POST /request-status
    Body: {
        "state_request": "PENDIENTE",
        "description": "Solicitud pendiente de revisión"
    }
    """
    data = request.get_json()
    result, status = RequestStatusService.create_status(data)
    return jsonify(result), status

# ========================================
# READ - Listar todos los estados
# ========================================
@request_status_bp.route("", methods=["GET"])
def get_all_statuses():
    """
    GET /request-status
    """
    result, status = RequestStatusService.get_all_statuses()
    return jsonify(result), status

# ========================================
# READ - Obtener estado por ID
# ========================================
@request_status_bp.route("/<int:status_id>", methods=["GET"])
def get_status_by_id(status_id):
    """
    GET /request-status/1
    """
    result, status = RequestStatusService.get_status_by_id(status_id)
    return jsonify(result), status

# ========================================
# UPDATE - Actualizar estado
# ========================================
@request_status_bp.route("/<int:status_id>", methods=["PUT"])
def update_status(status_id):
    """
    PUT /request-status/1
    Body: {
        "state_request": "APROBADO",
        "description": "Solicitud aprobada por el jefe"
    }
    """
    data = request.get_json()
    result, status = RequestStatusService.update_status(status_id, data)
    return jsonify(result), status

# ========================================
# DELETE - Eliminar estado (solo pruebas)
# ========================================
@request_status_bp.route("/<int:status_id>", methods=["DELETE"])
def delete_status(status_id):
    """
    DELETE /request-status/1
    ADVERTENCIA: Elimina permanentemente el estado (solo pruebas)
    """
    result, status = RequestStatusService.delete_status(status_id)
    return jsonify(result), status