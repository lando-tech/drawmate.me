import tkinter as tk 
from tkinter import ttk


class RootWindow:

    def __init__(self):
        self.root = tk.Tk()
        self.root.minsize(width=600, height=600)
        self.root.title('drawmate.me')
        self.root.config(padx=10, pady=10)
        self.root.mainloop()


class MainMenu:

    def __init__(self, root):
        options = [
            "Export to draw.io",
            "Create template",
            "Delete template",
            "View saved templates",
            "Upload file",
        ]
        clicked = tk.StringVar()
        clicked.set(options[0])
        main_menu = ttk.Combobox(root, textvariable=clicked, values=options)
        main_menu.pack()


if __name__ == "__main__":
    RootWindow()
