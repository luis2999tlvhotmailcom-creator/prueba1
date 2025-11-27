from flask import Blueprint, jsonify, request
from app.services.area_service import (
    get_all_areas,
    get_area_by_id,
    create_area,
    update_area,
    patch_area_status
)

area_bp = Blueprint("area_bp", __name__)

# ======================
# GET all areas
# ======================
@area_bp.route("", methods=["GET"])
def list_areas():
    areas = get_all_areas()
    return jsonify([a.to_dict() for a in areas]), 200

# ======================
# GET areas without chief
# ======================
@area_bp.route("/no-chief", methods=["GET"])
def list_areas_without_chief():
    from app.services.area_service import get_areas_without_chief
    areas = get_areas_without_chief()
    return jsonify([a.to_dict() for a in areas]), 200

# ======================
# GET area by ID
# ======================
@area_bp.route("/<int:area_id>", methods=["GET"])
def get_area(area_id):
    a = get_area_by_id(area_id)
    if not a:
        return jsonify({"mensaje": "Área no encontrada"}), 404
    return jsonify(a.to_dict()), 200


# ======================
# POST create area
# ======================
@area_bp.route("", methods=["POST"])
def add_area():
    data = request.get_json() or {}
    try:
        new = create_area(data)
    except ValueError as e:
        return jsonify({"mensaje": str(e)}), 400
    return jsonify({"mensaje": "Área creada correctamente", "area": new.to_dict()}), 201


# ======================
# PATCH update area
# ======================
@area_bp.route("/<int:area_id>", methods=["PATCH"])
def patch_area_update(area_id):
    data = request.get_json() or {}
    try:
        updated = update_area(area_id, data)
    except ValueError as e:
        return jsonify({"mensaje": str(e)}), 400
    if not updated:
        return jsonify({"mensaje": "Área no encontrada"}), 404
    return jsonify({"mensaje": "Área actualizada correctamente", "area": updated.to_dict()}), 200


# ======================
# PATCH toggle status (A/I)
# ======================
@area_bp.route("/<int:area_id>/status", methods=["PATCH"])
def patch_area(area_id):
    updated = patch_area_status(area_id)
    if not updated:
        return jsonify({"mensaje": "Área no encontrada"}), 404
    return jsonify({"mensaje": "Estado del área actualizado correctamente", "area": updated.to_dict()}), 200