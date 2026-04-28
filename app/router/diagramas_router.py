"""
Router para gestionar diagramas UML guardados.
Endpoints para guardar, obtener y usar metadatos como contexto para la IA.
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from typing import List, Optional
import json

from app.models.diagrama_guardado import DiagramaGuardado
from app.schemas.diagrama import (
    DiagramaGuardadoCreate,
    DiagramaGuardadoUpdate,
    DiagramaGuardadoResponse,
    ContextoDiagramasResponse,
    MetadatosDiagrama,
)
from app.dependencies import get_db

router = APIRouter(prefix="/api/diagramas", tags=["diagramas"])


@router.post(
    "/{proyecto_id}",
    response_model=DiagramaGuardadoResponse,
    summary="Guardar o actualizar un diagrama",
    description="Guarda los metadatos de un diagrama para usarlos como contexto en la generación de código"
)
def guardar_diagrama(
    proyecto_id: int,
    diagrama_data: DiagramaGuardadoCreate,
    db: Session = Depends(get_db)
) -> DiagramaGuardadoResponse:
    """
    Guarda un diagrama en la BD.
    Si ya existe uno del mismo tipo para este proyecto, lo actualiza.
    """
    # Verificar si ya existe un diagrama de este tipo para este proyecto
    diagrama_existente = db.query(DiagramaGuardado).filter(
        DiagramaGuardado.proyecto_id == proyecto_id,
        DiagramaGuardado.tipo == diagrama_data.tipo
    ).first()

    if diagrama_existente:
        # Actualizar
        diagrama_existente.nombre = diagrama_data.nombre or diagrama_existente.nombre
        diagrama_existente.metadatos = diagrama_data.metadatos.dict()
        diagrama_existente.codigo_mermaid = diagrama_data.codigo_mermaid or diagrama_existente.codigo_mermaid
        diagrama_existente.actualizado_en = datetime.utcnow()
        db.add(diagrama_existente)
    else:
        # Crear nuevo
        diagrama = DiagramaGuardado(
            proyecto_id=proyecto_id,
            tipo=diagrama_data.tipo,
            nombre=diagrama_data.nombre,
            metadatos=diagrama_data.metadatos.dict(),
            codigo_mermaid=diagrama_data.codigo_mermaid,
        )
        db.add(diagrama)

    db.commit()
    diagrama = diagrama_existente if diagrama_existente else diagrama
    db.refresh(diagrama)

    return DiagramaGuardadoResponse.from_orm(diagrama)


@router.get(
    "/contexto/{proyecto_id}",
    response_model=ContextoDiagramasResponse,
    summary="Obtener contexto de diagramas",
    description="Obtiene un resumen de todos los diagramas guardados para un proyecto"
)
def obtener_contexto_diagramas(
    proyecto_id: int,
    db: Session = Depends(get_db)
) -> ContextoDiagramasResponse:
    """
    Retorna un resumen de los diagramas guardados para un proyecto.
    Usado como contexto adicional para la generación de código con IA.
    """
    diagramas = db.query(DiagramaGuardado).filter(
        DiagramaGuardado.proyecto_id == proyecto_id
    ).order_by(desc(DiagramaGuardado.actualizado_en)).all()

    # Calcular totales
    elementos_totales = sum(
        d.metadatos.get("elementos", 0) if d.metadatos else 0
        for d in diagramas
    )
    relaciones_totales = sum(
        d.metadatos.get("relaciones", 0) if d.metadatos else 0
        for d in diagramas
    )
    tipos_guardados = list(set(d.tipo for d in diagramas))

    return ContextoDiagramasResponse(
        total_diagramas=len(diagramas),
        tipos_guardados=tipos_guardados,
        elementos_totales=elementos_totales,
        relaciones_totales=relaciones_totales,
        diagramas=[DiagramaGuardadoResponse.from_orm(d) for d in diagramas]
    )


@router.get(
    "/{proyecto_id}",
    response_model=List[DiagramaGuardadoResponse],
    summary="Listar diagramas",
    description="Lista todos los diagramas guardados para un proyecto"
)
def listar_diagramas(
    proyecto_id: int,
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de diagrama"),
    db: Session = Depends(get_db)
) -> List[DiagramaGuardadoResponse]:
    """
    Lista los diagramas guardados para un proyecto.
    Opcionalmente filtra por tipo.
    """
    query = db.query(DiagramaGuardado).filter(
        DiagramaGuardado.proyecto_id == proyecto_id
    )

    if tipo:
        query = query.filter(DiagramaGuardado.tipo == tipo)

    diagramas = query.order_by(desc(DiagramaGuardado.actualizado_en)).all()

    return [DiagramaGuardadoResponse.from_orm(d) for d in diagramas]


@router.delete(
    "/{proyecto_id}/{tipo}",
    summary="Eliminar diagrama",
    description="Elimina un diagrama específico de un proyecto"
)
def eliminar_diagrama(
    proyecto_id: int,
    tipo: str,
    db: Session = Depends(get_db)
) -> dict:
    """
    Elimina un diagrama de un proyecto.
    """
    diagrama = db.query(DiagramaGuardado).filter(
        DiagramaGuardado.proyecto_id == proyecto_id,
        DiagramaGuardado.tipo == tipo
    ).first()

    if not diagrama:
        raise HTTPException(status_code=404, detail="Diagrama no encontrado")

    db.delete(diagrama)
    db.commit()

    return {"mensaje": f"Diagrama {tipo} eliminado correctamente"}
