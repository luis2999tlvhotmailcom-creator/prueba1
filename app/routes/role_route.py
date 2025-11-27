from flask import Blueprint, jsonify, request
from app.services.role_service import get_all_roles, get_role_by_id, update_role

role_bp = Blueprint("role_bp", __name__)

# ======================
# GET all roles
# ======================
@role_bp.route("/", methods=["GET"])


def list_roles():
    roles = get_all_roles()
    return jsonify([r.to_dict() for r in roles]), 200

# ======================
# GET role by ID
# ======================
@role_bp.route("/<int:role_id>", methods=["GET"])
def get_role(role_id):
    r = get_role_by_id(role_id)
    if not r:
        return jsonify({"mensaje": "Rol no encontrado"}), 404
    return jsonify(r.to_dict()), 200

# ======================
# PUT update description (only description allowed)
# ======================
@role_bp.route("/<int:role_id>", methods=["PUT"])
def put_role(role_id):
    r = get_role_by_id(role_id)
    if not r:
        return jsonify({"mensaje": "Rol no encontrado"}), 404
    data = request.get_json() or {}
    try:
        updated = update_role(r, data)
    except ValueError as e:
        return jsonify({"mensaje": str(e)}), 400
    return jsonify({"mensaje": "Rol actualizado correctamente", "role": updated.to_dict()}), 200