import logging

from version import __version__
from src.Config import Config
from src.DisplayManager import DisplayManager
from src.Systray import run_systray_async

logging.basicConfig(level=logging.INFO)
FPS = 10


if __name__ == "__main__":
    config = Config({
        "pause_steps": FPS * 2,
    })

    display_manager = DisplayManager(config, FPS)
    display_manager.init()
    run_systray_async(display_manager)
    logging.info("[SpotifyLinker] Spotify Linker running in version %s", __version__)
    display_manager.run()
