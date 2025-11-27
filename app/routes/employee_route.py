from flask import Blueprint, jsonify, request
from app.services.employee_service import (
    get_all_employees,
    get_employee_by_id,
    create_employee,
    update_employee,
    delete_employee,
    patch_employee_status
)

employee_bp = Blueprint("employee_bp", __name__)

# ======================
# GET all employees
# ======================
@employee_bp.route("", methods=["GET"])
def list_employees():
    employees = get_all_employees()
    return jsonify([e.to_dict() for e in employees]), 200


# ======================
# GET employee by ID
# ======================
@employee_bp.route("/<int:emp_id>", methods=["GET"])
def get_employee(emp_id):
    emp = get_employee_by_id(emp_id)
    if not emp:
        return jsonify({"mensaje": "Empleado no encontrado"}), 404
    return jsonify(emp.to_dict()), 200


# ======================
# POST create employee
# ======================
@employee_bp.route("", methods=["POST"])
def add_employee():
    data = request.get_json() or {}
    try:
        new = create_employee(data)
    except ValueError as e:
        return jsonify({"mensaje": str(e)}), 400
    return jsonify({"mensaje": "Empleado creado correctamente", "employee": new.to_dict()}), 201


# ======================
# PATCH update employee
# ======================
@employee_bp.route("/<int:emp_id>", methods=["PATCH"])
def patch_employee_data(emp_id):
    data = request.get_json() or {}
    try:
        updated = update_employee(emp_id, data)
    except ValueError as e:
        return jsonify({"mensaje": str(e)}), 400
    if not updated:
        return jsonify({"mensaje": "Empleado no encontrado"}), 404
    return jsonify({"mensaje": "Empleado actualizado correctamente", "employee": updated.to_dict()}), 200


# ======================
# PATCH toggle status (A/I)
# ======================
@employee_bp.route("/<int:emp_id>/status", methods=["PATCH"])
def patch_employee(emp_id):
    updated = patch_employee_status(emp_id)
    if not updated:
        return jsonify({"mensaje": "Empleado no encontrado"}), 404
    return jsonify({"mensaje": "Estado del empleado actualizado correctamente", "employee": updated.to_dict()}), 200


# ======================
# DELETE employee
# ======================
@employee_bp.route("/<int:emp_id>", methods=["DELETE"])
def delete_employee_route(emp_id):
    deleted = delete_employee(emp_id)
    if not deleted:
        return jsonify({"mensaje": "Empleado no encontrado"}), 404
    return jsonify({"mensaje": "Empleado eliminado correctamente"}), 200