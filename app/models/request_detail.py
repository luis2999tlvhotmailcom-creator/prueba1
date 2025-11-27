# app/models/request_detail.py
from app import db

class RequestDetail(db.Model):
    __tablename__ = "request_detail"
    __table_args__ = {"schema": "DEVELOPER_01_SV"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    days_requested = db.Column(db.Integer, nullable=False)
    request_id = db.Column(
        db.Integer, 
        db.ForeignKey("DEVELOPER_01_SV.request.id"), 
        nullable=False
    )

    # Relación
    request = db.relationship("Request", back_populates="details")

    def __repr__(self):
        return f"<RequestDetail {self.id} - {self.days_requested} days>"

    def to_dict(self):
        return {
            "id": self.id,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "days_requested": self.days_requested,
            "request_id": self.request_id
        }