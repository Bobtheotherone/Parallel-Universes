
from typing import Dict, Tuple
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


class WorldState:
    _instance = None
    _singleton_lock = threading.Lock()

    def __new__(cls):
        with cls._singleton_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init_state()
            return cls._instance

    def _init_state(self):
        self.tiles: Dict[Tuple[int, int], str] = {}
        self.event_flags: Dict[str, bool] = {}
        self.lock = threading.Lock()
        for x in range(50):
            for y in range(50):
                self.tiles[(x, y)] = "empty"

    def apply_action(self, action: PlayerAction) -> None:
        with self.lock:
            if action.verb == "plant_flower":
                x = int(action.params.get("x", 0))
                y = int(action.params.get("y", 0))
                self.tiles[(x, y)] = "flower"
                self.event_flags["flower_planted"] = True
            elif action.verb == "open_door":
                x = int(action.params.get("x", 0))
                y = int(action.params.get("y", 0))
                self.tiles[(x, y)] = "door_open"
                self.event_flags["door_opened"] = True
            elif action.verb == "move":
                # No-op for now
                pass

    def compute_delta(self, previous_snapshot: Dict) -> WorldDelta:
        with self.lock:
            prev_tiles = previous_snapshot.get("tiles", {})
            prev_flags = previous_snapshot.get("event_flags", {})
            tile_changes = []
            for (x, y), tile_type in self.tiles.items():
                key = f"{x},{y}"
                if prev_tiles.get(key) != tile_type:
                    tile_changes.append(TileChange(x=x, y=y, new_type=tile_type))
            event_changes = []
            for flag, value in self.event_flags.items():
                if prev_flags.get(flag) != value and value:
                    event_changes.append(flag)
            return WorldDelta(tile_changes=tile_changes, event_flags=event_changes)

    def get_snapshot(self) -> Dict:
        with self.lock:
            tiles_serialized = {f"{x},{y}": t for (x, y), t in self.tiles.items()}
            flags_copy = dict(self.event_flags)
            return {"tiles": tiles_serialized, "event_flags": flags_copy}
