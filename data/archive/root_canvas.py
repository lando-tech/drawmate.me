import tkinter as tk
from tkinter import ttk
from canvas_one import CanvasOne
from canvas_two import CanvasTwo

class RootCanvas:

    def __init__(self, master) -> None:
        self.root_canvas = tk.Canvas(master=master)
        self.root_canvas.pack(side='bottom', padx=10, pady=10)
        self.child1 = CanvasOne(master=self.root_canvas)
        self.child2 = CanvasTwo(master=self.root_canvas)
       
    def set_root_canvas_configs(self, color_palette, font, padx, pady, side):
        pass
