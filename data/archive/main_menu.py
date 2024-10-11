import tkinter as tk 
from tkinter import ttk
from tkinter import filedialog as fd

from utils.xml2json import xml2json
from utils.json2xml import JsonUtils
from utils.pdf_handler import DataExtract
from config.config import AppConfig


class MainMenu(AppConfig):

    def __init__(self, master) -> None: 
        super().__init__()
        # Init main menu
        self.menu_frame = tk.Frame(master=master)
        self.menu_frame.pack(side='top', padx=10, pady=10)
        self.menu_frame.config(relief='flat', borderwidth=1)
        
        # Add label to frame
        self.main_label = tk.Label(master=self.menu_frame)
        self.main_label.config(text='drawmate')

        # Pack main_menu label
        self.main_label.pack(side='top')

        # Add buttons
        self.upload_xml_button()
        self.upload_pdf_button()
        self.export_json_button()
        self.view_templates_button()

    def main_menu_config(self, color_palette, font):
        pass

    def upload_xml_button(self):
        # Upload xml file to app and convert to json
        xml_button = tk.Button(master=self.menu_frame)
        xml_button.pack(side='left', padx=10, pady=10, expand=True)
        xml_button.config(text='Upload XML',
                      command=self.upload_xml_command,
                      relief='flat',
                      borderwidth=2)

    def upload_pdf_button(self):
        # Button to upload pdf. File is passed to pdfhandler class to extract relevant data
        pdf_button = tk.Button(master=self.menu_frame)
        pdf_button.pack(side='left', padx=10, pady=10, expand=True)
        pdf_button.config(text='Upload PDF',
                          command=self.upload_pdf_command,
                          relief='flat',
                          borderwidth=2)

    def export_json_button(self):
        # Export json template to xml
        export_button = tk.Button(master=self.menu_frame)
        export_button.pack(side='left', padx=10, pady=10, expand=True)
        export_button.config(text='Export JSON',
                             command=self.export_json_command,
                             relief='flat',
                             borderwidth=2)

    def view_templates_button(self):
        # Button to view json templates
        view_button = tk.Button(master=self.menu_frame)
        view_button.pack(side='left', padx=10, pady=10, expand=True)
        view_button.config(text='View Templates',
                           command=None,
                           relief='flat',
                           borderwidth=2)

    def upload_xml_command(self):
        file_path = fd.askopenfilename(initialdir='~/Downloads',
                                       filetypes=self.FILETYPES)
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
            xml_util = xml2json(file_path)
            xml_util.write_json(temp_name)

        # Submit button
        tk.Button(dialog, text='Submit', command=submit).pack()


    def upload_pdf_command(self):
        """
        Calls the pdf conversion method from the DataExtract class.
        This method writes a txt file with the scrapped text from
        the file operations. See pdf_handler.py docs for more info.
        """
        # Open dialog to provide template name
        dialog = tk.Toplevel()
        dialog.title('Entry')
        dialog.minsize(50, 20)
        tk.Label(dialog, text='Enter name for file:').pack(padx=10, pady=10)

        # Set entry to retrieve user input
        entry_1 = tk.Entry(dialog)
        entry_1.pack(padx=10, pady=10)

        def submit():
            """
            Nested function used to submit the filepath/name of new file.
            """

            # Submit the template name and filepath to the upload function for processing
            file_name = entry_1.get()
            # Destroy dialog once input is retrieved
            dialog.destroy()
            # Call pdf conversion method
            extractor = DataExtract()
            extractor.convert_pdf(new_file_name=file_name)

        # Submit button for user entry
        tk.Button(dialog, text='Submit', command=submit).pack()
    
    def export_json_command(self):
        """
        Opens a filedialog in the JSON directory and retrieve user entry
        to name the new file.
        """
        # Open filedialog and save filepath into variable
        project_dir = self.JSON_DIR
        file_path = fd.askopenfilename(initialdir=f'{project_dir}', filetypes=self.FILETYPES[1])

        # Ensure filepath exists
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
            extractor = JsonUtils()
            extractor.json2xml(file_path, xml_f_path)

        # Submit button
        tk.Button(dialog, text='Submit', command=submit).pack()

