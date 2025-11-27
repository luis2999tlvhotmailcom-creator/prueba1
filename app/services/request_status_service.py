# app/services/request_status_service.py
from app import db
from app.models.request_status import RequestStatus
from sqlalchemy.exc import SQLAlchemyError

class RequestStatusService:
    
    # ========================================
    # 📋 CREATE - Crear estado de solicitud
    # ========================================
    @staticmethod
    def create_status(data):
        """
        Crear un nuevo estado de solicitud
        
        Args:
            data (dict): {
                "state_request": "PENDIENTE",
                "description": "Solicitud pendiente de revisión"
            }
        """
        try:
            state_request = data.get("state_request")
            description = data.get("description")

            if not state_request:
                return {"error": "El campo 'state_request' es obligatorio"}, 400

            # Validar duplicado
            existing = RequestStatus.query.filter_by(state_request=state_request.upper()).first()
            if existing:
                return {"error": "El estado ya existe"}, 409

            new_status = RequestStatus(
                state_request=state_request.upper(),
                description=description
            )
            db.session.add(new_status)
            db.session.commit()

            return new_status.to_dict(), 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Error al crear estado: {str(e)}"}, 500

    # ========================================
    # 📋 READ - Listar todos los estados
    # ========================================
    @staticmethod
    def get_all_statuses():
        """
        Obtener todos los estados registrados
        """
        try:
            statuses = RequestStatus.query.order_by(RequestStatus.id).all()
            return [s.to_dict() for s in statuses], 200
        except SQLAlchemyError as e:
            return {"error": f"Error al listar estados: {str(e)}"}, 500

    # ========================================
    # 📋 READ - Obtener estado por ID
    # ========================================
    @staticmethod
    def get_status_by_id(status_id):
        """
        Obtener un estado específico por su ID
        """
        try:
            status = RequestStatus.query.get(status_id)
            if not status:
                return {"error": "Estado no encontrado"}, 404
            return status.to_dict(), 200
        except SQLAlchemyError as e:
            return {"error": f"Error al obtener estado: {str(e)}"}, 500

    # ========================================
    # 🔄 UPDATE - Actualizar estado existente
    # ========================================
    @staticmethod
    def update_status(status_id, data):
        """
        Actualizar un estado de solicitud existente
        """
        try:
            status = RequestStatus.query.get(status_id)
            if not status:
                return {"error": "Estado no encontrado"}, 404

            status.state_request = data.get("state_request", status.state_request)
            status.description = data.get("description", status.description)

            db.session.commit()
            return status.to_dict(), 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Error al actualizar estado: {str(e)}"}, 500

    # ========================================
    # ❌ DELETE - Eliminar estado (solo pruebas)
    # ========================================
    @staticmethod
    def delete_status(status_id):
        """
        Eliminar físicamente un estado de solicitud
        ADVERTENCIA: Solo para desarrollo/pruebas
        """
        try:
            status = RequestStatus.query.get(status_id)
            if not status:
                return {"error": "Estado no encontrado"}, 404

            db.session.delete(status)
            db.session.commit()

            return {"message": "Estado eliminado correctamente"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Error al eliminar estado: {str(e)}"}, 500