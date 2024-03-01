from PIL import Image, ImageFont, ImageDraw

from src.image_utils import draw_spotify
from src.ScrollableText import ScrollableText
from src.utils import fetch_content_path


class SpotifyPlayer:
    ARTIST_FONT = ImageFont.truetype(font=fetch_content_path('fonts/MunroSmall.ttf'), size=10)
    TITLE_FONT = ImageFont.truetype(font=fetch_content_path('fonts/VerdanaBold.ttf'), size=11)
    DURATION_FONT = ARTIST_FONT

    def __init__(self, config, fps=None):
        self.config = config

        self.fps = fps
        self.step = 0

        self.scrollbar_region = (self.config.scrollbar_padding, 24, self.config.width - self.config.scrollbar_padding + 1, 30)
        self.artist = ScrollableText(self.config, self.ARTIST_FONT, "", 3)
        self.title = ScrollableText(self.config, self.TITLE_FONT, "", 15)

        self.paused = True
        self.pause_started = 0
        self.changed = False
        self.song_position = 0
        self.song_duration = 0
        self.previous_image = None

    def set_paused(self, paused=True):
        self.paused = paused

    def update_song(self, title, artist, song_position=0, song_duration=0, paused=False):
        self.title.set_text(title)
        self.artist.set_text(artist)

        self.paused = paused
        self.song_position = song_position
        self.song_duration = song_duration
        self.changed = True
        self.step = 0
        self.title.set_step(0)
        self.artist.set_step(0)

    def is_playing(self):
        return self.song_position != self.song_duration

    def increase_timer(self):
        self.seek_song(self.song_position + 1000 / self.fps)

    def seek_song(self, song_position):
        is_same_second = int(self.song_position / 1000) == int(song_position / 1000)
        self.song_position = max(0, min(song_position, self.song_duration))

        if not is_same_second:
            self.changed = True

    def draw_progress_bar(self, draw, region):
        if self.song_duration == 0:
            percentage = 0
        else:
            percentage = self.song_position / self.song_duration

        draw.rectangle(region, outline=self.config.primary)
        draw.rectangle(
            (region[0], region[1], region[0] + int(percentage * (region[2] - region[0])), region[3]),
            fill=self.config.primary
        )

    def draw_duration(self, draw, duration, position, anchor):
        hours = duration // 3600
        minutes = (duration % 3600) // 60
        seconds = duration % 60

        if hours > 0:
            text = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        else:
            text = "{:02d}:{:02d}".format(minutes, seconds)

        draw.text(position, text, font=self.DURATION_FONT, fill=self.config.primary, anchor=anchor)

    def will_it_change(self):
        if not self.paused and int((self.song_position + 1000 / self.fps) / 1000) != int((self.song_position / 1000)):
            return True

        return self.title.will_it_change() or self.artist.will_it_change()

    def next_step(self, force_update=False):
        if not self.changed and not force_update and not self.will_it_change() and self.previous_image is not None:
            self.step += 1
            self.artist.increase_step()
            self.title.increase_step()

            if not self.paused:
                self.increase_timer()

            return self.previous_image

        if not self.paused:
            self.increase_timer()

        self.step += 1
        image = Image.new(mode="1", size=(self.config.width, self.config.height), color=self.config.secondary)
        draw = ImageDraw.Draw(image)

        self.artist.draw_next_step(draw)
        self.title.draw_next_step(draw)

        self.draw_progress_bar(draw, (self.config.scrollbar_padding, 24, self.config.width - (self.config.scrollbar_padding + 1), 30))

        self.draw_duration(draw, int(self.song_position / 1000), (self.config.scrollbar_padding, 34), "lm")
        self.draw_duration(draw, int(self.song_duration / 1000), (self.config.width - self.config.scrollbar_padding + 1, 34), "rm")

        draw.rectangle((0, 0, self.config.text_padding_left - 3, 22), fill=self.config.secondary)
        draw_spotify(image, (2, 3))

        self.previous_image = image
        self.changed = False
        return image
