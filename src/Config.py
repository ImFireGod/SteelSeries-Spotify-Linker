class Config:
    DEFAULT_CONFIG = {
        "primary": 1,
        "secondary": 0,
        "pause_steps": 10,
        "scrollbar_padding": 2,
        "text_padding_left": 30,
        "width": 128,
        "height": 40,
        "use_extended_font": False
    }

    def __init__(self, config=None):
        if config is None:
            config = {}

        for key, value in self.DEFAULT_CONFIG.items():
            setattr(self, key, config.get(key, value))

    def save_config(self, config_file):
        with open(config_file, "w") as file:
            file.write(self.to_json())

    def read_config(self, config_file):
        with open(config_file, "r") as file:
            self.from_json(file.read())
