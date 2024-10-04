from db import MyDB
from pathfinder import PathFinder
from xml2json import xml2json
from json2xml import JsonUtils
import os
import pathlib
import pandas
import tkinter as tk 
from tkinter import filedialog as fd 


class RootWindow(PathFinder, JsonUtils):

    def __init__(self) -> None:
        super().__init__()
        # Init root window
        self.root = tk.Tk()
        # Set minsize of root window
        self.root.minsize(width=500, height=500)
        # Add menubar to root 
        self.menu_bar()
        self.upload_button_xml()
        self.export_button_json()
        self.root.mainloop()
        # Initialize modules
        self.pf = PathFinder()
    
    def menu_bar(self):
        # Create menu bar
        menu_bar = tk.Menu(master=self.root)
        # Create filemenu
        filemenu = tk.Menu(master=menu_bar, tearoff=0)
        # Set commands for filemenu 
        filemenu.add_command(label='Upload', command=None)
        filemenu.add_command(label='Open', command=None)
        filemenu.add_command(label='Save', command=None)
        filemenu.add_command(label='Export', command=None)
        # Call root to init menubar
        menu_bar.add_cascade(label='File', menu=filemenu)
        self.root.config(menu=menu_bar)

    def upload_button_xml(self):
        # Upload xml file to app and convert to json
        button = tk.Button(master=self.root)
        button.pack()
        button.config(text='Upload XML', command=self.open_input_dialog)
       
    def export_button_json(self):
        # Export json template to xml
        export_button = tk.Button(master=self.root)
        export_button.pack()
        export_button.config(text='Export JSON', command=self.export_file)


    def upload_xml(self, file_path, temp_name):
        # Function call for upload button
        self.xml_util = xml2json(file_path)
        self.xml_util.write_json(temp_name=temp_name)

    def export_file(self):
        # Function call for export button
        project_dir = self.get_json_dir()
        xml_path = f'{self.XML_EXPORT_DIR}/export.drawio.xml'         
        file_path = fd.askopenfilename(initialdir=f'{project_dir}', filetypes=self.FILETYPES) 
        self.json2xml(file_path, xml_path)

    def open_input_dialog(self):
        # Open filedialog and save filepath into variable
        file_path = fd.askopenfilename(initialdir='~/Downloads', filetypes=self.FILETYPES) 
        if not file_path:
            return
        # Open dialog to provide template name
        dialog = tk.Toplevel()
        dialog.title('Entry')
        dialog.minsize(50, 20)
        tk.Label(dialog, text='Enter template name:').pack(padx=10, pady=10)
        
        entry_1 = tk.Entry(dialog)
        entry_1.pack(padx=10, pady=10)
        
        def submit():
            # Submit the template name and filepath to the upload function for processing
            temp_name = entry_1.get()
            dialog.destroy()
            self.upload_xml(file_path=file_path, temp_name=temp_name)

        # Submit button
        tk.Button(dialog, text='Submit', command=submit).pack()


if __name__ == "__main__":
    RootWindow()
