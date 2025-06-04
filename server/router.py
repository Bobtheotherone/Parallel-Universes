
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict
from shared.protocol import serialize_message, deserialize_message
from shared.schemas import PlayerAction, WorldDelta, SyncMessage
from server.models import WorldState

# Codex Prompt:
# """
# Implement a GET /world endpoint returning world.get_snapshot().
# Implement a WebSocket endpoint /ws that accepts connections, receives
# action messages, updates the world and broadcasts update messages to all
# connected clients.
# """

router = APIRouter()
world = WorldState()
active_connections: List[WebSocket] = []
client_snapshots: Dict[int, Dict] = {}


@router.get("/world")
async def get_world():
    return world.get_snapshot()


async def broadcast(message: str):
    to_remove = []
    for ws in active_connections:
        try:
            await ws.send_text(message)
        except Exception:
            to_remove.append(ws)
    for ws in to_remove:
        active_connections.remove(ws)
        client_snapshots.pop(id(ws), None)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    client_snapshots[id(websocket)] = world.get_snapshot()
    try:
        while True:
            raw = await websocket.receive_text()
            msg = deserialize_message(raw)
            if msg.type == "action" and isinstance(msg.data, PlayerAction):
                world.apply_action(msg.data)
                for ws in list(active_connections):
                    prev = client_snapshots.get(id(ws), world.get_snapshot())
                    delta = world.compute_delta(prev)
                    client_snapshots[id(ws)] = world.get_snapshot()
                    await ws.send_text(serialize_message(delta, "update"))
    except WebSocketDisconnect:
        pass
    finally:
        if websocket in active_connections:
            active_connections.remove(websocket)
            client_snapshots.pop(id(websocket), None)
