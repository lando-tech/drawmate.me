import tkinter as tk
from tkinter import ttk
from widgets import ListBox, TreeView


class CanvasTwo:

    def __init__(self, master) -> None:
        self.canvas_2 = tk.Canvas(master=master)
        self.canvas_2.pack(side='left', padx=10, pady=10)
        self.notebook = NotebookOne(self.canvas_2) 


class NotebookOne:

    def __init__(self, master) -> None: 
        self.notebook_1 = ttk.Notebook(master=master)
        self.listbox = ListBox()

    def create_notebook_tab(self, tab):
        tab_name = self.listbox.get_listbox_selection().get('tab_name')
        tab = ttk.Frame(master=self.notebook_1)
        self.notebook_1.add(tab, 
                            text=f"{tab_name}")
        self.treeview = TreeView()
        self.treeview.init_treeview(master=tab)

        
