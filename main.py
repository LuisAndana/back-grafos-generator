from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Imports desde app
from app.database.connection import engine, Base
from app.router.usuarios_router import router as usuarios_router


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
