# Initialize imports
import json

from xml.etree import ElementTree as et
from datetime import datetime
from os import path
from utils.pathfinder import PathFinder as pf
from database.db import MyDB


# noinspection PyTypeChecker
class xml2json:

    def __init__(self, file_path):
        # Establish connection to database
        self.conn = MyDB()  

        # Set filepath variable
        self.file_path = file_path
        # Set timestamp for file naming/tracking
        self.timestamp = datetime.now().replace(microsecond=0)
        self.formatted_timestamp = self.timestamp.strftime("%Y-%m-%d_%H-%M-%S")

        # Read the xml as a string
        self.xml_string = et.fromstring(self._read_file_as_bytes())
        # Create xml tree
        self.tree = et.parse(f'{self.file_path}')
        self.root = self.tree.getroot()

        self.current_template = None
        self.template_dict = {"templates": []}
        self.mxcell_connections = {"cell_connections": []} 
        self.mxfile = {
                'diagram': {
                    'mxGraphModel': {
                        'root': {

                        }
                    }
                }
            }

        self.path_finder = pf() 
        
    def _read_file_as_bytes(self):
        # Read the file as bytes to ensure data remains unchanged during extraction
        with open(self.file_path, 'rb') as xml_file:
            data = xml_file.read()

        return data

    def _preserve_escape_chars(self, text):
        # Ensure the text is returned as is to preserve the escape characters draw.io requires in its xml format
        return text

    def create_dict(self):
        # Iterate through the xml root and extract the needed values. Values are then stored inside a dictionary
        num_cells = 0
        num_points = 0
        num_array = 0
        for item in self.xml_string.iter():
            if item.tag == "mxfile":
                pass
            elif item.tag == "diagram":
                self.mxfile["diagram"].update(
                    dict(self._preserve_escape_chars(item.attrib)))
            elif item.tag == "mxGraphModel":
                self.mxfile["diagram"]["mxGraphModel"].update(
                    dict(self._preserve_escape_chars(item.attrib)))
            elif item.tag == "mxCell":
                num_cells += 1
                self.mxfile["diagram"]["mxGraphModel"]["root"].update(
                    dict({f"mxCell-{num_cells}": self._preserve_escape_chars(item.attrib)}))
            elif item.tag == "mxGeometry":
                self.mxfile["diagram"]["mxGraphModel"]["root"][f"mxCell-{num_cells}"].update(
                    dict({"mxGeometry": self._preserve_escape_chars(item.attrib)}))
            elif item.tag == "Array":
                num_array = num_cells
                self.mxfile["diagram"]["mxGraphModel"]["root"][f"mxCell-{num_cells}"]["mxGeometry"].update(
                    dict({"Array": self._preserve_escape_chars(item.attrib)}))
            elif item.tag == "mxPoint" and num_array == num_cells:
                num_points += 1
                self.mxfile["diagram"]["mxGraphModel"]["root"][f"mxCell-{num_cells}"]["mxGeometry"]["Array"].update(
                    dict({f"mxPoint-{num_points}": self._preserve_escape_chars(item.attrib)}))
            elif item.tag == "mxPoint":
                num_points += 1
                self.mxfile["diagram"]["mxGraphModel"]["root"][f"mxCell-{num_cells}"]["mxGeometry"].update(
                    dict({f"mxPoint-{num_points}": self._preserve_escape_chars(item.attrib)}))

        return self.mxfile

    def write_json(self, temp_name: str):
        # Write the json file to disk to store as a future template
        with open(f'{self.path_finder.JSON_DIR}{temp_name}_{self.timestamp}.json', 'w') as cell:
            json.dump(obj=self.create_dict(), fp=cell, indent=4, ensure_ascii=False)
        
        if 'audio' in temp_name.lower():
            db_name = 'templates.db'
            table_name = 'audio_templates' 
            self.conn.initialize_database(db_name=db_name, table_name=table_name)
            self.conn.add_entry(i=self.get_current_template(temp_name), o='Test', db_name=db_name, t_name=table_name)
        elif 'video' in temp_name.lower():
            db_name = 'templates.db'
            table_name = 'video_templates' 
            self.conn.initialize_database(db_name=db_name, table_name=table_name)
            self.conn.add_entry(i=self.get_current_template(temp_name), o='Test', db_name=db_name, t_name=table_name)

            # self.get_template_dict(temp_name)
            # self.create_json_template(temp_name)

    def from_string(self):
        # Returns the xml string as is to ensure proper encoding
        return self.xml_string

    def get_current_template(self, temp_name: str):
        # Returns the current template being created/updated
        self.current_template = f"{temp_name}_{self.formatted_timestamp}.json"
        return self.current_template

    def get_template_dict(self, temp_name: str):
        # Returns the template dictionary
        self.template_dict["templates"].append(self.get_current_template(temp_name))
        return self.template_dict

    def create_json_template(self, temp_name: str):
        # Update template if none is present, else create template
        if (path.exists(f'{self.path_finder.TEMPLATE_DIR}template_list.json')
                and path.getsize(f'{self.path_finder.TEMPLATE_DIR}template_list.json') > 0):
            self.update_json_template(temp_name)
        else:
            with open(f'{self.path_finder.TEMPLATE_DIR}template_list.json', 'w') as temp:
                json.dump(self.template_dict, temp, indent=4)
                print("file saved to disk")

    def update_json_template(self, temp_name: str):
        # Update current list of templates inside the json file
        with open(f'{self.path_finder.TEMPLATE_DIR}template_list.json', 'r') as temp_list:
            loaded_list = json.load(temp_list)
            for key, value in loaded_list.items():
                value.append(self.get_current_template(temp_name))
                updated_json = {"templates": value}
                with open(f'{self.path_finder.TEMPLATE_DIR}template_list.json', 'w') as update:
                    json.dump(updated_json, update, indent=4)

    def update_connections_list(self, cell):
        self.mxcell_connections["cell_connections"].append(cell)
    
    def write_connections_json(self, connect_list):
        connect_path = f'{self.path_finder.JSON_DIR}connections.json'
        if path.exists(connect_path) and path.getsize(connect_path) > 0:
            with open(connect_path, 'r') as cell_update:
                current_cell_data = json.load(cell_update)
                for key, value in current_cell_data:
                    value.append(connect_list)
                    updated_cell_data = {"cell_connections": value}
                    with open(connect_path, 'w') as new_connections:
                        json.dump(updated_cell_data, new_connections)
        else:
            with open(connect_path, 'w', encoding='utf-8') as init_connections:
                json.dump(connect_list, init_connections)

