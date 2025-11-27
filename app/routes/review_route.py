# app/routes/review_route.py
from flask import Blueprint, request, jsonify
from app.services.review_service import ReviewService

review_bp = Blueprint("review", __name__)

# ========================================
# APROBAR SOLICITUD
# ========================================
@review_bp.route("/approve", methods=["POST"])
def approve_request():
    """
    POST /reviews/approve
    Body: {
        "request_id": 1,
        "reviser_id": 3,
        "observation": "Aprobado"
    }
    """
    data = request.get_json()
    
    request_id = data.get("request_id")
    reviser_id = data.get("reviser_id")
    observation = data.get("observation")
    
    if not request_id or not reviser_id:
        return jsonify({"error": "request_id y reviser_id son requeridos"}), 400
    
    result, status = ReviewService.approve_request(request_id, reviser_id, observation)
    return jsonify(result), status

# ========================================
# RECHAZAR SOLICITUD
# ========================================
@review_bp.route("/reject", methods=["POST"])
def reject_request():
    """
    POST /reviews/reject
    Body: {
        "request_id": 1,
        "reviser_id": 3,
        "reason_rejection": "Periodo no disponible",
        "observation": "Solicitar en otro periodo"
    }
    """
    data = request.get_json()
    
    request_id = data.get("request_id")
    reviser_id = data.get("reviser_id")
    reason_rejection = data.get("reason_rejection")
    observation = data.get("observation")
    
    if not request_id or not reviser_id or not reason_rejection:
        return jsonify({"error": "request_id, reviser_id y reason_rejection son requeridos"}), 400
    
    result, status = ReviewService.reject_request(
        request_id, reviser_id, reason_rejection, observation
    )
    return jsonify(result), status

# ========================================
# LISTAR SOLICITUDES PENDIENTES (FORMATO SIMPLE)
# ========================================
@review_bp.route("/pending", methods=["GET"])
def get_pending_requests():
    """
    GET /reviews/pending?reviser_id=3
    
    Formato de respuesta simplificado para frontend:
    [
        {
            "request_id": 1,
            "employee_name": "Juan Pérez",
            "area": "Administración",
            "total_days": 10,
            "periods": [...]
        }
    ]
    """
    reviser_id = request.args.get("reviser_id", type=int)
    
    result, status = ReviewService.get_pending_requests_simple(reviser_id)
    return jsonify(result), status