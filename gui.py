from db import MyDB
from pathfinder import PathFinder
from xml2json import xml2json
from json2xml import JsonUtils
from pdf_handler import DataExtract 
import os
import pathlib
import pandas
import tkinter as tk 
from tkinter import filedialog as fd 


class RootWindow(PathFinder, JsonUtils, DataExtract):

    def __init__(self) -> None:
        super().__init__()
        # Init root window
        self.root = tk.Tk()

        # Configure root window 
        self.root.minsize(width=500, height=500)
        self.root.config(bg='#282828')

        # Add frame to left side of window 
        self.l_frame = tk.Frame(master=self.root)
        self.l_frame.grid(column=0, row=0)

        # Configure l_frame
        self.l_frame.config(background='#a89984')

        # Init menu buttons for l_frame
        self.upload_button_xml()
        self.upload_button_pdf()
        self.export_button_json()

        # Add menu bar
        self.menu_bar()
        
        # Call mainloop
        self.root.mainloop()
    
    def menu_bar(self):
        # Create menu bar
        menu_bar = tk.Menu(master=self.root)
        menu_bar.config(background='#282828',
                        foreground='white',
                        activebackground='#a89984')
        # Create filemenu
        filemenu = tk.Menu(master=menu_bar, tearoff=0)
        # Set commands for filemenu 
        filemenu.add_command(label='Upload',
                             command=None,
                             background='#282828',
                             foreground='white',
                             activebackground='#a89984')
        filemenu.add_command(label='Open',
                             command=None,
                             background='#282828',
                             foreground='white',
                             activebackground='#a89984')
        filemenu.add_command(label='Save',
                             command=None,
                             background='#282828',
                             foreground='white',
                             activebackground='#a89984')
        filemenu.add_command(label='Export',
                             command=None,
                             background='#282828',
                             foreground='white',
                             activebackground='#a89984')
        # Call root to init menubar
        menu_bar.add_cascade(label='File', menu=filemenu)
        self.root.config(menu=menu_bar)

    def upload_button_xml(self):
        # Upload xml file to app and convert to json
        button = tk.Button(master=self.l_frame)
        button.pack(padx=10, pady=10)
        button.config(text='Upload XML',
                      command=self.open_input_dialog_xml,
                      background='#282828',
                      foreground='white',
                      activebackground='#a89984',
                      activeforeground='black')

    def upload_button_pdf(self):
        pdf_button = tk.Button(master=self.l_frame)
        pdf_button.pack(padx=10, pady=10)
        pdf_button.config(text='Upload PDF',
                          command=self.open_input_dialog_pdf,
                          background='#282828',
                          foreground='white',
                          activebackground='#a89984',
                          activeforeground='black')
       
    def export_button_json(self):
        # Export json template to xml
        export_button = tk.Button(master=self.l_frame)
        export_button.pack(padx=10, pady=10)
        export_button.config(text='Export JSON',
                             command=self.open_input_dialog_json,
                             background='#282828',
                             foreground='white',
                             activebackground='#a89984',
                             activeforeground='black')

    def upload_xml(self, file_path, temp_name):
        # Function call for upload button
        self.xml_util = xml2json(file_path)
        self.xml_util.write_json(temp_name=temp_name)

    def export_json(self, file_path, xml_path):
        # Function call for export button
        self.json2xml(file_path, xml_path)

    def open_input_dialog_xml(self):
        # Open filedialog and save filepath into variable
        file_path = fd.askopenfilename(initialdir='~/Downloads', filetypes=self.FILETYPES[0])
        if not file_path:
            return
        # Open dialog to provide template name
        dialog = tk.Toplevel()
        dialog.title('Entry')
        dialog.minsize(50, 20)
        tk.Label(dialog, text='Enter name for file:').pack(padx=10, pady=10)
        
        entry_1 = tk.Entry(dialog)
        entry_1.pack(padx=10, pady=10)
        
        def submit():
            # Submit the template name and filepath to the upload function for processing
            temp_name = entry_1.get()
            dialog.destroy()
            self.upload_xml(file_path=file_path, temp_name=temp_name)

        # Submit button
        tk.Button(dialog, text='Submit', command=submit).pack()

    def open_input_dialog_json(self):
        # Open filedialog and save filepath into variable
        project_dir = self.get_json_dir()
        file_path = fd.askopenfilename(initialdir=f'{project_dir}', filetypes=self.FILETYPES[1])
        if not file_path:
            return
        # Open dialog to provide template name
        dialog = tk.Toplevel()
        dialog.title('Entry')
        dialog.minsize(50, 20)
        tk.Label(dialog, text='Enter name for file:').pack(padx=10, pady=10)
        
        entry_1 = tk.Entry(dialog)
        entry_1.pack(padx=10, pady=10)
        
        def submit():
            # Submit the template name and filepath to the upload function for processing
            file_name = entry_1.get()
            xml_f_path = f'{self.XML_EXPORT_DIR}/{file_name}.drawio.xml'
            dialog.destroy()
            self.export_json(file_path, xml_f_path)

        # Submit button
        tk.Button(dialog, text='Submit', command=submit).pack()

    def open_input_dialog_pdf(self):
        # Open dialog to provide template name
        dialog = tk.Toplevel()
        dialog.title('Entry')
        dialog.minsize(50, 20)
        tk.Label(dialog, text='Enter name for file:').pack(padx=10, pady=10)
        
        entry_1 = tk.Entry(dialog)
        entry_1.pack(padx=10, pady=10)
        
        def submit():
            # Submit the template name and filepath to the upload function for processing
            file_name = entry_1.get()
            dialog.destroy()
            self.convert_pdf(new_file_name=file_name)
        # Submit button
        tk.Button(dialog, text='Submit', command=submit).pack()


if __name__ == "__main__":
    RootWindow()
