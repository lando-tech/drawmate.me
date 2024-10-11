import tkinter as tk 
from tkinter import ttk


class MenuBar:

    def __init__(self, master) -> None:
        self.menu_bar = tk.Menu(master=master)

        # Create filemenu
        self.filemenu = tk.Menu(master=self.menu_bar, tearoff=0)

        # Set commands for filemenu
        self.filemenu.add_command(label='Upload', command=None)
        self.filemenu.add_command(label='Open', command=None)
        self.filemenu.add_command(label='Save', command=None)
        self.filemenu.add_command(label='Export', command=None)

        # Call root to init menubar
        self.menu_bar.add_cascade(label='File', menu=self.filemenu)

    def set_menu_bar_configs(self):
        pass

    def attach_menu_bar(self, root):
        root.config(menu=self.menu_bar) 
