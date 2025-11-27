from app import db
from app.models.role import Role
# ======================
# get all roles
# ======================
def get_all_roles():
    return Role.query.all()

# ======================
# get role by id
# ======================
def get_role_by_id(role_id):
    return Role.query.get(role_id)

# ======================
# update description role
# ======================
def update_role(role, data):
    # No permitimos cambiar name (solo description)
    if "name" in data and data["name"] != role.name:
        raise ValueError("No está permitido cambiar el nombre del rol.")
    role.description = data.get("description", role.description)
    db.session.commit()
    return role