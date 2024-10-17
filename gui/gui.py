import customtkinter as ct
from customtkinter import filedialog as fd
from tkinter import ttk
import tkinter as tk
from typing import Dict

import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.pathfinder import PathFinder
from utils.xml2json import xml2json
from utils.json2xml import JsonUtils
from utils.pdf_handler import DataExtract
from config.config import AppConfig
from database.db import MyDB


config = AppConfig()
pathfinder = PathFinder()
json_utils = JsonUtils()
extractor = DataExtract()


class Root(ct.CTk):

    def __init__(self):
        super().__init__()
        self.title("drawmate.me")
        self.geometry("800x800")
        self.frame_one = FrameOne(root=self)


class FrameOne(ct.CTkFrame):

    def __init__(self, root) -> None:
        super().__init__(root)
        self.pack(padx=10, pady=10, fill="both", expand=True)
        self.menu_frame = MenuFrame(root=self)
        self.tabview = TabView(root=self)


class MenuFrame(ct.CTkFrame):

    def __init__(self, root) -> None:
        super().__init__(root)
        # Pack frame to canvas
        self.pack(padx=10, pady=10, fill="x")

        # Declare buttons for menu frame
        self.upload_button = ct.CTkButton(
            master=self, text="Upload", command=self.upload_command
        )
        self.upload_button.grid(column=0, row=0, padx=20, pady=10)

        self.export_button = ct.CTkButton(
            master=self, text="Export", command=self.export_command
        )
        self.export_button.grid(column=1, row=0, padx=20, pady=10)

        self.exit_button = ct.CTkButton(master=self, text="Exit", command=sys.exit)
        self.exit_button.grid(column=3, row=0, padx=20, pady=10)

        self.entry_widget = ct.CTkEntry(
            master=self, placeholder_text="Enter template name"
        )

        self.submit_button = ct.CTkButton(master=self, text="Submit")

    def upload_command(self):
        file_path = fd.askopenfilename(
            initialdir="~/Documents/EasyRok", filetypes=pathfinder.FILETYPES[0]
        )

        if not file_path:
            return
        else:
            self.entry_widget.grid(column=0, row=1, padx=10, pady=10)
            self.submit_button.grid(column=0, row=2, padx=10, pady=10)

        def submit(file_path=file_path):
            file_name = self.entry_widget.get().lower()
            xml_obj = xml2json(file_path)
            xml_obj.write_json(temp_name=file_name)
            self.entry_widget.destroy()
            self.submit_button.destroy()

        self.submit_button.configure(command=submit)

    def export_command(self):
        file_path = fd.askopenfilename(
            initialdir=f"{pathfinder.JSON_DIR}", filetypes=pathfinder.FILETYPES[1]
        )

        if not file_path:
            return
        else:
            self.entry_widget.grid(column=1, row=1, padx=10, pady=10)
            self.submit_button.grid(column=1, row=2, padx=10, pady=10)

        def submit():
            xml_name = self.entry_widget.get().lower()
            json_utils.json2xml(
                json_file_path=file_path,
                xml_file_path=f"{pathfinder.XML_EXPORT_DIR}{xml_name}",
            )
            self.entry_widget.destroy()
            self.submit_button.destroy()

        self.submit_button.configure(command=submit)


class TreeView(ttk.Treeview):

    def __init__(self, root) -> None:
        super().__init__(root)
        self.configure(height=200)
        self["column"] = ("diagram",)
        self.column("diagram", width=600, minwidth=200, stretch=tk.YES)

        # Set treevieew heading
        self.heading("#0", text="drawio", anchor=tk.W)
        self.heading("diagram", text="values", anchor="w")

        self.root_node = self.insert("", "end", text="mxfile")

    def generate_tree_view(self, root, data):
        for k, v in data.items():
            if isinstance(v, dict):
                node_id = self.insert(root, "end", text=k)
                self.generate_tree_view(node_id, v)
            else:
                self.insert(root, "end", text=k, values=(v,))

        self.pack(expand=True)


class TabView(ct.CTkTabview):

    def __init__(self, root) -> None:
        super().__init__(root)
        self.pack(fill="both", padx=20, pady=20, expand=True)
        # Add tabs
        self.tab_1 = self.add("Templates")
        self.tab_2 = self.add("Tree View")
        self.tab_3 = self.add("Image View")
        # Add treeview 
        self.tree_view = TreeView(root=self.tab_2)
        self.pack_treeview()


    def pack_treeview(self):
        # TODO add dynamic function to iterate through template directory
        json_path = f"{pathfinder.JSON_DIR}video_codec_test_1_2024-10-17 14:41:45.json"
        json_dict = load_json_file(json_path)
        self.tree_view.generate_tree_view(
            root=self.tree_view.root_node,
            data=json_dict,
        )

@staticmethod
def load_json_file(file_path) -> Dict:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

        return data


if __name__ == "__main__":

    app = Root()
    app.mainloop()
