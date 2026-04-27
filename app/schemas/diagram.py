from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class DiagramType(str, Enum):
    """Tipos de diagramas UML"""
    CLASS = "class"
    SEQUENCE = "sequence"
    PACKAGE = "package"
    USECASE = "usecase"


# ========================================
# ESQUEMAS DE ELEMENTOS Y CONEXIONES
# ========================================

class DiagramElementCreate(BaseModel):
    """Schema para crear elemento en diagrama"""
    id: str
    tipo: str
    nombre: str
    x: int
    y: int
    ancho: Optional[int] = None
    alto: Optional[int] = None
    color: Optional[str] = "#3b82f6"
    propiedades: Optional[Dict[str, Any]] = {}

    class Config:
        schema_extra = {
            "example": {
                "id": "elem-1",
                "tipo": "class",
                "nombre": "Usuario",
                "x": 100,
                "y": 50,
                "ancho": 200,
                "alto": 250,
                "color": "#3b82f6",
                "propiedades": {
                    "atributos": ["id: int", "nombre: string"],
                    "metodos": ["getId(): int", "setNombre(string)"]
                }
            }
        }


class DiagramConnectionCreate(BaseModel):
    """Schema para crear conexión entre elementos"""
    id: str
    elemento_origen: str
    elemento_destino: str
    tipo: str
    etiqueta: Optional[str] = None
    puntos_control: Optional[List[Dict[str, int]]] = []

    class Config:
        schema_extra = {
            "example": {
                "id": "conn-1",
                "elemento_origen": "elem-1",
                "elemento_destino": "elem-2",
                "tipo": "inheritance",
                "etiqueta": None,
                "puntos_control": []
            }
        }


class ViewTransform(BaseModel):
    """Schema para la transformación de vista (pan, zoom)"""
    scale: float = 1.0
    translateX: float = 0
    translateY: float = 0

    class Config:
        schema_extra = {
            "example": {
                "scale": 1.0,
                "translateX": 0,
                "translateY": 0
            }
        }


# ========================================
# ESQUEMAS DE REQUEST - DIAGRAMA
# ========================================

class DiagramCreate(BaseModel):
    """Schema para crear nuevo diagrama"""
    nombre: str
    tipo: DiagramType
    descripcion: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "nombre": "Diagrama de Clases - Usuario",
                "tipo": "class",
                "descripcion": "Diagrama que muestra las clases del módulo de usuarios"
            }
        }


class DiagramUpdate(BaseModel):
    """Schema para actualizar diagrama"""
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    elementos: Optional[List[DiagramElementCreate]] = None
    conexiones: Optional[List[DiagramConnectionCreate]] = None
    vista_actual: Optional[ViewTransform] = None

    class Config:
        schema_extra = {
            "example": {
                "nombre": "Diagrama de Clases Actualizado",
                "descripcion": "Descripción actualizada",
                "elementos": [],
                "conexiones": [],
                "vista_actual": {"scale": 1.2, "translateX": 50, "translateY": 0}
            }
        }


class DiagramExport(BaseModel):
    """Schema para exportar diagrama"""
    formato: str  # "png", "pdf", "svg", "json"
    escala: Optional[float] = 1.0

    class Config:
        schema_extra = {
            "example": {
                "formato": "png",
                "escala": 2.0
            }
        }


# ========================================
# ESQUEMAS DE RESPONSE - DIAGRAMA
# ========================================

class DiagramResponse(BaseModel):
    """Schema para respuesta de diagrama"""
    id: str
    proyecto_id: int
    nombre: str
    tipo: DiagramType
    descripcion: Optional[str] = None
    elementos: List[DiagramElementCreate] = []
    conexiones: List[DiagramConnectionCreate] = []
    vista_actual: Optional[ViewTransform] = None
    creado_en: datetime
    actualizado_en: datetime
    creado_por: int

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "diagram-123",
                "proyecto_id": 1,
                "nombre": "Diagrama de Clases",
                "tipo": "class",
                "descripcion": "Diagrama principal",
                "elementos": [],
                "conexiones": [],
                "vista_actual": {"scale": 1.0, "translateX": 0, "translateY": 0},
                "creado_en": "2024-01-15T10:30:00",
                "actualizado_en": "2024-01-20T14:45:00",
                "creado_por": 1
            }
        }


class DiagramListResponse(BaseModel):
    """Schema para listado de diagramas"""
    total: int
    items: List[DiagramResponse]

    class Config:
        schema_extra = {
            "example": {
                "total": 5,
                "items": []
            }
        }


class DiagramDeleteResponse(BaseModel):
    """Schema para respuesta de eliminación"""
    mensaje: str
    diagrama_id: str

    class Config:
        schema_extra = {
            "example": {
                "mensaje": "Diagrama eliminado exitosamente",
                "diagrama_id": "diagram-123"
            }
        }
