from src.utils import fetch_content_path

from PIL import ImageFont


class ScrollableText:
    DEFAULT_FONT = ImageFont.truetype(fetch_content_path('./fonts/MunroSmall.ttf'), size=10)

    def __init__(self, config, content="", pos_y=0, font=DEFAULT_FONT):
        self.content = None
        self.font = None

        self.content_pixels_size = 0
        self.need_scrolling = False
        self.intern_step = 0
        self.text_offset = 0
        self.max_step = 0

        self.config = config
        self.set_text(content, font)
        self.pos_y = pos_y

    def increase_step(self):
        self.intern_step += 1
        if self.max_step != 0 and self.intern_step > self.max_step:
            self.intern_step = 0

    def set_step(self, step):
        self.intern_step = min(max(0, step), self.max_step)

    def will_it_change(self):
        if not self.need_scrolling:
            return False

        if self.config.pause_steps <= self.intern_step <= (self.config.pause_steps + self.text_offset) \
                or self.intern_step == self.max_step:
            return True
        return False

    def set_text(self, content, font=None):
        if font is not None:
            self.font = font

        self.content = content
        self.content_pixels_size = int(self.font.getlength(self.content))
        self.text_offset = self.content_pixels_size - (self.config.width - self.config.text_padding_left)

        if self.content_pixels_size > (self.config.width - self.config.text_padding_left):
            self.need_scrolling = True
            self.max_step = 2 * self.config.pause_steps + self.content_pixels_size - (self.config.width - self.config.text_padding_left)
        else:
            self.need_scrolling = False

    def draw_next_step(self, draw):
        self.increase_step()
        self.draw_step(draw, self.intern_step)

    def draw_step(self, draw, step=-1):
        if step < 0:
            step = self.intern_step

        if not self.need_scrolling:
            draw.text((self.config.width - 1, self.pos_y), self.content, font=self.font, anchor="rm", fill=self.config.primary)
            return

        if (step - self.config.pause_steps) > self.text_offset:
            step = self.text_offset
        else:
            if step <= self.config.pause_steps:
                step = 0
            else:
                step -= self.config.pause_steps

        draw.text((self.config.width - 1 + self.text_offset - step, self.pos_y), self.content, font=self.font, anchor="rm",
                  fill=self.config.primary)
