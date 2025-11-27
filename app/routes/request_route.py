# app/routes/request_route.py
from flask import Blueprint, request, jsonify
from app.services.request_service import RequestService

request_bp = Blueprint("request", __name__)

# ========================================
# CREATE - Crear solicitud
# ========================================
@request_bp.route("", methods=["POST"])
def create_request():
    """
    POST /requests
    Body: {
        "employee_id": 1,
        "description": "Vacaciones de verano",
        "details": [
            {"start_date": "2025-01-15", "end_date": "2025-01-20"}
        ]
    }
    """
    data = request.get_json()
    
    employee_id = data.get("employee_id")
    description = data.get("description", "")
    details = data.get("details", [])
    
    if not employee_id or not details:
        return jsonify({"error": "employee_id y details son requeridos"}), 400
    
    result, status = RequestService.create_request(employee_id, description, details)
    return jsonify(result), status

# ========================================
# READ - Listar todas las solicitudes
# ========================================
@request_bp.route("", methods=["GET"])
def get_all_requests():
    """
    GET /requests?employee_id=1&status=PENDIENTE
    """
    employee_id = request.args.get("employee_id", type=int)
    status = request.args.get("status")
    
    result, status_code = RequestService.get_all_requests(employee_id, status)
    return jsonify(result), status_code

# ========================================
# READ - Obtener solicitud por ID
# ========================================
@request_bp.route("/<int:request_id>", methods=["GET"])
def get_request_by_id(request_id):
    """
    GET /requests/1
    """
    result, status = RequestService.get_request_by_id(request_id)
    return jsonify(result), status

# ========================================
# UPDATE - Actualizar solicitud (PATCH)
# ========================================
@request_bp.route("/<int:request_id>", methods=["PATCH"])
def update_request(request_id):
    """
    PATCH /requests/1
    Body: {
        "description": "Nueva descripción",
        "details": [
            {"start_date": "2025-02-01", "end_date": "2025-02-10"}
        ]
    }
    """
    data = request.get_json()
    
    description = data.get("description")
    details = data.get("details")
    
    result, status = RequestService.update_request(request_id, description, details)
    return jsonify(result), status

# ========================================
# DELETE - Eliminación lógica (PATCH)
# ========================================
@request_bp.route("/<int:request_id>/cancel", methods=["PATCH"])
def cancel_request(request_id):
    """
    PATCH /requests/1/cancel
    Marca la solicitud como CANCELADA (eliminación lógica)
    """
    result, status = RequestService.soft_delete_request(request_id)
    return jsonify(result), status

# ========================================
# DELETE - Eliminación física (SOLO PRUEBAS)
# ========================================
@request_bp.route("/<int:request_id>/hard-delete", methods=["DELETE"])
def hard_delete_request(request_id):
    """
    DELETE /requests/1/hard-delete
    ADVERTENCIA: Elimina permanentemente de la BD. Solo para pruebas.
    """
    result, status = RequestService.hard_delete_request(request_id)
    return jsonify(result), status

# ========================================
# Resumen de vacaciones del empleado
# ========================================
@request_bp.route("/employee/<int:employee_id>/summary", methods=["GET"])
def get_vacation_summary(employee_id):
    """
    GET /requests/employee/1/summary
    """
    result, status = RequestService.get_employee_vacation_summary(employee_id)
    return jsonify(result), status