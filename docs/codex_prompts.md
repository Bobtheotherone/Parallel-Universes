# Codex Prompts for Parallel Universes

Below are comment templates that can be placed in source files. Codex will
expand them into functioning code.

## shared/schemas.py
```python
from pydantic import BaseModel
from typing import Literal, Dict, Any, List, Union

# Codex Prompt:
# """
# Define a Pydantic model `PlayerAction` with:
#   - actor_id: str
#   - verb: Literal["move", "plant_flower", "open_door"]
#   - params: Dict[str, Any]
# Define a model `TileChange` with x, y and new_type (same literals as above).
# Define `WorldDelta` with a list of TileChange and a list of event flag names.
# Define `SyncMessage` with fields `type` ("action" or "update") and `data`
#   containing either a PlayerAction or WorldDelta.
# """
```

## shared/protocol.py
```python
import json
from typing import Union
from .schemas import PlayerAction, WorldDelta, SyncMessage

# Codex Prompt:
# """
# Implement two functions:
#   1. serialize_message(message: Union[PlayerAction, WorldDelta], msg_type: str) -> str
#       - Return a JSON string with keys "type" and "data".
#   2. deserialize_message(raw: str) -> SyncMessage
#       - Parse JSON and return a SyncMessage instance populated with
#         PlayerAction or WorldDelta depending on the "type" field.
# """
```

## server/models.py
```python
from typing import Dict, Tuple, List
import threading
from shared.schemas import PlayerAction, TileChange, WorldDelta

# Codex Prompt:
# """
# Create a thread-safe singleton class `WorldState` with attributes:
#   tiles: Dict[Tuple[int,int], str]
#   event_flags: Dict[str, bool]
#   lock: threading.Lock
# Methods:
#   apply_action(action: PlayerAction) -> None
#   compute_delta(previous_snapshot: Dict) -> WorldDelta
#   get_snapshot() -> Dict
# The apply_action method should handle verbs "move", "plant_flower", "open_door"
# as described in the design doc. compute_delta compares current state with the
# previous snapshot and returns only the changes.
# """
```

## server/router.py
```python
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
```

## client/network.py
```python
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
```

## client/game.py
```python
import pygame
import asyncio
import threading
from typing import Dict
from shared.schemas import PlayerAction, WorldDelta
from client.network import NetworkClient
from client.settings import WS_ENDPOINT, REST_ENDPOINT, SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, FPS
from shared.utils import draw_tile

# Codex Prompt:
# """
# Implement Game class with methods:
#   async setup()
#   def process_input()
#   def apply_delta(delta: WorldDelta)
#   def render()
#   def run()
# The game should render the tile grid and send actions based on key presses.
# """
```

## client/main.py
```python
import argparse
import uuid
from client.game import Game

# Codex Prompt:
# """
# Parse optional --player-id. Generate a UUID if missing and start the Game.
# """
```
