from app import db
from app.models.employee import Employee
from app.models.area import Area  # 🔹 Import necesario para vincular jefe de área
from sqlalchemy.exc import IntegrityError
from datetime import datetime

def _parse_date(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value.date()
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except Exception:
        raise ValueError("Formato de fecha inválido, use YYYY-MM-DD")

# ======================
# Get all employees
# ======================
def get_all_employees():
    return Employee.query.all()

# ======================
# Get by id
# ======================
def get_employee_by_id(emp_id):
    return Employee.query.get(emp_id)

# ======================
# Create employee
# ======================
def create_employee(data):
    birth = _parse_date(data.get("birthdate")) if data.get("birthdate") else None
    try:
        role_id = int(data.get("role_id")) if data.get("role_id") else None
        area_id = int(data.get("area_id")) if data.get("area_id") else None
        vacation_days = int(data.get("vacation_days", 30))
    except ValueError:
        raise ValueError("Los campos numéricos deben ser números válidos.")

    new = Employee(
        type_document=data.get("type_document"),
        number_document=data.get("number_document"),
        names=data.get("names"),
        lastnames=data.get("lastnames"),
        birthdate=birth,
        phone=data.get("phone"),
        email=data.get("email"),
        address=data.get("address"),
        gender=data.get("gender"),
        vacation_days=vacation_days,
        status=data.get("status", "A"),
        role_id=role_id,
        area_id=area_id,
    )

    db.session.add(new)
    db.session.flush()  # 🔹 Para obtener el ID antes del commit

    # ======================
    # Si es Jefe de Área → asignar como jefe de esa área
    # ======================
    if new.role_id == 2 and new.area_id:
        area = Area.query.get(new.area_id)
        if area:
            # Evitar conflicto si el área ya tiene jefe
            if area.chief_area_id and area.chief_area_id != new.id:
                raise ValueError(f"El área '{area.name}' ya tiene un jefe asignado.")
            area.chief_area_id = new.id

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        # detectar duplicados
        if data.get("number_document") and Employee.query.filter_by(number_document=data.get("number_document")).first():
            raise ValueError("Número de documento ya existe")
        if data.get("email") and Employee.query.filter_by(email=data.get("email")).first():
            raise ValueError("Email ya registrado")
        if data.get("phone") and Employee.query.filter_by(phone=data.get("phone")).first():
            raise ValueError("Teléfono ya registrado")
        raise ValueError("Error al crear empleado: " + str(e))

    return new

# ======================
# Update employee
# ======================
def update_employee(emp_id, data):
    emp = Employee.query.get(emp_id)
    if not emp:
        return None

    if "birthdate" in data:
        emp.birthdate = _parse_date(data.get("birthdate"))

    for field in [
        "type_document","number_document","names","lastnames","phone",
        "email","address","gender","vacation_days","status","role_id","area_id"
    ]:
        if field in data:
            setattr(emp, field, data[field])

    db.session.flush()

    # ======================
    # Actualizar relación jefe ↔ área
    # ======================
    if emp.role_id == 2 and emp.area_id:
        area = Area.query.get(emp.area_id)
        if area:
            # Evita que dos jefes se asignen al mismo área
            if area.chief_area_id and area.chief_area_id != emp.id:
                raise ValueError(f"El área '{area.name}' ya tiene un jefe asignado.")
            area.chief_area_id = emp.id
    else:
        # Si deja de ser jefe, remover su vínculo como chief
        existing_area = Area.query.filter_by(chief_area_id=emp.id).first()
        if existing_area:
            existing_area.chief_area_id = None

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError("Error al actualizar empleado: " + str(e))

    return emp

# ======================
# Toggle status (PATCH)
# ======================
def patch_employee_status(emp_id):
    emp = Employee.query.get(emp_id)
    if not emp:
        return None
    emp.status = "I" if emp.status == "A" else "A"
    db.session.commit()
    return emp

# ======================
# Hard delete (if ever needed)
# ======================
def delete_employee(emp_id):
    emp = Employee.query.get(emp_id)
    if not emp:
        return False

    # Si el empleado era jefe, liberar el área
    area = Area.query.filter_by(chief_area_id=emp.id).first()
    if area:
        area.chief_area_id = None

    db.session.delete(emp)
    db.session.commit()
    return True