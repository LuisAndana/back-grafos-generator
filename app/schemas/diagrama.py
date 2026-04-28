"""
Esquemas Pydantic para validación de datos de diagramas.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class MetadatosDiagrama(BaseModel):
    """Metadatos del diagrama para contexto de IA."""
    elementos: int = Field(0, description="Cantidad de elementos en el diagrama")
    relaciones: int = Field(0, description="Cantidad de relaciones/conexiones")
    tipos_elementos: List[str] = Field(default_factory=list, description="Tipos únicos de elementos")
    tipos_relaciones: List[str] = Field(default_factory=list, description="Tipos únicos de relaciones")
    extra: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Información adicional")


class DiagramaGuardadoCreate(BaseModel):
    """Esquema para crear un diagrama guardado."""
    tipo: str = Field(..., description="Tipo: 'class', 'sequence', 'package', 'usecase'")
    nombre: Optional[str] = Field(None, description="Nombre descriptivo del diagrama")
    metadatos: MetadatosDiagrama = Field(default_factory=MetadatosDiagrama)
    codigo_mermaid: Optional[str] = Field(None, description="Código Mermaid")


class DiagramaGuardadoUpdate(BaseModel):
    """Esquema para actualizar un diagrama guardado."""
    nombre: Optional[str] = None
    metadatos: Optional[MetadatosDiagrama] = None
    codigo_mermaid: Optional[str] = None


class DiagramaGuardadoResponse(BaseModel):
    """Esquema de respuesta para un diagrama."""
    id: int
    proyecto_id: int
    tipo: str
    nombre: Optional[str]
    metadatos: Dict[str, Any]
    creado_en: datetime
    actualizado_en: datetime

    class Config:
        from_attributes = True


class ContextoDiagramasResponse(BaseModel):
    """Esquema de respuesta para el contexto de diagramas de un proyecto."""
    total_diagramas: int = Field(description="Total de diagramas guardados")
    tipos_guardados: List[str] = Field(description="Tipos de diagramas que hay")
    elementos_totales: int = Field(description="Suma de elementos en todos los diagramas")
    relaciones_totales: int = Field(description="Suma de relaciones en todos los diagramas")
    diagramas: List[DiagramaGuardadoResponse] = Field(default_factory=list, description="Detalle de cada diagrama")


class ContextoResumenIA(BaseModel):
    """Contexto completo para pasar a la IA."""
    proyecto_id: int
    casos_uso: int = Field(description="Cantidad de casos de uso")
    stakeholders: int = Field(description="Cantidad de stakeholders")
    entrevistas: int = Field(description="Total de entrevistas")
    procesos: int = Field(description="Total de procesos")
    necesidades: int = Field(description="Total de necesidades")
    diagramas: ContextoDiagramasResponse = Field(description="Contexto de diagramas")
