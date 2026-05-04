import logging
from sqlalchemy import or_
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query

from app.core.database import SessionLocal
from app.core.security import decode_access_token
from app.services.user_service import UserService
from app.models.friendship import Friendship, FriendshipStatus
from app.websocket.presence_manager import presence_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ws", tags=["WebSocket"])


def _authenticate(token: str):
    """Returns User or None."""
    payload = decode_access_token(token)
    if payload is None:
        return None
    email = payload.get("sub")
    if not email:
        return None
    db = SessionLocal()
    try:
        user = UserService.get_user_by_email(db, email)
        return user
    finally:
        db.close()


def _get_friend_ids(user_id: int) -> set[int]:
    """Devuelve los IDs de amigos aceptados del usuario."""
    db = SessionLocal()
    try:
        rows = db.query(Friendship).filter(
            or_(
                Friendship.requester_id == user_id,
                Friendship.addressee_id == user_id,
            ),
            Friendship.status == FriendshipStatus.accepted,
        ).all()
        ids: set[int] = set()
        for row in rows:
            other = row.addressee_id if row.requester_id == user_id else row.requester_id
            ids.add(other)
        return ids
    finally:
        db.close()


@router.websocket("/presence")
async def websocket_presence(
    websocket: WebSocket,
    token: str = Query(...),
):
    """
    WebSocket endpoint for live presence and location sharing.

    Auth:  ?token=<jwt>

    Client sends: {"type": "location", "lat": float, "lng": float}

    Server sends:
      - {"type": "snapshot", "friends": [{user_id, username, lat, lng, updated_at}, ...]}
      - {"type": "update", "user_id", "username", "lat", "lng", "updated_at"}
      - {"type": "offline", "user_id"}
    """
    # --- Auth ---
    current_user = _authenticate(token)
    if current_user is None or not current_user.is_active:
        await websocket.close(code=1008)
        return

    await websocket.accept()

    friend_ids = _get_friend_ids(current_user.id)

    # Registrar en el manager
    await presence_manager.connect(
        user_id=current_user.id,
        username=current_user.username,
        websocket=websocket,
        friend_ids=friend_ids,
        share_location=current_user.share_location,
    )

    # Enviar snapshot inicial de amigos online
    snapshot = await presence_manager.get_snapshot_for(current_user.id)
    await websocket.send_json({"type": "snapshot", "friends": snapshot})

    try:
        while True:
            data = await websocket.receive_json()
            if data.get("type") != "location":
                await websocket.send_json({"error": "Tipo desconocido"})
                continue

            try:
                lat = float(data["lat"])
                lng = float(data["lng"])
            except (KeyError, TypeError, ValueError):
                await websocket.send_json({"error": "lat/lng inválidos"})
                continue

            # Validación básica de rangos
            if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                await websocket.send_json({"error": "lat/lng fuera de rango"})
                continue

            await presence_manager.update_location(current_user.id, lat, lng)

    except WebSocketDisconnect:
        pass
    finally:
        ids = presence_manager.disconnect(current_user.id)
        if ids:
            await presence_manager.notify_offline(current_user.id, ids)
