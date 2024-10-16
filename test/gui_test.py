import customtkinter as ct
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk

import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.pathfinder import PathFinder
from utils.xml2json import xml2json
from utils.json2xml import JsonUtils
from utils.pdf_handler import DataExtract
from config.config import AppConfig

config = AppConfig()


class Root(PathFinder, JsonUtils, DataExtract):

    def __init__(self):
        super().__init__()
        self.root = ct.CTk()
        self.root.minsize(800, 600)
        self.menu_bar = MenuBar(root=self.root)
        self.canvas_one = CanvasOne(root=self.root)
        self.canvas_two = CanvasTwo(root=self.root)
        self.root.config(menu=self.menu_bar.get_menu_bar())
        self.root.mainloop()


class MenuBar:

    def __init__(self, root):
        self.menu_bar = tk.Menu(master=root)
        self.menu_bar.config(font=config.font_regular)
        self.file_menu = tk.Menu(master=self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=None)
        self.file_menu.add_command(label="Open", command=None)
        self.file_menu.add_command(label="Save", command=None)
        self.file_menu.add_command(label="Export", command=None)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

    def get_menu_bar(self):
        return self.menu_bar


class CanvasOne:
    
    def __init__(self, root) -> None:
        self.canvas = ct.CTkCanvas(master=root)
        self.menu = ct.CTkOptionMenu(master=self.canvas)
        self.menu.pack()
        self.canvas.pack(side='left', padx=10, pady=10)
    
    def get_canvas_one(self):
        return self.canvas


class CanvasTwo:
    
    def __init__(self, root) -> None:
        self.canvas = ct.CTkCanvas(master=root)
        self.canvas.pack(side='left', padx=10, pady=10)
    
    def get_canvas_two(self):
        return self.canvas


if __name__ == "__main__":
    Root()
