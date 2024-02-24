import logging

from src.Config import Config
from src.DisplayManager import DisplayManager

logging.basicConfig(level=logging.INFO)
FPS = 10

if __name__ == "__main__":
    config = Config({
        "pause_steps": FPS * 2,
    })

    display_manager = DisplayManager(config, FPS)
    display_manager.init()
    logging.info("[SpotifyLinker] Application ready")
    display_manager.run()
