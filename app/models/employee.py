from app import db
from datetime import date

class Employee(db.Model):
    __tablename__ = "employee"
    __table_args__ = {"schema": "DEVELOPER_01_SV"}

    # =====================
    # Campos base
    # =====================
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_document = db.Column(db.String(3), nullable=False)
    number_document = db.Column(db.String(15), unique=True, nullable=False)
    names = db.Column(db.String(100), nullable=False)
    lastnames = db.Column(db.String(90), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(9), unique=True)
    email = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(100))
    gender = db.Column(db.String(1))
    vacation_days = db.Column(db.Integer, default=30)
    status = db.Column(db.String(1), default="A")

    # =====================
    # Foreign Keys
    # =====================
    role_id = db.Column(db.Integer, db.ForeignKey("DEVELOPER_01_SV.role.id"), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey("DEVELOPER_02_SV.area.id"))

    # =====================
    # Relaciones
    # =====================
    role = db.relationship("Role", back_populates="employees")
    area = db.relationship("Area", back_populates="employees", foreign_keys=[area_id])

    # Relación 1:1 — empleado puede ser jefe de una sola área
    chief_area = db.relationship(
        "Area",
        back_populates="chief",
        uselist=False,
        foreign_keys="[Area.chief_area_id]"
    )

    # Relación con solicitudes de vacaciones
    requests = db.relationship("Request", back_populates="employee", lazy=True)

    # =====================
    # Métodos de utilidad
    # =====================
    def __repr__(self):
        return f"<Employee {self.names} {self.lastnames}>"

    def to_dict(self):
        return {
            "id": self.id,
            "type_document": self.type_document,
            "number_document": self.number_document,
            "names": self.names,
            "lastnames": self.lastnames,
            "birthdate": self.birthdate.isoformat() if self.birthdate else None,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "gender": self.gender,
            "vacation_days": self.vacation_days,
            "status": self.status,
            "role_id": self.role_id,
            "area_id": self.area_id,
            "area_name": self.area.name if self.area else None,
            "chief_area_id": self.chief_area.id if self.chief_area else None
        }