import uuid
from typing import Dict
import pygame


def generate_player_id() -> str:
    """Return a new UUID string."""
    return str(uuid.uuid4())


def draw_tile(surface: pygame.Surface, x: int, y: int, tile_type: str, tile_size: int) -> None:
    """Draw a simple colored rectangle representing a tile."""
    colors: Dict[str, tuple] = {
        "empty": (50, 50, 50),
        "grass": (34, 139, 34),
        "flower": (255, 0, 255),
        "door": (139, 69, 19),
        "door_open": (205, 133, 63),
    }
    rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
    pygame.draw.rect(surface, colors.get(tile_type, (100, 100, 100)), rect)
