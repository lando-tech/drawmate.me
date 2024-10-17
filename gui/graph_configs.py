class Configs:

    def __init__(self) -> None:
        self.COLOR_PALETTE = {
            "bg": (40, 44, 52),
            "fg": (171, 178, 191),
            "rect": (209, 154, 102),
            "menu": (76, 82, 99),
            "button": (97, 175, 239),
        }
        self.fonts = ["arial", "calibri"]
        self.ROOT_SURFACE_WIDTH = 1000
        self.ROOT_SURFACE_HEIGHT = 800

    def get_color_palette(self) -> dict[str, tuple]:
        return self.COLOR_PALETTE
