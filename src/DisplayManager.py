from dotenv import dotenv_values
from threading import Thread
from time import sleep, time
import logging

from src.SpotifyAPI import SpotifyAPI
from src.SpotifyPlayer import SpotifyPlayer
from src.SteelSeriesAPI import SteelSeriesAPI
from src.Timer import Timer
from src.image_utils import convert_to_bitmap
from src.utils import fetch_content_path


class DisplayManager:
    def __init__(self, config, fps):
        env = dotenv_values(fetch_content_path('.env'))
        if not env:
            logging.error("No environment file found, has the .env file been modified?")
            exit(1)

        self.player = SpotifyPlayer(config, fps)
        self.fetch_delay = max(int(env["SPOTIFY_FETCH_DELAY"]), 1 / fps)
        self.steelseries_api = SteelSeriesAPI()
        self.timer = Timer(config, env["DATE_FORMAT"], env["DISPLAY_SECONDS"].lower() in ("true", "yes", "1"))
        self.timer_threshold = int(env["TIMER_THRESHOLD"]) * 1000
        self.spotify_api = SpotifyAPI(
            env['SPOTIFY_CLIENT_ID'],
            env['SPOTIFY_CLIENT_SECRET'],
            env['SPOTIFY_REDIRECT_URI'],
            env['LOCAL_PORT']
        )

        self.display_clock = True
        self.display_player = True
        self.enabled = True

        self.fps = fps
        self.state = 0

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
                self.state = 1

            frame_data = None
            if (self.state == 0 or not self.display_player) and self.display_clock:
                frame_data = convert_to_bitmap(self.timer.get_image().getdata())
            elif self.display_player:
                frame_data = convert_to_bitmap(self.player.next_step().getdata())
                if self.player.pause_started and (round(time() * 1000) - self.player.pause_started) > self.timer_threshold:
                    self.player.pause_started = 0
                    self.state = 0

            if frame_data is not None:
                thread = Thread(target=self.send_frame, daemon=True, args=(self.steelseries_api, frame_data))
                thread.start()

            sleep(1 / self.fps)
            i += 1 / self.fps

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
