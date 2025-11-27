# app/models/request_status.py
from app import db

class RequestStatus(db.Model):
    __tablename__ = "request_status"
    __table_args__ = {"schema": "DEVELOPER_02_SV"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state_request = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(50))

    # Relación inversa
    reviews = db.relationship("ReviewRequest", back_populates="status", lazy=True)

    def __repr__(self):
        return f"<RequestStatus {self.state_request}>"

    def to_dict(self):
        return {
            "id": self.id,
            "state_request": self.state_request,
            "description": self.description
        }