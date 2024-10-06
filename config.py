import toml
from pathfinder import PathFinder as pf


class AppConfig(pf):

    def __init__(self) -> None:
        super().__init__()
        self.color_pallete_path = self.COLOR_PALLETE_TOML
        self.color_pallete = {
                'black': "#282a36",
                'white': "#f8f8f2",
                'green': "#50fa7b",
                'red': "#ff5555",
                'orange': "#ffb86c",
                'yellow': "#f1fa8c",
                'purple': "#bd93f9",
                'cyan': "#8be9fd",
                'grey': "#6272a4",
                'light_grey': "#44475a",
                }

    def get_color_pallete(self):
        with open(self.color_pallete_path, 'r', encoding='utf-8') as file:
            config = toml.load(file)

            for k, v in config.items():
                if isinstance(v, dict):
                    for key, value in v.items():
                        print(value)
                        return value
