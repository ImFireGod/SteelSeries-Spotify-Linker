from os import path, getenv
from json import loads, dumps

import logging
import ctypes

from src.utils import fetch_app_data_path

logger = logging.getLogger("SpotifyLinker")

class UserPreferences:
    DEFAULT = {
        "spotify_client_id": "",
        "spotify_client_secret": "",
        "spotify_redirect_uri": "",
        "local_port": 2408,
        "date_format": 12,
        "display_seconds": True,
        "timer_threshold": 2,
        "spotify_fetch_delay": 2,
        "extended_font": True,
        "display_timer": True,
        "display_player": True
    }

    def __init__(self):
        self.valid = True
        self.preferences = self.DEFAULT
        self.config_path = fetch_app_data_path("config.json")
        logger.info("Preferences path : " + self.config_path)

    def load_preferences(self) -> bool:
        self.valid = True

        try:
            with open(self.config_path, "r") as file:
                try:
                    self.preferences = loads(file.read())

                    modified = False
                    for key, value in self.DEFAULT.items():
                        if key not in self.preferences:
                            self.preferences[key] = value
                            modified = True

                    if modified:
                        self.save_preferences()
                    return True
                
                except Exception as e:
                    self.valid = False
                    logger.error("Error loading preferences: " + str(e))
                    ctypes.windll.user32.MessageBoxW(0, f"Error loading preferences: {str(e)}", "Error", 0x10)
                    return False
                
        except FileNotFoundError:
            logger.info("No preferences found, created default preferences")
            self.save_preferences()
        return True

    def save_preferences(self):
        with open(self.config_path, "w") as file:
            file.write(dumps(self.preferences, indent=4))

    def get_preference(self, key):
        return self.preferences.get(key)