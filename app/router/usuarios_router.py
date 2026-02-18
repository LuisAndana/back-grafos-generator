from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import json
import os

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


# Modelos
class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    nombre: str
    apellido: str
    email: str
    password: str


# Archivo de datos
USERS_FILE = "usuarios.json"


# Funciones auxiliares
def cargar_usuarios():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}


def guardar_usuarios(usuarios):
    with open(USERS_FILE, 'w') as f:
        json.dump(usuarios, f, indent=4)


# Rutas
@router.post("/login")
def login(data: LoginRequest):
    usuarios = cargar_usuarios()

    if data.email not in usuarios:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    usuario = usuarios[data.email]
    if usuario['password'] != data.password:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return {
        "token": "fake-jwt-token",
        "usuario": {
            "email": usuario['email'],
            "nombre": usuario['nombre'],
            "apellido": usuario['apellido']
        }
    }


@router.post("/registro")
def registro(data: RegisterRequest):
    usuarios = cargar_usuarios()

    if data.email in usuarios:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    usuarios[data.email] = {
        "email": data.email,
        "nombre": data.nombre,
        "apellido": data.apellido,
        "password": data.password,
        "fechaRegistro": datetime.now().isoformat()
    }

    guardar_usuarios(usuarios)

    return {
        "token": "fake-jwt-token",
        "usuario": {
            "email": data.email,
            "nombre": data.nombre,
            "apellido": data.apellido
        }
    }


@router.get("/perfil/{email}")
def obtener_perfil(email: str):
    usuarios = cargar_usuarios()

    if email not in usuarios:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario = usuarios[email]
    return {
        "email": usuario['email'],
        "nombre": usuario['nombre'],
        "apellido": usuario['apellido'],
        "fechaRegistro": usuario.get('fechaRegistro')
    }