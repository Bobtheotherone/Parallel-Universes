
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

class PlayerAction(BaseModel):
    actor_id: str
    verb: Literal["move", "plant_flower", "open_door"]
    params: Dict[str, Any]


class TileChange(BaseModel):
    x: int
    y: int
    new_type: Literal["empty", "grass", "flower", "door", "door_open"]


class WorldDelta(BaseModel):
    tile_changes: List[TileChange] = []
    event_flags: List[str] = []


class SyncMessage(BaseModel):
    type: Literal["action", "update"]
    data: Union[PlayerAction, WorldDelta]
