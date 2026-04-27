from sqlalchemy.orm import Session
from app.models.diagram import Diagram, DiagramType
from app.schemas.diagram import DiagramCreate, DiagramUpdate, DiagramResponse, DiagramListResponse
from app.repositories.diagram_repository import DiagramRepository
from uuid import uuid4
from typing import List, Optional


class DiagramService:
    """Servicio para operaciones de diagramas"""

    @staticmethod
    def crear_diagrama(db: Session, proyecto_id: int, usuario_id: int, diagrama_create: DiagramCreate) -> DiagramResponse:
        """Crear nuevo diagrama"""
        diagrama_id = str(uuid4())
        diagrama = DiagramRepository.crear_diagrama(
            db=db,
            diagrama_id=diagrama_id,
            proyecto_id=proyecto_id,
            usuario_id=usuario_id,
            diagrama_create=diagrama_create
        )
        return DiagramResponse.from_orm(diagrama)

    @staticmethod
    def obtener_diagrama(db: Session, diagrama_id: str, proyecto_id: int) -> Optional[DiagramResponse]:
        """Obtener diagrama por ID (verificar que pertenezca al proyecto)"""
        diagrama = DiagramRepository.obtener_diagrama(db, diagrama_id)
        if not diagrama or diagrama.proyecto_id != proyecto_id:
            return None
        return DiagramResponse.from_orm(diagrama)

    @staticmethod
    def listar_diagramas(db: Session, proyecto_id: int, skip: int = 0, limit: int = 100) -> DiagramListResponse:
        """Listar todos los diagramas de un proyecto"""
        diagramas = DiagramRepository.obtener_diagramas_proyecto(db, proyecto_id, skip, limit)
        total = DiagramRepository.contar_diagramas_proyecto(db, proyecto_id)
        items = [DiagramResponse.from_orm(d) for d in diagramas]
        return DiagramListResponse(total=total, items=items)

    @staticmethod
    def actualizar_diagrama(db: Session, diagrama_id: str, proyecto_id: int,
                            diagrama_update: DiagramUpdate) -> Optional[DiagramResponse]:
        """Actualizar diagrama"""
        diagrama = DiagramRepository.obtener_diagrama(db, diagrama_id)
        if not diagrama or diagrama.proyecto_id != proyecto_id:
            return None

        diagrama_actualizado = DiagramRepository.actualizar_diagrama(db, diagrama_id, diagrama_update)
        if not diagrama_actualizado:
            return None

        return DiagramResponse.from_orm(diagrama_actualizado)

    @staticmethod
    def eliminar_diagrama(db: Session, diagrama_id: str, proyecto_id: int) -> bool:
        """Eliminar diagrama"""
        diagrama = DiagramRepository.obtener_diagrama(db, diagrama_id)
        if not diagrama or diagrama.proyecto_id != proyecto_id:
            return False

        return DiagramRepository.eliminar_diagrama(db, diagrama_id)

    @staticmethod
    def listar_diagramas_por_tipo(db: Session, proyecto_id: int, tipo: str) -> List[DiagramResponse]:
        """Listar diagramas por tipo"""
        try:
            tipo_enum = DiagramType(tipo)
        except ValueError:
            return []

        diagramas = DiagramRepository.obtener_diagramas_por_tipo(db, proyecto_id, tipo_enum)
        return [DiagramResponse.from_orm(d) for d in diagramas]

    @staticmethod
    def guardar_estado_diagrama(db: Session, diagrama_id: str, proyecto_id: int,
                                elementos: List, conexiones: List, vista_actual: dict) -> Optional[DiagramResponse]:
        """Guardar estado completo del diagrama"""
        diagrama_update = DiagramUpdate(
            elementos=elementos,
            conexiones=conexiones,
            vista_actual=vista_actual
        )
        return DiagramService.actualizar_diagrama(db, diagrama_id, proyecto_id, diagrama_update)
