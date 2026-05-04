from datetime import datetime
from typing import Optional
from fastapi import WebSocket


class PresenceManager:
    def __init__(self):
        # user_id -> dict
        self._connections: dict[int, dict] = {}

    async def connect(
        self,
        user_id: int,
        username: str,
        websocket: WebSocket,
        friend_ids: set[int],
        share_location: bool,
    ) -> None:
        """Registra un nuevo usuario online. Cierra la conexión previa si existía."""
        # Si ya estaba conectado, cerrar la anterior
        existing = self._connections.get(user_id)
        if existing:
            try:
                await existing["websocket"].close(code=1000, reason="reconnected")
            except Exception:
                pass

        self._connections[user_id] = {
            "websocket": websocket,
            "username": username,
            "lat": None,
            "lng": None,
            "updated_at": None,
            "friend_ids": friend_ids,
            "share_location": share_location,
        }

        # Notificar a los amigos online de que estoy online (sin posición aún)
        # No mandamos nada hasta que tengamos posición real

    def disconnect(self, user_id: int) -> Optional[set[int]]:
        """Quita al usuario y devuelve sus friend_ids para notificar offline."""
        entry = self._connections.pop(user_id, None)
        if entry is None:
            return None
        return entry["friend_ids"]

    async def update_location(
        self, user_id: int, lat: float, lng: float
    ) -> None:
        """Actualiza posición y difunde a amigos online."""
        entry = self._connections.get(user_id)
        if entry is None:
            return
        if not entry["share_location"]:
            return  # no compartiendo, ignoramos

        entry["lat"] = lat
        entry["lng"] = lng
        entry["updated_at"] = datetime.now()

        message = {
            "type": "update",
            "user_id": user_id,
            "username": entry["username"],
            "lat": lat,
            "lng": lng,
            "updated_at": entry["updated_at"].isoformat(),
        }
        await self._broadcast_to_friends(user_id, message, entry["friend_ids"])

    async def get_snapshot_for(self, user_id: int) -> list[dict]:
        """Devuelve posiciones actuales de los amigos online del user."""
        entry = self._connections.get(user_id)
        if entry is None:
            return []
        snapshot = []
        for fid in entry["friend_ids"]:
            friend = self._connections.get(fid)
            if friend is None:
                continue
            if not friend["share_location"]:
                continue
            if friend["lat"] is None or friend["lng"] is None:
                continue  # online pero aún sin posición
            snapshot.append({
                "user_id": fid,
                "username": friend["username"],
                "lat": friend["lat"],
                "lng": friend["lng"],
                "updated_at": friend["updated_at"].isoformat(),
            })
        return snapshot

    async def notify_offline(self, user_id: int, friend_ids: set[int]) -> None:
        """Notifica a los amigos que un user se ha desconectado."""
        message = {"type": "offline", "user_id": user_id}
        await self._broadcast_to_friends(user_id, message, friend_ids)

    async def _broadcast_to_friends(
        self, sender_id: int, message: dict, friend_ids: set[int]
    ) -> None:
        """Envía a cada amigo online (que comparta o no, da igual: recibe)."""
        for fid in friend_ids:
            friend_entry = self._connections.get(fid)
            if friend_entry is None:
                continue
            try:
                await friend_entry["websocket"].send_json(message)
            except Exception:
                # Conexión rota; ignoramos. El disconnect del WS la limpiará.
                pass


# Singleton
presence_manager = PresenceManager()
  