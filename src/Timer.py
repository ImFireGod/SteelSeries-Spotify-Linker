from PIL import ImageFont, ImageDraw, Image
from time import localtime, strftime

from src.image_utils import fetch_content_path


class Timer:
    TIMER_FONT = ImageFont.truetype(font=fetch_content_path('fonts/DS-DIGIB.ttf'), size=24)

    def __init__(self, config, date_format, display_seconds):
        self.config = config
        self.date_format = int(date_format)
        self.display_seconds = display_seconds

    def get_image(self):
        image = Image.new(mode="1", size=(self.config.width, self.config.height), color=self.config.secondary)
        draw = ImageDraw.Draw(image)

        time = self.get_current_time()
        draw.text((self.config.width / 2, self.config.height / 2), time, font=self.TIMER_FONT, fill=self.config.primary, anchor="mm")

        return image

    def get_current_time(self):
        current_time = localtime()
        seconds = ":%S" if self.display_seconds else ""
        if self.date_format == 12:
            formatted_time = strftime("%I:%M" + seconds + " %p", current_time)
        else:
            formatted_time = strftime("%H:%M" + seconds, current_time)
        return formatted_time
    
    def set_display_seconds(self, display_seconds):
        self.display_seconds = display_seconds

    def set_date_format(self, date_format):
        self.date_format = date_format if date_format == 12 else 24
