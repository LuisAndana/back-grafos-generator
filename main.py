from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import sys
from pathlib import Path

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio raíz al path de Python
sys.path.insert(0, str(Path(__file__).parent))

# Imports desde app
from app.database.connection import engine, Base
from app.router.usuarios_router import router as usuarios_router
from app.api.v1.endpoints.diagramas import router as diagramas_router

# Importar modelos para crear tablas (orden importa por las relaciones)
from app.models.usuario import Usuario
from app.models.diagram import Diagram, DiagramElement, DiagramConnection


app = FastAPI(
    title="SRS Manager API",
    description="API para el generador de grafos y gestión de requisitos",
    version="1.0.0"
)

# ===============================
# Crear tablas al iniciar la app
# ===============================
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


# ===============================
# Configurar CORS
# ===============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://localhost:4000",
        "http://127.0.0.1:4200",
        "http://127.0.0.1:4000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# Incluir routers
# ===============================
app.include_router(usuarios_router)
app.include_router(diagramas_router)


# ===============================
# Rutas básicas
# ===============================

@app.get("/")
def root():
    return {
        "mensaje": "Bienvenido a SRS Manager API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/api/datos")
def obtener_datos():
    return {"mensaje": "¡Hola desde FastAPI!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)