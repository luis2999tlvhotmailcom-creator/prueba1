# app/models/review_request.py
from app import db
from datetime import datetime

class ReviewRequest(db.Model):
    __tablename__ = "review_request"
    __table_args__ = {"schema": "DEVELOPER_02_SV"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    review_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    reason_rejection = db.Column(db.String(100))
    observation = db.Column(db.String(260))
    
    # Foreign Keys
    reviser_id = db.Column(db.Integer, db.ForeignKey("DEVELOPER_01_SV.employee.id"))
    request_id = db.Column(
        db.Integer, 
        db.ForeignKey("DEVELOPER_01_SV.request.id"), 
        nullable=False
    )
    request_status_id = db.Column(
        db.Integer, 
        db.ForeignKey("DEVELOPER_02_SV.request_status.id"), 
        nullable=False
    )

    # Relaciones
    reviser = db.relationship("Employee", foreign_keys=[reviser_id])
    request = db.relationship("Request", back_populates="reviews")
    status = db.relationship("RequestStatus", back_populates="reviews")

    def __repr__(self):
        return f"<ReviewRequest {self.id} - Status {self.request_status_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "review_date": self.review_date.isoformat() if self.review_date else None,
            "reason_rejection": self.reason_rejection,
            "observation": self.observation,
            "reviser_id": self.reviser_id,
            "reviser_name": f"{self.reviser.names} {self.reviser.lastnames}" if self.reviser else None,
            "request_id": self.request_id,
            "status": self.status.to_dict() if self.status else None
        }