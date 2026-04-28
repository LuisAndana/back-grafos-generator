"""
Modelo para almacenar diagramas UML guardados en la BD.
Metadatos serán usados como contexto en la generación de código.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey
from app.models.base import Base


class DiagramaGuardado(Base):
    """Almacena diagramas UML para usarlos como contexto en la IA."""

    __tablename__ = "diagramas_guardados"

    id = Column(Integer, primary_key=True, index=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"), nullable=False, index=True)
    tipo = Column(
        String(50),
        nullable=False,
        comment="Tipo de diagrama: 'class', 'sequence', 'package', 'usecase'"
    )
    nombre = Column(String(255), comment="Nombre del diagrama (ej: 'Diagrama de Clases - Usuarios')")

    # Metadatos para contexto
    metadatos = Column(
        JSON,
        default=dict,
        comment="Metadatos del diagrama: {elementos: 5, relaciones: 3, tipos_elementos: [...], tipos_relaciones: [...]}"
    )

    # Código del diagrama
    codigo_mermaid = Column(
        Text,
        nullable=True,
        comment="Código Mermaid del diagrama para regeneración"
    )

    # Timestamps
    creado_en = Column(DateTime, default=datetime.utcnow, index=True)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Índices compuestos para búsquedas rápidas
    __table_args__ = (
        {
            "indexes": [
                {"name": "ix_proyecto_tipo", "expressions": ["proyecto_id", "tipo"]}
            ]
        },
    )

    def __repr__(self):
        return f"<DiagramaGuardado(id={self.id}, proyecto_id={self.proyecto_id}, tipo={self.tipo})>"
