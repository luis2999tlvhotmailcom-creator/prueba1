# app/services/area_service.py
from app import db
from app.models.area import Area
from sqlalchemy.exc import IntegrityError

# ======================
# get all areas
# ======================
def get_all_areas():
    return Area.query.all()

# ======================
# get area by id
# ======================
def get_area_by_id(area_id):
    return Area.query.get(area_id)

# ======================
# get areas WITHOUT chief assigned
# ======================
def get_areas_without_chief():
    return Area.query.filter(Area.chief_area_id.is_(None)).all()

# ======================
# create area
# ======================
def create_area(data):
    new = Area(
        name=data.get("name"),
        description=data.get("description"),
        status=data.get("status", "A"),
        chief_area_id=data.get("chief_area_id")  # puede ser None
    )
    db.session.add(new)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError("Error al crear área: " + str(e))
    return new

# ======================
# update area
# ======================
def update_area(area_id, data):
    a = Area.query.get(area_id)
    if not a:
        return None

    a.name = data.get("name", a.name)
    a.description = data.get("description", a.description)
    a.chief_area_id = data.get("chief_area_id", a.chief_area_id)

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError("Error al actualizar área: " + str(e))
    return a

# ======================
# toggle status (PATCH)
# ======================
def patch_area_status(area_id):
    a = Area.query.get(area_id)
    if not a:
        return None
    a.status = "I" if a.status == "A" else "A"
    db.session.commit()
    return a