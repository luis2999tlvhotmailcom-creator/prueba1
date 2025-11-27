# app/services/request_service.py
from app import db
from app.models.request import Request
from app.models.request_detail import RequestDetail
from app.models.employee import Employee
from app.models.request_status import RequestStatus
from app.models.review_request import ReviewRequest
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

class RequestService:
    
    # ========================================
    # 📋 CREATE - Crear solicitud
    # ========================================
    @staticmethod
    def create_request(employee_id, description, details):
        """
        Crear una nueva solicitud de vacaciones con sus detalles
        
        Args:
            employee_id: ID del empleado
            description: Descripción de la solicitud
            details: Lista de dict con [{"start_date": "2025-01-15", "end_date": "2025-01-20"}]
        
        Returns:
            dict: Solicitud creada o error
        """
        try:
            # 🔹 Validar empleado
            employee = Employee.query.get(employee_id)
            if not employee:
                return {"error": "Empleado no encontrado"}, 404
            
            if not details or len(details) == 0:
                return {"error": "Debe incluir al menos un periodo de vacaciones"}, 400
            
            # 🔹 Calcular y validar días
            total_days = 0
            validated_details = []
            
            for detail in details:
                start_date = datetime.strptime(detail["start_date"], "%Y-%m-%d").date()
                end_date = datetime.strptime(detail["end_date"], "%Y-%m-%d").date()
                
                if end_date < start_date:
                    return {"error": "La fecha de fin no puede ser anterior a la fecha de inicio"}, 400
                
                if start_date < datetime.now().date():
                    return {"error": "No se pueden solicitar vacaciones en fechas pasadas"}, 400
                
                days = (end_date - start_date).days + 1
                
                if days < 1 or days > 30:
                    return {"error": f"Los días solicitados deben estar entre 1 y 30. Recibido: {days}"}, 400
                
                total_days += days
                validated_details.append({
                    "start_date": start_date,
                    "end_date": end_date,
                    "days": days
                })
            
            # 🔹 Validar días disponibles
            if total_days > employee.vacation_days:
                return {
                    "error": f"Días insuficientes. Disponibles: {employee.vacation_days}, Solicitados: {total_days}"
                }, 400
            
            # 🔹 Crear solicitud
            request = Request(
                employee_id=employee_id,
                request_date=datetime.now().date(),
                description=description
            )
            
            db.session.add(request)
            db.session.flush()
            
            # 🔹 Crear detalles
            for detail in validated_details:
                request_detail = RequestDetail(
                    request_id=request.id,
                    start_date=detail["start_date"],
                    end_date=detail["end_date"],
                    days_requested=detail["days"]
                )
                db.session.add(request_detail)
            
            # 🔹 Crear revisión inicial (PENDIENTE)
            pending_status = RequestStatus.query.filter_by(state_request="PENDIENTE").first()
            if not pending_status:
                pending_status = RequestStatus(
                    state_request="PENDIENTE",
                    description="Solicitud en espera de revisión"
                )
                db.session.add(pending_status)
                db.session.flush()
            
            review = ReviewRequest(
                request_id=request.id,
                request_status_id=pending_status.id,
                review_date=datetime.now().date(),
                observation="Solicitud creada, pendiente de revisión"
            )
            db.session.add(review)
            
            db.session.commit()
            
            return request.to_dict(), 201
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Error al crear solicitud: {str(e)}"}, 500
    
    # ========================================
    # 📋 READ - Listar todas las solicitudes
    # ========================================
    @staticmethod
    def get_all_requests(employee_id=None, status=None):
        """
        Listar solicitudes con filtros opcionales
        
        Args:
            employee_id: Filtrar por empleado (opcional)
            status: Filtrar por estado: PENDIENTE, APROBADO, RECHAZADO (opcional)
        """
        try:
            query = Request.query
            
            if employee_id:
                query = query.filter_by(employee_id=employee_id)
            
            requests = query.order_by(Request.request_date.desc()).all()
            
            # Filtro por estado
            if status:
                filtered = []
                for req in requests:
                    if req.reviews:
                        last_review = max(req.reviews, key=lambda r: r.review_date)
                        if last_review.status.state_request.upper() == status.upper():
                            filtered.append(req)
                requests = filtered
            
            return [req.to_dict() for req in requests], 200
            
        except SQLAlchemyError as e:
            return {"error": f"Error al listar solicitudes: {str(e)}"}, 500
    
    # ========================================
    # 📋 READ - Obtener solicitud por ID
    # ========================================
    @staticmethod
    def get_request_by_id(request_id):
        """
        Obtener detalle completo de una solicitud
        """
        try:
            request = Request.query.get(request_id)
            if not request:
                return {"error": "Solicitud no encontrada"}, 404
            
            return request.to_dict(), 200
            
        except SQLAlchemyError as e:
            return {"error": f"Error al obtener solicitud: {str(e)}"}, 500
    
    # ========================================
    # 🔄 UPDATE - Actualizar solicitud (SOLO PARA PRUEBAS)
    # ========================================
    @staticmethod
    def update_request(request_id, description=None, details=None):
        """
        Actualizar una solicitud existente
        NOTA: En producción, esto solo debería permitirse si está PENDIENTE
        
        Args:
            request_id: ID de la solicitud
            description: Nueva descripción (opcional)
            details: Nuevos detalles de fechas (opcional)
        """
        try:
            request = Request.query.get(request_id)
            if not request:
                return {"error": "Solicitud no encontrada"}, 404
            
            # 🔹 Actualizar descripción
            if description is not None:
                request.description = description
            
            # 🔹 Actualizar detalles
            if details:
                # Eliminar detalles anteriores
                RequestDetail.query.filter_by(request_id=request_id).delete()
                
                # Validar y crear nuevos detalles
                total_days = 0
                for detail in details:
                    start_date = datetime.strptime(detail["start_date"], "%Y-%m-%d").date()
                    end_date = datetime.strptime(detail["end_date"], "%Y-%m-%d").date()
                    
                    if end_date < start_date:
                        return {"error": "Fecha de fin no puede ser anterior a fecha de inicio"}, 400
                    
                    days = (end_date - start_date).days + 1
                    
                    if days < 1 or days > 30:
                        return {"error": f"Días deben estar entre 1 y 30. Recibido: {days}"}, 400
                    
                    total_days += days
                    
                    new_detail = RequestDetail(
                        request_id=request_id,
                        start_date=start_date,
                        end_date=end_date,
                        days_requested=days
                    )
                    db.session.add(new_detail)
                
                # Validar días disponibles
                employee = request.employee
                if total_days > employee.vacation_days:
                    return {
                        "error": f"Días insuficientes. Disponibles: {employee.vacation_days}, Solicitados: {total_days}"
                    }, 400
            
            db.session.commit()
            
            return request.to_dict(), 200
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Error al actualizar solicitud: {str(e)}"}, 500
    
    # ========================================
    # ❌ DELETE - Eliminación lógica (cambiar estado a CANCELADO)
    # ========================================
    @staticmethod
    def soft_delete_request(request_id):
        """
        Eliminación lógica: marcar solicitud como CANCELADO
        NOTA: Solo si está PENDIENTE
        """
        try:
            request = Request.query.get(request_id)
            if not request:
                return {"error": "Solicitud no encontrada"}, 404
            
            # Verificar estado actual
            if request.reviews:
                last_review = max(request.reviews, key=lambda r: r.review_date)
                current_status = last_review.status.state_request.upper()
                
                if current_status != "PENDIENTE":
                    return {"error": f"No se puede cancelar una solicitud {current_status}"}, 400
            
            # Crear estado CANCELADO si no existe
            canceled_status = RequestStatus.query.filter_by(state_request="CANCELADO").first()
            if not canceled_status:
                canceled_status = RequestStatus(
                    state_request="CANCELADO",
                    description="Solicitud cancelada por el empleado"
                )
                db.session.add(canceled_status)
                db.session.flush()
            
            # Crear nueva revisión con estado CANCELADO
            review = ReviewRequest(
                request_id=request_id,
                request_status_id=canceled_status.id,
                review_date=datetime.now().date(),
                observation="Solicitud cancelada"
            )
            db.session.add(review)
            
            db.session.commit()
            
            return {"message": "Solicitud cancelada correctamente", "request": request.to_dict()}, 200
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Error al cancelar solicitud: {str(e)}"}, 500
    
    # ========================================
    # ❌ DELETE - Eliminación física (SOLO PARA PRUEBAS)
    # ========================================
    @staticmethod
    def hard_delete_request(request_id):
        """
        Eliminación física de la base de datos
        ADVERTENCIA: Solo para pruebas/desarrollo
        """
        try:
            request = Request.query.get(request_id)
            if not request:
                return {"error": "Solicitud no encontrada"}, 404
            
            db.session.delete(request)
            db.session.commit()
            
            return {"message": "Solicitud eliminada permanentemente"}, 200
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Error al eliminar solicitud: {str(e)}"}, 500
    
    # ========================================
    # 📊 UTILIDADES - Resumen de vacaciones
    # ========================================
    @staticmethod
    def get_employee_vacation_summary(employee_id):
        """
        Resumen de vacaciones del empleado
        """
        try:
            employee = Employee.query.get(employee_id)
            if not employee:
                return {"error": "Empleado no encontrado"}, 404
            
            approved_days = 0
            pending_days = 0
            
            for request in employee.requests:
                if request.reviews:
                    last_review = max(request.reviews, key=lambda r: r.review_date)
                    status = last_review.status.state_request.upper()
                    
                    total_days = sum(d.days_requested for d in request.details)
                    
                    if status == "APROBADO":
                        approved_days += total_days
                    elif status == "PENDIENTE":
                        pending_days += total_days
            
            return {
                "employee_id": employee_id,
                "employee_name": f"{employee.names} {employee.lastnames}",
                "total_vacation_days": employee.vacation_days,
                "approved_days": approved_days,
                "pending_days": pending_days,
                "available_days": employee.vacation_days - approved_days
            }, 200
            
        except SQLAlchemyError as e:
            return {"error": f"Error al obtener resumen: {str(e)}"}, 500