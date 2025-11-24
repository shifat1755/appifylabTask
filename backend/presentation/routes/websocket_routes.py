import json
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from infrastructure.websocket.manager import manager
from presentation.routes.dependencies import get_user_id_from_token

websocketRouter = APIRouter(tags=["WebSocket"])

logger = logging.getLogger(__name__)


@websocketRouter.websocket("/ws/posts/{post_id}")
async def websocket_endpoint(websocket: WebSocket, post_id: int):
    """
    WebSocket endpoint for real-time post updates.
    Clients can subscribe to a post to receive events like:
    - post: commented
    - post: liked
    - comment: replied
    - comment: liked
    """
    user_id = None

    # Try to get user from query parameter or header
    token = websocket.query_params.get("token") or websocket.headers.get(
        "Authorization", ""
    ).replace("Bearer ", "")
    if token:
        user_id = get_user_id_from_token(token)

    if user_id is None:
        await websocket.close(code=4001)
        return  # Unauthorized

    await manager.connect(websocket, post_id, user_id)

    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                # Handle client messages if needed (e.g., ping/pong)
                if message.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
            except json.JSONDecodeError:
                pass
    except WebSocketDisconnect:
        manager.disconnect(websocket, post_id, user_id or 0)
    except Exception:
        logger.exception("WebSocket error")
        manager.disconnect(websocket, post_id, user_id or 0)
