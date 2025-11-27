# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.setting import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # CORS completamente habilitado para todo
    CORS(app, resources={r"/*": {"origins": "*"}})


    with app.app_context():
        from app.models.employee import Employee
        from app.models.area import Area
        from app.models.role import Role
        from app.models.request_status import RequestStatus
        from app.models.request import Request
        from app.models.request_detail import RequestDetail
        from app.models.review_request import ReviewRequest

    from app.routes.employee_route import employee_bp
    from app.routes.area_route import area_bp
    from app.routes.role_route import role_bp
    from app.routes.request_route import request_bp
    from app.routes.review_route import review_bp
    from app.routes.request_status_route import request_status_bp

    app.register_blueprint(employee_bp, url_prefix="/employees")
    app.register_blueprint(area_bp, url_prefix="/areas")
    app.register_blueprint(role_bp, url_prefix="/roles")
    app.register_blueprint(request_bp, url_prefix="/requests")
    app.register_blueprint(review_bp, url_prefix="/reviews")
    app.register_blueprint(request_status_bp, url_prefix="/request-status")

    return app
