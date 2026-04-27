from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from app.database.connection import Base
from app.models.usuario import Usuario


class DiagramType(str, Enum):
    """Tipos de diagramas UML soportados"""
    CLASS = "class"
    SEQUENCE = "sequence"
    PACKAGE = "package"
    USECASE = "usecase"


class Diagram(Base):
    """Modelo para diagrama UML"""
    __tablename__ = "diagramas"

    id = Column(String(36), primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nombre = Column(String(255), nullable=False)
    tipo = Column(SQLEnum(DiagramType), nullable=False)
    descripcion = Column(Text, nullable=True)

    # Datos del diagrama (JSON serializado)
    elementos = Column(JSON, default=list)  # Lista de DiagramElement
    conexiones = Column(JSON, default=list)  # Lista de DiagramConnection
    vista_actual = Column(JSON, default=dict)  # ViewTransform

    # Metadatos
    creado_en = Column(DateTime, default=datetime.utcnow, nullable=False)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    creado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Relaciones
    proyecto = relationship("Usuario", foreign_keys=[proyecto_id])
    autor = relationship("Usuario", foreign_keys=[creado_por])

    class Config:
        from_attributes = True


class DiagramElement(Base):
    """Modelo para elementos del diagrama"""
    __tablename__ = "diagram_elementos"

    id = Column(String(36), primary_key=True, index=True)
    diagrama_id = Column(String(36), ForeignKey("diagramas.id"), nullable=False)
    tipo = Column(String(50), nullable=False)  # class, interface, enum, actor, etc
    nombre = Column(String(255), nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    ancho = Column(Integer, nullable=True)
    alto = Column(Integer, nullable=True)
    color = Column(String(7), default="#3b82f6")

    # Propiedades específicas (JSON)
    propiedades = Column(JSON, default=dict)  # atributos, métodos, etc

    creado_en = Column(DateTime, default=datetime.utcnow, nullable=False)

    class Config:
        from_attributes = True


class DiagramConnection(Base):
    """Modelo para conexiones entre elementos"""
    __tablename__ = "diagram_conexiones"

    id = Column(String(36), primary_key=True, index=True)
    diagrama_id = Column(String(36), ForeignKey("diagramas.id"), nullable=False)
    elemento_origen = Column(String(36), nullable=False)
    elemento_destino = Column(String(36), nullable=False)
    tipo = Column(String(50), nullable=False)  # inheritance, association, composition, etc
    etiqueta = Column(String(255), nullable=True)

    # Puntos de control para bezier curves
    puntos_control = Column(JSON, default=list)

    creado_en = Column(DateTime, default=datetime.utcnow, nullable=False)

    class Config:
        from_attributes = True
