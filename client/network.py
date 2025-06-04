
import asyncio
import websockets
import requests
from typing import Callable
from shared.protocol import serialize_message, deserialize_message
from shared.schemas import PlayerAction, WorldDelta, SyncMessage

# Codex Prompt:
# """
# Implement NetworkClient with methods:
#   __init__(self, ws_url: str, rest_url: str)
#   async connect()
#   async send_action(action: PlayerAction)
#   async receive_loop(on_update: Callable[[WorldDelta], None])
#   def get_initial_world(self) -> dict
# """


class NetworkClient:
    def __init__(self, ws_url: str, rest_url: str):
        self.ws_url = ws_url
        self.rest_url = rest_url
        self.ws = None

    async def connect(self):
        if self.ws is None:
            self.ws = await websockets.connect(self.ws_url)
        return self.ws

    async def send_action(self, action: PlayerAction):
        await self.connect()
        await self.ws.send(serialize_message(action, "action"))

    async def receive_loop(self, on_update: Callable[[WorldDelta], None]):
        await self.connect()
        try:
            async for raw in self.ws:
                msg = deserialize_message(raw)
                if msg.type == "update" and isinstance(msg.data, WorldDelta):
                    on_update(msg.data)
        except Exception as e:
            print(f"WebSocket error: {e}")

    def get_initial_world(self) -> dict:
        resp = requests.get(f"{self.rest_url}/world")
        resp.raise_for_status()
        return resp.json()
