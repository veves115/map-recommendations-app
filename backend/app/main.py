from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, maps
from app.api import preferences, locations, recommendations, messages, friendships
from app.websocket.chat import router as ws_router
from app.websocket.presence import router as presence_router
from sqlalchemy import text
from app.core import database
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

import os
app = FastAPI(
    title="Map Recommendations API",
    description="API para recomendaciones basadas en ubicacion",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


cors_origins_env = os.getenv("CORS_ORIGINS", "")
allow_origins = (
    [o.strip() for o in cors_origins_env.split(",") if o.strip()]
    if cors_origins_env
    else ["*"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
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
app.include_router(presence_router)
app.include_router(friendships.router, prefix="/api/v1")



@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a mi app",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    db = next(database.get_db())
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    return {"status": "healthy", "database": db_status}
        
