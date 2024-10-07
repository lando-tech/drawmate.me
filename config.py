import toml
from pathfinder import PathFinder as pf


class AppConfig(pf):

    def __init__(self) -> None:
        super().__init__()
        self.color_pallete_path = self.COLOR_PALLETE_TOML
        # Place holder for color pallete function 
        # that returns the specified config file
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
        self.font_regular = ('Arial', 13) 
        self.font_bold = ('Arial', 13, 'bold') 
        self.font_italic = ('Arial', 12, 'italic') 
        self.font_large = ('Arial', 18, 'bold') 

    def get_color_pallete(self, toml_config: str):
        """
        toml_config_params: catppucin, dracula, gruvbox 
        """
        with open(self.color_pallete_path, 'r', encoding='utf-8') as file:
            config = toml.load(file)
            
            return config
