import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.core.database import SessionLocal
from app.core.security import decode_access_token
from app.services.user_service import UserService
from app.services.message_service import MessageService
from app.schemas.message import MessageCreate
from app.websocket.manager import manager
from app.services.user_service import UserService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ws", tags=["WebSocket"])


def _get_room_id(user_id_a: int, user_id_b: int) -> str:
    """Returns canonical room_id with smaller ID first."""
    lo, hi = sorted([user_id_a, user_id_b])
    return f"{lo}_{hi}"


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


@router.websocket("/chat/{room_id}")
async def websocket_chat(
    websocket: WebSocket,
    room_id: str,
    token: str = Query(...),
):
    """
    WebSocket endpoint for real-time chat.

    room_id format: '{min_user_id}_{max_user_id}'  e.g. '1_3'
    Auth:  ?token=<jwt>

    Client sends:  {"receiver_id": 3, "content": "Hello!"}
    Server broadcasts: {"id": 1, "sender_id": 1, "receiver_id": 3,
                        "content": "Hello!", "timestamp": "...", "is_read": false}
    """
    # --- Authentication ---
    current_user = _authenticate(token)
    if current_user is None or not current_user.is_active:
        await websocket.close(code=1008)
        return

    # --- Validate room membership ---
    try:
        parts = room_id.split("_")
        if len(parts) != 2:
            raise ValueError
        id_a, id_b = int(parts[0]), int(parts[1])
    except (ValueError, IndexError):
        await websocket.close(code=1008)
        return

    if current_user.id not in (id_a, id_b):
        await websocket.close(code=1008)
        return

    # --- Connect ---
    await manager.connect(websocket, room_id)

    db = SessionLocal()
    try:
        while True:
            raw = await websocket.receive_text()

            try:
                data = json.loads(raw)
                receiver_id = int(data["receiver_id"])
                content = str(data["content"]).strip()
                if not content:
                    raise ValueError("empty content")
            except (KeyError, ValueError, TypeError):
                await websocket.send_text(
                    json.dumps({"error": "Formato inválido. Usa {\"receiver_id\": int, \"content\": str}"})
                )
                continue

            if receiver_id == current_user.id:
                await websocket.send_text(
                    json.dumps({"error": "No puedes enviarte un mensaje a ti mismo"})
                )
                continue
            
            UserService.get_user_by_id(db,receiver_id)
            receiver  = UserService.get_user_by_id(db,receiver_id)
            if not receiver:
                await websocket.send_text(json.dumps({"error": "Usuario receptor no existe"}))
                continue
            
            # Persist
            msg = MessageService.create_message(
                db,
                sender_id=current_user.id,
                message_data=MessageCreate(receiver_id=receiver_id, content=content),
            )

            # Broadcast to room
            payload = json.dumps({
                "id": msg.id,
                "sender_id": msg.sender_id,
                "receiver_id": msg.receiver_id,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "is_read": msg.is_read,
            })
            await manager.broadcast(room_id, payload)

    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
    finally:
        db.close()
