
import argparse
import uuid
from client.game import Game

# Codex Prompt:
# """
# Parse optional --player-id. Generate a UUID if missing and start the Game.
# """


def main():
    parser = argparse.ArgumentParser(description="Parallel Universes Client")
    parser.add_argument("--player-id", type=str, help="Unique player id")
    args = parser.parse_args()
    player_id = args.player_id or str(uuid.uuid4())
    game = Game(player_id)
    game.run()


if __name__ == "__main__":
    main()
