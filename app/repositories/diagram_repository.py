from sqlalchemy.orm import Session
from app.models.diagram import Diagram, DiagramElement, DiagramConnection, DiagramType
from app.schemas.diagram import DiagramCreate, DiagramUpdate
from typing import List, Optional


class DiagramRepository:
    """Repositorio para operaciones de base de datos de diagramas"""

    @staticmethod
    def crear_diagrama(db: Session, diagrama_id: str, proyecto_id: int, usuario_id: int,
                       diagrama_create: DiagramCreate) -> Diagram:
        """Crear nuevo diagrama"""
        db_diagrama = Diagram(
            id=diagrama_id,
            proyecto_id=proyecto_id,
            nombre=diagrama_create.nombre,
            tipo=diagrama_create.tipo,
            descripcion=diagrama_create.descripcion,
            elementos=[],
            conexiones=[],
            vista_actual={"scale": 1.0, "translateX": 0, "translateY": 0},
            creado_por=usuario_id
        )
        db.add(db_diagrama)
        db.commit()
        db.refresh(db_diagrama)
        return db_diagrama

    @staticmethod
    def obtener_diagrama(db: Session, diagrama_id: str) -> Optional[Diagram]:
        """Obtener diagrama por ID"""
        return db.query(Diagram).filter(Diagram.id == diagrama_id).first()

    @staticmethod
    def obtener_diagramas_proyecto(db: Session, proyecto_id: int, skip: int = 0, limit: int = 100) -> List[Diagram]:
        """Obtener todos los diagramas de un proyecto"""
        return db.query(Diagram).filter(Diagram.proyecto_id == proyecto_id).offset(skip).limit(limit).all()

    @staticmethod
    def actualizar_diagrama(db: Session, diagrama_id: str, diagrama_update: DiagramUpdate) -> Optional[Diagram]:
        """Actualizar diagrama"""
        db_diagrama = DiagramRepository.obtener_diagrama(db, diagrama_id)
        if not db_diagrama:
            return None

        if diagrama_update.nombre:
            db_diagrama.nombre = diagrama_update.nombre
        if diagrama_update.descripcion:
            db_diagrama.descripcion = diagrama_update.descripcion
        if diagrama_update.elementos:
            db_diagrama.elementos = [elem.dict() for elem in diagrama_update.elementos]
        if diagrama_update.conexiones:
            db_diagrama.conexiones = [conn.dict() for conn in diagrama_update.conexiones]
        if diagrama_update.vista_actual:
            db_diagrama.vista_actual = diagrama_update.vista_actual.dict()

        db.add(db_diagrama)
        db.commit()
        db.refresh(db_diagrama)
        return db_diagrama

    @staticmethod
    def eliminar_diagrama(db: Session, diagrama_id: str) -> bool:
        """Eliminar diagrama"""
        db_diagrama = DiagramRepository.obtener_diagrama(db, diagrama_id)
        if not db_diagrama:
            return False

        db.delete(db_diagrama)
        db.commit()
        return True

    @staticmethod
    def contar_diagramas_proyecto(db: Session, proyecto_id: int) -> int:
        """Contar diagramas en un proyecto"""
        return db.query(Diagram).filter(Diagram.proyecto_id == proyecto_id).count()

    @staticmethod
    def obtener_diagramas_por_tipo(db: Session, proyecto_id: int, tipo: DiagramType) -> List[Diagram]:
        """Obtener diagramas de un tipo específico"""
        return db.query(Diagram).filter(
            Diagram.proyecto_id == proyecto_id,
            Diagram.tipo == tipo
        ).all()
