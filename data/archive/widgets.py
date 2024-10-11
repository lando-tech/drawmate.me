import tkinter as tk
from tkinter import ttk
from utils.pathfinder import PathFinder

import os
import json

class ListBox:

    def __init__(self) -> None:
        self.pf = PathFinder()
        self.tree = TreeView()

    def init_listbox(self, master):
        # Init listbox
        self.listbox = tk.Listbox(master=master)
        # Configure listbox settings
        self.listbox.config(selectmode='single',
                            relief='flat',
                            borderwidth=2,
                            activestyle='none',
                            height=10,
                            width=40,
                            )

        # Bind keys and commands
        self.listbox.bind('<Up>', self.on_up)
        self.listbox.bind('<Down>', self.on_down)
        self.listbox.bind('<Return>', self.on_enter)

        # Set label
        self.listbox_label = tk.Label(master=master, text='Drawio Templates:')
        self.listbox_label.pack(side='top', padx=10, pady=10)

        # List templates stored in json dir
        self.list_templates()

        # Pack listbox to canvas
        self.listbox.pack(padx=10, pady=10)

    def list_templates(self):
        # Return current selection in listbox
        if os.path.isdir(self.pf.JSON_DIR):
            self.listbox.delete(0, 'end')
            for item in self.pf.export_json_templates():
                split_item = item.split('/')
                if '.git' in item:
                    pass
                else:
                    self.listbox.insert(tk.END, split_item[-1])
        else:
            raise NotADirectoryError

    def on_up(self, e):
        # Get current selection and highlight by moving arrow key up
        current_selection = self.listbox.curselection()
        if current_selection:
            index = current_selection[0]
            if index > 0:
                self.listbox.selection_clear(index)
                self.listbox.selection_set(index - 1)
                self.listbox.activate(index - 1)

    def on_down(self, e):
        # Get current selection and highlight by moving arrow key down
        current_selection = self.listbox.curselection()
        if current_selection:
            index = current_selection[0]
            if index < self.listbox.size() - 1:
                self.listbox.selection_clear(index)
                self.listbox.selection_set(index + 1)
                self.listbox.activate(index + 1)

    def on_enter(self, e):
        if not self.listbox.curselection():
            return 
        else:
            json_data = self.get_listbox_selection().get('json_data')
            tab_name = self.get_listbox_selection().get('json_data')
            self.tree.create_tree_view(json_data, tab_name)

    def get_listbox_selection(self):
        """Returns current selection of the listbox"""

        # Get index of selected item
        selected_index = self.listbox.curselection()
        # Return nil if nothing is selected
        if not selected_index:
            return

        selectetd_template = self.listbox.get(selected_index)
        template_path = os.path.join(self.pf.JSON_DIR, selectetd_template)

        if os.path.isfile(template_path):
            with open(template_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                tab_name = selectetd_template.split()[0]

                listbox_select = {'json_data': json_data, 'tab_name': tab_name}

            return listbox_select

class TreeView:

    def __init__(self) -> None: 
        pass 

    def init_treeview(self, master):
        self.tree = ttk.Treeview(master=master)
        self.tree.configure(height=200)
        self.tree['column'] = ('diagram',)
        self.tree.column('diagram',
                         width=400,
                         minwidth=200,
                         stretch=tk.NO)
        self.tree.heading('#0',
                          text='drawio',
                          anchor=tk.W)
        self.tree.heading('diagram',
                          text='values',
                          anchor=tk.W)
        self.root_node = self.tree.insert('', 'end', text='mxfile')
    
    def create_tree_view(self, json_data, root_node):
        for k, v in json_data.items():
            if isinstance(v, dict):
                node_id = self.tree.insert(self.root_node, 'end', text=k)
                self.create_tree_view(node_id, v)
            else:
                self.tree.insert(self.root_node, 'end', text=k, values=(v,))
        self.tree.pack(side='top', padx=10, pady=10)

