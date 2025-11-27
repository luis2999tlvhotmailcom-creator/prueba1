# app/models/request.py
from app import db
from datetime import datetime

class Request(db.Model):
    __tablename__ = "request"
    __table_args__ = {"schema": "DEVELOPER_01_SV"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(2000))
    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("DEVELOPER_01_SV.employee.id"),
        nullable=False
    )

    # Relaciones
    employee = db.relationship("Employee", back_populates="requests")
    details = db.relationship(
        "RequestDetail",
        back_populates="request",
        cascade="all, delete-orphan",
        lazy=True
    )
    reviews = db.relationship(
        "ReviewRequest",
        back_populates="request",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Request {self.id} - Employee {self.employee_id}>"

    def to_dict(self):
        """
        Convierte el objeto Request a un diccionario listo para JSON.
        Incluye detalles, revisiones y el estado actual real.
        """

        # 🔹 Obtener la última revisión (más reciente por ID)
        if self.reviews:
            last_review = max(self.reviews, key=lambda r: r.id)
            current_status = {
                "state": last_review.status.state_request if last_review.status else "PENDIENTE",
                "description": last_review.status.description if last_review.status else "Solicitud en espera de revisión"
            }
        else:
            current_status = {
                "state": "PENDIENTE",
                "description": "Solicitud en espera de revisión"
            }

        # 🔹 Calcular total de días solicitados
        total_days = sum(detail.days_requested for detail in self.details) if self.details else 0

        return {
            "id": self.id,
            "request_date": self.request_date.isoformat() if self.request_date else None,
            "description": self.description,
            "employee_id": self.employee_id,
            "employee_name": f"{self.employee.names} {self.employee.lastnames}" if self.employee else None,
            "total_days": total_days,
            "current_status": current_status,
            "details": [detail.to_dict() for detail in self.details] if self.details else [],
            "reviews": [review.to_dict() for review in self.reviews] if self.reviews else []
        }