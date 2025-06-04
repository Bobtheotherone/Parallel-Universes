# Parallel Universes – Design Notes

## 1. Overall Flow
1. Client A and Client B both run a Pygame instance (`client/main.py`).
2. On startup, each client connects to the FastAPI server via WebSocket at `/ws`.
3. Clients maintain a local `WorldState` object.
4. Player input generates an "action" message which is sent to the server.
5. The server applies the action, computes a `world_delta` and broadcasts an
   update message back to both clients.
6. Clients apply the delta to their local world state and render the result.

## 2. Core Data Models
`shared/schemas.py` defines:
- `PlayerAction` – actor id, verb, and parameters.
- `TileChange` – a single tile update.
- `WorldDelta` – list of tile changes and event flags.
- `SyncMessage` – either an action or an update message.

## 3. Modules Overview
- `shared/utils.py` – helpers like `draw_tile` for rendering.
- `server/main.py` – FastAPI application running under Uvicorn.
- `server/router.py` – REST `/world` endpoint and WebSocket `/ws` endpoint.
- `server/models.py` – in memory `WorldState` singleton with methods to apply
  actions and compute deltas.
- `client/settings.py` – constants such as server URLs and screen size.
- `client/network.py` – WebSocket client to send actions and receive updates.
- `client/game.py` – Pygame loop handling input, rendering and network sync.
- `client/main.py` – CLI entrypoint creating the game and starting it.

## 4. World Representation
World is a 50×50 grid of tiles identified by `(x,y)` coordinates.  Each tile has
one of: `empty`, `grass`, `flower`, or `door`.  Event flags are stored in a
simple dictionary mapping string names to booleans.

## 5. Networking Protocol
- Action message:
```json
{
  "type": "action",
  "data": {
    "actor_id": "uuid",
    "verb": "plant_flower",
    "params": {"x": 10, "y": 22}
  }
}
```
- Update message:
```json
{
  "type": "update",
  "data": {
    "tile_changes": [{"x": 10, "y": 22, "new_type": "flower"}],
    "event_flags": ["flower_planted"]
  }
}
```

## 6. Game Loop
1. Initialize Pygame and load the initial world via REST `/world`.
2. Connect to the WebSocket and start a background receive loop.
3. In each frame: process input, send actions, apply deltas and render tiles.
