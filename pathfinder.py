import os
import json


class PathFinder:

    def __init__(self):
        # Path to the data directories to export to other modules
        self.XML_EXPORT_DIR = ''
        self.XML_UPLOAD_DIR = ''
        self.TEMPLATE_DIR = ''
        self.JSON_DIR = ''
        self.CONNECTIONS_DIR = ''
        self.CSV_DIR = ''
        self.TXT_DIR = ''
        self.HTML_DIR = ''
        self.PDF_DIR = ''
        self.PNG_DIR = ''
        self.SVG_DIR = ''
        self.FILETYPES = (('xml files', '*.xml'), ('all files', '*.*')) 

    def get_xml_exports(self):
        """Return the contents of the xml exports dir, sorted by timestamp"""
        
        with os.scandir(self.XML_EXPORT_DIR) as entries:
            file_paths = [entry.path for entry in entries if entry.is_file()]

        return sorted(file_paths, key=lambda x: os.path.getmtime(x)) 

    def get_xml_uploads(self):
        """Return the contents of the xml uploads dir, sorted by timestamp"""
        with os.scandir(self.XML_UPLOAD_DIR) as entries:
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
    
    def get_html_dir(self):
        return self.HTML_DIR
    
    def get_pdf_dir(self):
        return self.PDF_DIR

    def get_png_dir(self):
        return self.PNG_DIR

    def get_svg_dir(self):
        return self.SVG_DIR

    def get_text_dir(self):
        return self.TXT_DIR 
    
    def get_xml_upload_dir(self):
        return self.XML_UPLOAD_DIR

    def get_xml_export_dir(self):
        return self.XML_EXPORT_DIR
    
    def get_connections_dir(self):
        return self.CONNECTIONS_DIR

    def get_template_dir(self):
        return self.TEMPLATE_DIR

    def get_json_dir(self):
        return self.JSON_DIR

    def get_csv_dir(self):
        return self.CSV_DIR

    def get_filetypes(self):
        return self.FILETYPES
    
