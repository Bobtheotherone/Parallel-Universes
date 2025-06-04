# Parallel Universes – Design Notes

## 1. Overall Flow
1. Client A and Client B both run a Pygame instance (`client/main.py`).
2. Upon startup, each client connects to the FastAPI server (WebSocket endpoint: `/ws`).
3. Clients maintain a local `WorldState` object (loaded from JSON or blank).
4. Player input (e.g., press arrow keys to move a cursor, plant seeds, open doors) triggers an “action” message:
   ```json
   {
     "type": "action",
     "actor_id": "<player_uuid>",
     "action": {
       "verb": "move",
       "params": { "dx": 1, "dy": 0 }
     }
   }
