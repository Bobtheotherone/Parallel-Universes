
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


class Game:
    def __init__(self, player_id: str):
        self.player_id = player_id
        self.screen = None
        self.clock = None
        self.network = NetworkClient(WS_ENDPOINT, REST_ENDPOINT)
        self.world_state: Dict = {}
        self.running = True
        self.cursor_x = 0
        self.cursor_y = 0
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.loop.run_forever, daemon=True).start()

    async def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.world_state = self.network.get_initial_world()
        await self.network.connect()
        self.loop.create_task(self.network.receive_loop(self.apply_delta))

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_LEFT:
                    self.cursor_x = max(0, self.cursor_x - 1)
                    action = PlayerAction(actor_id=self.player_id, verb="move", params={"dx": -1, "dy": 0})
                    asyncio.run_coroutine_threadsafe(self.network.send_action(action), self.loop)
                elif event.key == pygame.K_RIGHT:
                    self.cursor_x = min(49, self.cursor_x + 1)
                    action = PlayerAction(actor_id=self.player_id, verb="move", params={"dx": 1, "dy": 0})
                    asyncio.run_coroutine_threadsafe(self.network.send_action(action), self.loop)
                elif event.key == pygame.K_UP:
                    self.cursor_y = max(0, self.cursor_y - 1)
                    action = PlayerAction(actor_id=self.player_id, verb="move", params={"dx": 0, "dy": -1})
                    asyncio.run_coroutine_threadsafe(self.network.send_action(action), self.loop)
                elif event.key == pygame.K_DOWN:
                    self.cursor_y = min(49, self.cursor_y + 1)
                    action = PlayerAction(actor_id=self.player_id, verb="move", params={"dx": 0, "dy": 1})
                    asyncio.run_coroutine_threadsafe(self.network.send_action(action), self.loop)
                elif event.key == pygame.K_SPACE:
                    action = PlayerAction(actor_id=self.player_id, verb="plant_flower", params={"x": self.cursor_x, "y": self.cursor_y})
                    asyncio.run_coroutine_threadsafe(self.network.send_action(action), self.loop)

    def apply_delta(self, delta: WorldDelta):
        for change in delta.tile_changes:
            key = f"{change.x},{change.y}"
            self.world_state.setdefault("tiles", {})[key] = change.new_type
        for flag in delta.event_flags:
            self.world_state.setdefault("event_flags", {})[flag] = True

    def render(self):
        self.screen.fill((0, 0, 0))
        for key, tile_type in self.world_state.get("tiles", {}).items():
            x, y = map(int, key.split(","))
            draw_tile(self.screen, x, y, tile_type, TILE_SIZE)
        rect = pygame.Rect(self.cursor_x * TILE_SIZE, self.cursor_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)
        pygame.display.flip()

    def run(self):
        asyncio.run(self.setup())
        while self.running:
            self.process_input()
            self.render()
            self.clock.tick(FPS)
        pygame.quit()
