from app import db

class Role(db.Model):
    __tablename__ = "role"
    __table_args__ = {"schema": "DEVELOPER_01_SV"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(35), unique=True, nullable=False)   # coincide con DDL (columna 'name')
    description = db.Column(db.String(200))

    # Relación con Employee
    employees = db.relationship("Employee", back_populates="role", foreign_keys="Employee.role_id")

    def __repr__(self):
        return f"<Role {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "employees_count": len(self.employees) if self.employees is not None else 0
        }