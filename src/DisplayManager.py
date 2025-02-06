from threading import Thread
from time import sleep, time
import logging
import ctypes

from src.SpotifyAPI import SpotifyAPI
from src.SpotifyPlayer import SpotifyPlayer
from src.SteelSeriesAPI import SteelSeriesAPI
from src.Timer import Timer
from src.image_utils import convert_to_bitmap
from src.UserPreferences import UserPreferences
from src.Systray import run_systray_async


logger = logging.getLogger("SpotifyLinker")

class State:
    SHOW_CLOCK = 0
    SHOW_PLAYER = 1 

class DisplayManager:
    def __init__(self, config, fps):
        self.fps = fps
        self.state = State.SHOW_CLOCK

        self.enabled = True
        self.display_clock = True
        self.display_player = True

        self.user_preferences = UserPreferences()
        self.timer = Timer(config, self.user_preferences.get_preference('date_format'), self.user_preferences.get_preference('display_seconds'))
        self.player = SpotifyPlayer(config, fps)
        
        # Load systray menu
        run_systray_async(self)

        self.load_preferences()
        self.steelseries_api = SteelSeriesAPI()
        self.spotify_api = SpotifyAPI(self.user_preferences)

    def load_preferences(self):
        self.user_preferences.load_preferences()
        self.update_preferences()
    
    def update_preferences(self):
        self.fetch_delay = max(int(self.user_preferences.get_preference('spotify_fetch_delay')), 1 / self.fps)
        self.timer_threshold = max(self.user_preferences.get_preference('timer_threshold'), 0) * 1000

        self.display_clock = self.user_preferences.get_preference('display_timer')
        self.display_player = self.user_preferences.get_preference('display_player')
        
        self.timer.set_display_seconds(self.user_preferences.get_preference('display_seconds'))
        self.timer.set_date_format(self.user_preferences.get_preference('date_format'))

    def init(self):
        self.spotify_api.fetch_token()

    def run(self):
        i = self.fetch_delay + 1
        while True:
            if not self.enabled:
                continue

            if i > self.fetch_delay and self.display_player:
                thread = Thread(target=self._fetch_and_update_song, daemon=True, args=(self.spotify_api, self.player))
                thread.start()
                i = 0

            if not self.player.paused:
                self.state = State.SHOW_PLAYER

            frame_data = None
            if (self.state == State.SHOW_CLOCK or not self.display_player) and self.display_clock:
                frame_data = convert_to_bitmap(self.timer.get_image().getdata())
            elif self.display_player:
                frame_data = convert_to_bitmap(self.player.next_step().getdata())
                if self.player.pause_started and (
                        round(time() * 1000) - self.player.pause_started) > self.timer_threshold:
                    self.player.pause_started = 0
                    self.state = State.SHOW_CLOCK

            if frame_data is not None:
                thread = Thread(target=self.send_frame, daemon=True, args=(self.steelseries_api, frame_data))
                thread.start()

            sleep(1 / self.fps)
            i += 1 / self.fps

    def update_config(self):
        if not self.user_preferences.load_preferences():
            logger.error("Failed to update configuration")
            return
        
        self.update_preferences()

        logger.info("Configuration updated")
        ctypes.windll.user32.MessageBoxW(0, "Configuration successfully updated", "Info", 0x40 | 0x1)

    @staticmethod
    def _fetch_and_update_song(spotify_api, player):
        song_data = spotify_api.fetch_song()
        if song_data is not None:
            if player.title.content != song_data['title']:
                player.update_song(song_data['title'], song_data['artist'],
                                   song_data['progress'], song_data['duration'])
            else:
                if not player.paused:
                    player.seek_song(song_data['progress'])

            if not player.paused and song_data["paused"]:
                player.pause_started = round(time() * 1000)
            elif player.paused and not song_data["paused"]:
                player.pause_started = 0

            player.set_paused(song_data["paused"])
        else:
            player.set_paused(True)

    @staticmethod
    def send_frame(steelseries_api, frame):
        steelseries_api.send_frame(frame)
