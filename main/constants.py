import os
import json


class PathFinder:

    def __init__(self):
        # Path to the data directories to export to other modules
        self.XML_DIR = '/home/landotech/Documents/GitHub/drawmate.me/data/xml_files/'
        self.TEMPLATE_DIR = '/home/landotech/Documents/GitHub/drawmate.me/data/templates/'
        self.JSON_DIR = '/home/landotech/Documents/GitHub/drawmate.me/data/json_files/'
        self.CONNECTIONS_DIR = '/home/landotech/Documents/GitHub/drawmate.me/data/connections/'
        self.CSV_DIR = '/home/landotech/Documents/GitHub/drawmate.me/data/csv_files/'
        self.TXT_DIR = '/home/landotech/Documents/GitHub/drawmate.me/data/txt_files/'
        self.FILETYPES = (('xml files', '*.xml'), ('all files', '*.*')) 

    def export_xml_files(self):
        """Return the contents of the xml directory sorted by timestamp"""
        
        with os.scandir(self.XML_DIR) as entries:
            file_paths = [entry.path for entry in entries if entry.is_file()]

        return sorted(file_paths, key=lambda x: os.path.getmtime(x)) 


    def export_json_templates(self):
        """Return the contents of the json directory sorted by timestamp""" 
        
        with os.scandir(self.JSON_DIR) as entries:
            file_paths = [entry.path for entry in entries if entry.is_file()]

        return sorted(file_paths, key=lambda x: os.path.getmtime(x))


    def export_template(self):
        """Return the latest entry in the template_list"""
        with open(f'{self.TEMPLATE_DIR}template_list.json', 'r', encoding='utf-8') as export:
            exported_data = json.load(export)

        return exported_data["templates"][-1]


    def view_templates(self):
        """Return a list of current templates"""
        
        with open(f'{self.TEMPLATE_DIR}template_list.json', 'r', encoding='utf-8') as view:
            template_view = json.load(view)
            
            for key, value in template_view.items():
                template_list = value
            
            return template_list

    def get_text_dir(self):
        return self.TXT_DIR 
