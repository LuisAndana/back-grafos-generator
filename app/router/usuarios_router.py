from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioLogin,
    UsuarioResponse,
    UsuarioUpdate,
    LoginResponse,
    RegisterResponse
)
from app.services import usuario_service
from app.utils.auth import create_access_token, validate_token

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


# ============================================
# RUTAS DE AUTENTICACIÓN
# ============================================

@router.post("/registro", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Registrar nuevo usuario
    """
    # Verificar si el email ya existe
    db_usuario = usuario_service.get_usuario_by_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario con este email ya existe"
        )

    # Crear usuario
    nuevo_usuario = usuario_service.create_usuario(db=db, usuario=usuario)

    # Crear token
    access_token = create_access_token(data={"sub": nuevo_usuario.email})

    # Preparar respuesta
    usuario_dict = {
        "email": nuevo_usuario.email,
        "nombre": nuevo_usuario.nombre,
        "apellido": nuevo_usuario.apellido,
        "rol": nuevo_usuario.rol.value if hasattr(nuevo_usuario.rol, 'value') else nuevo_usuario.rol,
        "fechaRegistro": nuevo_usuario.fecha_registro.isoformat()
    }

    return RegisterResponse(
        token=access_token,
        usuario=usuario_dict,
        message="Usuario registrado exitosamente"
    )


@router.post("/login", response_model=LoginResponse)
def login_usuario(credentials: UsuarioLogin, db: Session = Depends(get_db)):
    """
    Login de usuario
    """
    # Autenticar usuario
    usuario = usuario_service.authenticate_usuario(
        db=db,
        email=credentials.email,
        password=credentials.password
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    # Crear token
    access_token = create_access_token(data={"sub": usuario.email})

    # Preparar respuesta
    usuario_dict = {
        "email": usuario.email,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "rol": usuario.rol.value if hasattr(usuario.rol, 'value') else usuario.rol,
        "fechaLogin": usuario.fecha_ultimo_login.isoformat() if usuario.fecha_ultimo_login else None
    }

    return LoginResponse(
        token=access_token,
        usuario=usuario_dict,
        message="Login exitoso"
    )


@router.post("/verify-token")
def verificar_token(token_data: dict):
    """
    Verificar si un token es válido
    """
    token = token_data.get("token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token no proporcionado"
        )

    is_valid = validate_token(token)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )

    return {"valid": True}


# ============================================
# RUTAS DE USUARIOS (CRUD)
# ============================================

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener lista de usuarios
    """
    usuarios = usuario_service.get_usuarios(db, skip=skip, limit=limit)
    return usuarios


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """
    Obtener usuario por ID
    """
    usuario = usuario_service.get_usuario_by_id(db, usuario_id=usuario_id)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario


@router.put("/perfil", response_model=UsuarioResponse)
def actualizar_perfil(
        usuario_update: UsuarioUpdate,
        db: Session = Depends(get_db)
):
    """
    Actualizar perfil de usuario
    """
    # TODO: Implementar autenticación con token
    usuario_id = 1

    usuario = usuario_service.update_usuario(db, usuario_id=usuario_id, usuario_update=usuario_update)

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return usuario


@router.get("/count/total")
def contar_usuarios(db: Session = Depends(get_db)):
    """
    Contar usuarios activos
    """
    count = usuario_service.count_usuarios(db)
    return {"total": count}


# ============================================
# MANTENER COMPATIBILIDAD CON CÓDIGO ANTERIOR
# ============================================

@router.get("/perfil/{email}")
def obtener_perfil_por_email(email: str, db: Session = Depends(get_db)):
    """
    Obtener perfil de usuario por email (compatibilidad)
    """
    usuario = usuario_service.get_usuario_by_email(db, email=email)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return {
        "email": usuario.email,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "rol": usuario.rol.value if hasattr(usuario.rol, 'value') else usuario.rol,
        "fechaRegistro": usuario.fecha_registro.isoformat()
    }