# app/services/review_service.py
from app import db
from app.models.request import Request
from app.models.employee import Employee
from app.models.request_status import RequestStatus
from app.models.review_request import ReviewRequest
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

class ReviewService:
    
    # ========================================
    # ✅ APROBAR SOLICITUD
    # ========================================
    @staticmethod
    def approve_request(request_id, reviser_id, observation=None):
        """
        Aprobar una solicitud de vacaciones
        
        Args:
            request_id: ID de la solicitud
            reviser_id: ID del jefe/RRHH que aprueba
            observation: Observaciones opcionales
        """
        try:
            # 🔹 Validar solicitud
            request = Request.query.get(request_id)
            if not request:
                return {"error": "Solicitud no encontrada"}, 404
            
            # 🔹 Validar revisor
            reviser = Employee.query.get(reviser_id)
            if not reviser:
                return {"error": "Revisor no encontrado"}, 404
            
            if reviser.role.name not in ["JEFE_AREA", "RRHH"]:
                return {"error": "El revisor debe ser JEFE_AREA o RRHH"}, 403
            
            # 🔹 Verificar estado actual
            if request.reviews:
                last_review = max(request.reviews, key=lambda r: r.review_date)
                if last_review.status.state_request.upper() != "PENDIENTE":
                    return {"error": "La solicitud ya fue revisada"}, 400
            
            # 🔹 Calcular días y descontar
            total_days = sum(d.days_requested for d in request.details)
            
            employee = request.employee
            if total_days > employee.vacation_days:
                return {"error": "El empleado no tiene suficientes días disponibles"}, 400
            
            employee.vacation_days -= total_days
            
            # 🔹 Crear estado APROBADO
            approved_status = RequestStatus.query.filter_by(state_request="APROBADO").first()
            if not approved_status:
                approved_status = RequestStatus(
                    state_request="APROBADO",
                    description="Solicitud aprobada"
                )
                db.session.add(approved_status)
                db.session.flush()
            
            # 🔹 Crear revisión
            review = ReviewRequest(
                request_id=request_id,
                reviser_id=reviser_id,
                request_status_id=approved_status.id,
                review_date=datetime.now().date(),
                observation=observation or "Solicitud aprobada"
            )
            
            db.session.add(review)
            db.session.commit()
            
            return {
                "message": "Solicitud aprobada correctamente",
                "request": request.to_dict()
            }, 200
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Error al aprobar solicitud: {str(e)}"}, 500
    
    # ========================================
    # ❌ RECHAZAR SOLICITUD
    # ========================================
    @staticmethod
    def reject_request(request_id, reviser_id, reason_rejection, observation=None):
        """
        Rechazar una solicitud de vacaciones
        
        Args:
            request_id: ID de la solicitud
            reviser_id: ID del jefe/RRHH que rechaza
            reason_rejection: Motivo del rechazo (OBLIGATORIO)
            observation: Observaciones adicionales
        """
        try:
            # 🔹 Validaciones
            request = Request.query.get(request_id)
            if not request:
                return {"error": "Solicitud no encontrada"}, 404
            
            reviser = Employee.query.get(reviser_id)
            if not reviser:
                return {"error": "Revisor no encontrado"}, 404
            
            if reviser.role.name not in ["JEFE_AREA", "RRHH"]:
                return {"error": "El revisor debe ser JEFE_AREA o RRHH"}, 403
            
            if not reason_rejection:
                return {"error": "El motivo de rechazo es obligatorio"}, 400
            
            # 🔹 Verificar estado
            if request.reviews:
                last_review = max(request.reviews, key=lambda r: r.review_date)
                if last_review.status.state_request.upper() != "PENDIENTE":
                    return {"error": "La solicitud ya fue revisada"}, 400
            
            # 🔹 Crear estado RECHAZADO
            rejected_status = RequestStatus.query.filter_by(state_request="RECHAZADO").first()
            if not rejected_status:
                rejected_status = RequestStatus(
                    state_request="RECHAZADO",
                    description="Solicitud rechazada"
                )
                db.session.add(rejected_status)
                db.session.flush()
            
            # 🔹 Crear revisión
            review = ReviewRequest(
                request_id=request_id,
                reviser_id=reviser_id,
                request_status_id=rejected_status.id,
                review_date=datetime.now().date(),
                reason_rejection=reason_rejection,
                observation=observation
            )
            
            db.session.add(review)
            db.session.commit()
            
            return {
                "message": "Solicitud rechazada",
                "request": request.to_dict()
            }, 200
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Error al rechazar solicitud: {str(e)}"}, 500
    
    # ========================================
    # 📋 LISTAR SOLICITUDES PENDIENTES (FORMATO SIMPLIFICADO)
    # ========================================
    @staticmethod
    def get_pending_requests_simple(reviser_id=None):
        """
        Listar solicitudes pendientes en formato simplificado para el frontend
        
        Args:
            reviser_id: Si es JEFE_AREA, filtra por su área. Si es RRHH, muestra todas.
        
        Returns:
            Lista con formato:
            {
                "request_id": 1,
                "employee_id": 5,
                "employee_name": "Juan Pérez",
                "area": "Administración",
                "request_date": "2025-11-10",
                "total_days": 10,
                "periods": [
                    {"start": "2025-12-15", "end": "2025-12-20", "days": 6}
                ],
                "description": "Vacaciones de fin de año"
            }
        """
        try:
            reviser = None
            is_area_chief = False
            area_id = None
            
            if reviser_id:
                reviser = Employee.query.get(reviser_id)
                if not reviser:
                    return {"error": "Revisor no encontrado"}, 404
                
                # Identificar si es jefe de área
                if reviser.role.name == "JEFE_AREA":
                    is_area_chief = True
                    area_id = reviser.area_id
            
            # 🔹 Obtener estado PENDIENTE
            pending_status = RequestStatus.query.filter_by(state_request="PENDIENTE").first()
            if not pending_status:
                return [], 200
            
            # 🔹 Buscar todas las solicitudes
            all_requests = Request.query.order_by(Request.request_date.desc()).all()
            
            pending_list = []
            
            for req in all_requests:
                if req.reviews:
                    last_review = max(req.reviews, key=lambda r: r.review_date)
                    
                    # Solo mostrar PENDIENTES
                    if last_review.status.state_request.upper() == "PENDIENTE":
                        
                        # Filtro por área si es jefe
                        if is_area_chief and req.employee.area_id != area_id:
                            continue
                        
                        # 🔹 Calcular días totales y periodos
                        total_days = sum(d.days_requested for d in req.details)
                        periods = [
                            {
                                "start": d.start_date.isoformat(),
                                "end": d.end_date.isoformat(),
                                "days": d.days_requested
                            }
                            for d in req.details
                        ]
                        
                        # 🔹 Formato simplificado
                        pending_list.append({
                            "request_id": req.id,
                            "employee_id": req.employee_id,
                            "employee_name": f"{req.employee.names} {req.employee.lastnames}",
                            "area": req.employee.area.name if req.employee.area else "Sin área",
                            "request_date": req.request_date.isoformat(),
                            "total_days": total_days,
                            "periods": periods,
                            "description": req.description or ""
                        })
            
            return pending_list, 200
            
        except SQLAlchemyError as e:
            return {"error": f"Error al listar solicitudes pendientes: {str(e)}"}, 500