import tkinter as tk


class RootWindow:

    def __init__(self):
        self.root = tk.Tk()
        self.root.minsize(width=600, height=600)
        self.root.title('diagram.me')

        self.root.mainloop()

    def _init_window(self):
        self.main_menu = tk.Menu(self.root)


if __name__ == "__main__":
    RootWindow()