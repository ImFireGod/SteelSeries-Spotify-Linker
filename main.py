import logging
from psutil import pid_exists
from os import getpid, path, getenv, makedirs
import atexit
import sys
import ctypes

from version import __version__
from src.Config import Config
from src.DisplayManager import DisplayManager
from src.utils import fetch_app_data_path


logging.basicConfig(
    level=logging.INFO, 
    format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)

FPS = 10


if __name__ == "__main__":
    logger = logging.getLogger("SpotifyLinker")

    # Create app data directory if it doesn't exist
    app_data_path = fetch_app_data_path()
    if not path.exists(app_data_path):
        logger.info("Creating app data directory at %s", app_data_path)
        makedirs(app_data_path)

    lock_file_path = path.join(app_data_path, '.lock')

    # Check if another instance is already running through lock file which contains PID
    if path.exists(lock_file_path):
        with open(lock_file_path, 'r') as f:
            content = f.read().strip()
            if content.isdigit():
                pid = int(content)
                if pid_exists(pid):
                    logger.error("Another instance is already running with PID %d", pid)
                    ctypes.windll.user32.MessageBoxW(0, f"Another instance is already running with PID {pid}", "Error", 0x10)
                    sys.exit(1)
            
    # Write lock file with PID to prevent multiple instances
    with open(lock_file_path, 'w') as lock_file:
        lock_file.write(str(getpid()))

    # Remove lock file on exit
    atexit.register(lambda: path.exists(lock_file_path) and path.unlink(lock_file_path))

    config = Config({
        "pause_steps": FPS * 2,
    })

    display_manager = DisplayManager(config, FPS)
    display_manager.init()  
    logger.info("Spotify Linker running in version %s", __version__)
    display_manager.run()
