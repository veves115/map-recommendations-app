from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    """
    Manages active WebSocket connections grouped by room_id.

    Each room_id maps to a list of WebSocket instances that are
    currently connected to that chat room. Supports connect,
    disconnect, and broadcast operations.
    """

    def __init__(self) -> None:
        # Maps room_id -> list of active WebSocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str) -> None:
        """
        Accept a new WebSocket connection and register it under room_id.

        Args:
            websocket: The incoming WebSocket connection to accept.
            room_id:   The chat room identifier (format: '{min_id}_{max_id}').
        """
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: str) -> None:
        """
        Remove a WebSocket connection from the given room.

        If the room becomes empty after removal, its entry is deleted
        from active_connections to avoid memory leaks.

        Args:
            websocket: The WebSocket connection that disconnected.
            room_id:   The chat room identifier the socket belonged to.
        """
        if room_id in self.active_connections:
            try:
                self.active_connections[room_id].remove(websocket)
            except ValueError:
                pass  # Already removed; safe to ignore
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast(self, room_id: str, message_json: str) -> None:
        """
        Send a JSON string to every active connection in the given room.

        Connections that fail to receive the message are silently skipped
        so that one broken socket does not interrupt delivery to others.

        Args:
            room_id:      The chat room to broadcast to.
            message_json: A JSON-serialised string to send as text.
        """
        connections = self.active_connections.get(room_id, [])
        for connection in connections:
            try:
                await connection.send_text(message_json)
            except Exception:
                pass  # Connection may have closed between iteration steps


# Module-level singleton used by the chat endpoint
manager = ConnectionManager()
