from fastapi import APIRouter, Depends, HTTPException, status, Header, Path, Query
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.diagram import (
    DiagramCreate, DiagramUpdate, DiagramResponse, DiagramListResponse, DiagramDeleteResponse
)
from app.services.diagram_service import DiagramService
from app.utils.auth import verify_token

router = APIRouter(
    prefix="/api/v1/diagramas",
    tags=["diagramas"],
    responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=DiagramResponse, status_code=status.HTTP_201_CREATED)
def crear_diagrama(
    proyecto_id: int = Query(..., description="ID del proyecto", gt=0),
    diagrama_create: DiagramCreate = None,
    db: Session = Depends(get_db),
    authorization: str = Header(None),
):
    """
    Crear nuevo diagrama para un proyecto

    - **proyecto_id**: ID del proyecto
    - **diagrama_create**: Datos del diagrama a crear
    """
    token = verify_token(authorization)
    usuario_id = token.get("sub")
    if not usuario_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    diagrama = DiagramService.crear_diagrama(
        db=db,
        proyecto_id=proyecto_id,
        usuario_id=usuario_id,
        diagrama_create=diagrama_create
    )
    return diagrama


@router.get("/{diagrama_id}", response_model=DiagramResponse)
def obtener_diagrama(
    diagrama_id: str = Path(..., description="ID del diagrama"),
    proyecto_id: int = Query(..., description="ID del proyecto", gt=0),
    db: Session = Depends(get_db),
    authorization: str = Header(None),
):
    """
    Obtener diagrama específico

    - **diagrama_id**: ID del diagrama
    - **proyecto_id**: ID del proyecto
    """
    token = verify_token(authorization)
    diagrama = DiagramService.obtener_diagrama(db, diagrama_id, proyecto_id)
    if not diagrama:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diagrama no encontrado")
    return diagrama


@router.get("/proyecto/{proyecto_id}", response_model=DiagramListResponse)
def listar_diagramas(
    proyecto_id: int = Path(..., description="ID del proyecto", gt=0),
    skip: int = Query(0, description="Número de registros a saltar", ge=0),
    limit: int = Query(100, description="Número máximo de registros", ge=1, le=1000),
    db: Session = Depends(get_db),
    authorization: str = Header(None),
):
    """
    Listar todos los diagramas de un proyecto

    - **proyecto_id**: ID del proyecto
    - **skip**: Número de registros a saltar
    - **limit**: Número máximo de registros
    """
    token = verify_token(authorization)
    return DiagramService.listar_diagramas(db, proyecto_id, skip, limit)


@router.put("/{diagrama_id}", response_model=DiagramResponse)
def actualizar_diagrama(
    diagrama_id: str = Path(..., description="ID del diagrama"),
    proyecto_id: int = Query(..., description="ID del proyecto", gt=0),
    diagrama_update: DiagramUpdate = None,
    db: Session = Depends(get_db),
    authorization: str = Header(None),
):
    """
    Actualizar diagrama

    - **diagrama_id**: ID del diagrama
    - **proyecto_id**: ID del proyecto
    - **diagrama_update**: Datos a actualizar
    """
    token = verify_token(authorization)
    diagrama = DiagramService.actualizar_diagrama(db, diagrama_id, proyecto_id, diagrama_update)
    if not diagrama:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diagrama no encontrado")
    return diagrama


@router.delete("/{diagrama_id}", response_model=DiagramDeleteResponse)
def eliminar_diagrama(
    diagrama_id: str = Path(..., description="ID del diagrama"),
    proyecto_id: int = Query(..., description="ID del proyecto", gt=0),
    db: Session = Depends(get_db),
    authorization: str = Header(None),
):
    """
    Eliminar diagrama

    - **diagrama_id**: ID del diagrama
    - **proyecto_id**: ID del proyecto
    """
    token = verify_token(authorization)
    success = DiagramService.eliminar_diagrama(db, diagrama_id, proyecto_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diagrama no encontrado")
    return DiagramDeleteResponse(
        mensaje="Diagrama eliminado exitosamente",
        diagrama_id=diagrama_id
    )


@router.get("/proyecto/{proyecto_id}/tipo/{tipo}", response_model=list[DiagramResponse])
def listar_diagramas_por_tipo(
    proyecto_id: int = Path(..., description="ID del proyecto", gt=0),
    tipo: str = Path(..., description="Tipo de diagrama"),
    db: Session = Depends(get_db),
    authorization: str = Header(None),
):
    """
    Listar diagramas por tipo

    - **proyecto_id**: ID del proyecto
    - **tipo**: Tipo de diagrama (class, sequence, package, usecase)
    """
    token = verify_token(authorization)
    diagramas = DiagramService.listar_diagramas_por_tipo(db, proyecto_id, tipo)
    return diagramas


@router.patch("/{diagrama_id}/guardar-estado", response_model=DiagramResponse)
def guardar_estado_diagrama(
    diagrama_id: str = Path(..., description="ID del diagrama"),
    proyecto_id: int = Query(..., description="ID del proyecto", gt=0),
    datos: dict = None,
    db: Session = Depends(get_db),
    authorization: str = Header(None),
):
    """
    Guardar estado completo del diagrama (elementos, conexiones, vista)

    - **diagrama_id**: ID del diagrama
    - **proyecto_id**: ID del proyecto
    - **datos**: {elementos: [], conexiones: [], vista_actual: {}}
    """
    token = verify_token(authorization)
    diagrama = DiagramService.guardar_estado_diagrama(
        db=db,
        diagrama_id=diagrama_id,
        proyecto_id=proyecto_id,
        elementos=datos.get("elementos", []),
        conexiones=datos.get("conexiones", []),
        vista_actual=datos.get("vista_actual", {})
    )
    if not diagrama:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diagrama no encontrado")
    return diagrama
