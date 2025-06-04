
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


def serialize_message(message: Union[PlayerAction, WorldDelta], msg_type: str) -> str:
    payload = {
        "type": msg_type,
        "data": message.model_dump(),
    }
    return json.dumps(payload)


def deserialize_message(raw: str) -> SyncMessage:
    obj = json.loads(raw)
    msg_type = obj.get("type")
    data = obj.get("data", {})
    if msg_type == "action":
        parsed = PlayerAction(**data)
    else:
        parsed = WorldDelta(**data)
    return SyncMessage(type=msg_type, data=parsed)
