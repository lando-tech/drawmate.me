import os
import json


class PathFinder:

    def __init__(self):
        # Path to the data directories to export to other modules
        self.XML_EXPORT_DIR = f'{self.get_project_dir()}/data/xml_files/xml_exports/'
        self.XML_UPLOAD_DIR = f'{self.get_project_dir()}/data/xml_files/xml_uploads/'
        self.TEMPLATE_DIR = f'{self.get_project_dir()}/data/templates/'
        self.JSON_DIR = f'{self.get_project_dir()}/data/json_files/'
        self.CONNECTIONS_DIR = f'{self.get_project_dir()}/data/connections/'
        self.CSV_DIR = f'{self.get_project_dir()}/data/csv_files/'
        self.TXT_DIR = f'{self.get_project_dir()}/data/txt_files/'
        self.HTML_DIR = f'{self.get_project_dir()}/data/html_files/'
        self.PDF_DIR = f'{self.get_project_dir()}/data/pdf_files/'
        self.PNG_DIR = f'{self.get_project_dir()}/data/png_files/'
        self.SVG_DIR = f'{self.get_project_dir()}/data/svg_files/'
        self.SCRIPTS_DIR = f'{self.get_project_dir()}/scripts/drawio_cli.sh'
        self.COLOR_PALLETE_TOML = f'{self.get_project_dir()}/data/color_palettes/one_dark.toml'
        self.CONFIG_TOML = f'{self.get_project_dir()}/config/config.toml'
        self.GRAPH_CONFIG_TOML = f'{self.get_project_dir()}/config/graph_config.toml'
        self.FILETYPES = [(('xml files', '*.xml'), ('all files', '*.*')),
                          (('json files', '*.json'), ('all files', '*.*')),
                          (('pdf files', '*.pdf'), ('all files', '*.*')),
                          (('toml files', '*.toml'), ('all files', '*.*'))]
    
    def get_project_dir(self):
        """Return the root directory of the project"""
        path_finder_dir = os.path.dirname(os.path.abspath(__file__))
        
        while not os.path.isfile(os.path.join(path_finder_dir, 'anchor.toml')) and path_finder_dir != '/':
            path_finder_dir = os.path.dirname(path_finder_dir)

        if path_finder_dir == '/':
            raise RuntimeError("Project root directory not found")

        return path_finder_dir

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
        template_list = None 
        with open(f'{self.TEMPLATE_DIR}template_list.json', 'r', encoding='utf-8') as view:
            template_view = json.load(view)
            
            for key, value in template_view.items():
                template_list = value
            
            return template_list
    
