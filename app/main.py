from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.models import User, Message, Preference, Location
from app.api import auth, users, maps

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Map Recommendations API",
    description="API para recomendaciones basadas en ubicación",
    version="1.0.0"
)

# Configurar CORS (para que el frontend pueda conectarse)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica dominios concretos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(maps.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {
        "message": "holaaaaaaaaaa",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy","database": "connected"}
