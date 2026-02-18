from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.usuarios_router import router as usuarios_router

app = FastAPI(
    title="Grafo Generator API",
    description="API para el generador de grafos",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(usuarios_router)

# Ruta de prueba
@app.get("/")
def root():
    return {"mensaje": "Bienvenido a Grafo Generator API"}

@app.get("/api/datos")
def obtener_datos():
    return {"mensaje": "¡Hola desde FastAPI!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)