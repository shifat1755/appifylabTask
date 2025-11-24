from typing import Dict, Set

from fastapi import WebSocket


class ConnectionManager:
    """Manages WebSocket connections and broadcasts events."""

    def __init__(self):
        # Map of post_id -> set of WebSocket connections
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        # Map of user_id -> set of WebSocket connections
        self.user_connections: Dict[int, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, post_id: int, user_id: int):
        """Connect a user to a post's WebSocket channel."""
        await websocket.accept()

        if post_id not in self.active_connections:
            self.active_connections[post_id] = set()
        self.active_connections[post_id].add(websocket)

        if user_id not in self.user_connections:
            self.user_connections[user_id] = set()
        self.user_connections[user_id].add(websocket)

    def disconnect(self, websocket: WebSocket, post_id: int, user_id: int):
        """Disconnect a user from a post's WebSocket channel."""
        if post_id in self.active_connections:
            self.active_connections[post_id].discard(websocket)
            if not self.active_connections[post_id]:
                del self.active_connections[post_id]

        if user_id in self.user_connections:
            self.user_connections[user_id].discard(websocket)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific WebSocket connection."""
        try:
            await websocket.send_json(message)
        except Exception:
            pass  # Connection may be closed

    async def broadcast_to_post(self, post_id: int, message: dict):
        """Broadcast a message to all connections subscribed to a post."""
        if post_id not in self.active_connections:
            return

        disconnected = set()
        for connection in self.active_connections[post_id]:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.add(connection)

        # Clean up disconnected connections
        for connection in disconnected:
            self.active_connections[post_id].discard(connection)

    async def broadcast_to_user(self, user_id: int, message: dict):
        """Broadcast a message to all connections for a specific user."""
        if user_id not in self.user_connections:
            return

        disconnected = set()
        for connection in self.user_connections[user_id]:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.add(connection)

        # Clean up disconnected connections
        for connection in disconnected:
            self.user_connections[user_id].discard(connection)


# Global connection manager instance
manager = ConnectionManager()
