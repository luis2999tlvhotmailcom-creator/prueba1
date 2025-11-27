# app/models/area.py
from app import db

class Area(db.Model):
    __tablename__ = "area"
    __table_args__ = {"schema": "DEVELOPER_02_SV"}

    # =====================
    # Campos base
    # =====================
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200))
    status = db.Column(db.String(1), default="A", nullable=False)

    # =====================
    # Relación con empleado (jefe de área)
    # =====================
    # Un área puede tener UN jefe asignado
    chief_area_id = db.Column(
        db.Integer,
        db.ForeignKey("DEVELOPER_01_SV.employee.id"),
        unique=True,  # relación uno a uno
        nullable=True
    )

    # El empleado jefe (relación 1:1)
    chief = db.relationship(
        "Employee",
        back_populates="chief_area",
        uselist=False,
        foreign_keys=[chief_area_id]
    )

    # =====================
    # Relación inversa con empleados
    # =====================
    # Un área puede tener muchos empleados
    employees = db.relationship(
        "Employee",
        back_populates="area",
        foreign_keys="Employee.area_id",
        lazy=True
    )

    # =====================
    # Métodos de utilidad
    # =====================
    def __repr__(self):
        return f"<Area {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "chief_area_id": self.chief_area_id,
            "chief_name": f"{self.chief.names} {self.chief.lastnames}" if self.chief else None
        }