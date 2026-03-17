from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, maps
from app.api import preferences, locations, recommendations, messages
from app.websocket.chat import router as ws_router


app = FastAPI(
    title="Map Recommendations API",
    description="API para recomendaciones basadas en ubicacion",
    version="1.0.0"
)

# Configurar CORS (para que el frontend pueda conectarse)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En produccion, especifica dominios concretos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(maps.router, prefix="/api/v1")
app.include_router(preferences.router, prefix="/api/v1")
app.include_router(locations.router, prefix="/api/v1")
app.include_router(recommendations.router, prefix="/api/v1")
app.include_router(messages.router, prefix="/api/v1")
app.include_router(ws_router)


@app.get("/")
def read_root():
    return {
        "message": "holaaaaaaaaaa",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}
