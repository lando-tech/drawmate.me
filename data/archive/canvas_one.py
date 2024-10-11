import tkinter as tk
from tkinter import ttk
from widgets import ListBox


class CanvasOne:

    def __init__(self, master) -> None:
        self.canvas_1 = tk.Canvas(master=master)
        self.canvas_1.pack(side='left', padx=10, pady=10)

        self.listbox = ListBox()
        self.listbox.init_listbox(master=self.canvas_1)

    def generate_treeview_button(self):
        pass
