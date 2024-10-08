import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.pathfinder import PathFinder
from utils.xml2json import xml2json
from utils.json2xml import JsonUtils
from utils.pdf_handler import DataExtract
from config.config import AppConfig
import json
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk


class RootWindow(PathFinder, JsonUtils, DataExtract):
    """
    Main class for the drawmate UI.
    Initializes a main window and makes calls to the backend modules
    for data processing.
    """

    def __init__(self) -> None:
        super().__init__()
        # Init root window
        self.root = tk.Tk()

        # Set configs
        self.config = AppConfig()
        self.set_root_configs()

        self.root.mainloop()

    def set_root_configs(self):
        """
        Set root configs, color_pallete, window_size, title etc...
        Defines the main ui components for the child elements.
        """
        # Define color_pallete
        self.root.tk_setPalette(
                    background=self.config.color_pallete.get('light_grey'),
                    foreground=self.config.color_pallete.get('white'),
                    highlightBackground=self.config.color_pallete.get('purple'),
                    highlightForeground=self.config.color_pallete.get('white'),
                    selectBackground=self.config.color_pallete.get('red'),
                    selectForeground=self.config.color_pallete.get('white'),
                    activeBackground=self.config.color_pallete.get('purple'),
                    activeForeground=self.config.color_pallete.get('black'),
                )

        # Set window size
        self.root.minsize(width=600, height=400)
        # Set title
        self.root.title('drawmate.me')


if __name__ == "__main__":
    RootWindow()
