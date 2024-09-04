import json

from xml.etree import ElementTree as et
from datetime import datetime
from os import path
from main.constants import export_xml_files


# noinspection PyTypeChecker
class xml2json:

    def __init__(self, file_path):
        self.file_path = file_path
        self.timestamp = datetime.today()
        self.xml_string = et.fromstring(self._read_file_as_bytes())
        self.tree = et.parse(f'{self.file_path}')
        self.root = self.tree.getroot()
        self.current_template = None
        self.template_dict = {"templates": []}
        self.mxfile = {
                'diagram': {
                    'mxGraphModel': {
                        'root': {

                        }
                    }
                }
            }

    def _read_file_as_bytes(self):
        with open(self.file_path, 'rb') as xml_file:
            data = xml_file.read()

        return data

    def _preserve_escape_chars(self, text):
        return text

    def create_dict(self):
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

    def write_json(self):

        with open(f'../data/json_files/{self.get_current_template()}', 'w') as cell:
            json.dump(obj=self.create_dict(), fp=cell, indent=4, ensure_ascii=False)

        self.get_template_dict()
        self.create_template_json()

    def from_string(self):
        return self.xml_string

    def get_current_template(self):
        self.current_template = f"template{self.timestamp}.json"
        return self.current_template

    def get_template_dict(self):
        self.template_dict["templates"].append(self.get_current_template())
        return self.template_dict

    def create_template_json(self):

        if (path.exists('../data/templates/template_list.json')
                and path.getsize('../data/templates/template_list.json') > 0):
            self.update_json()
        else:
            with open('../data/templates/template_list.json', 'w') as temp:
                json.dump(self.template_dict, temp, indent=4)
                print("file saved to disk")

    def update_json(self):

        with open('../data/templates/template_list.json', 'r') as temp_list:
            loaded_list = json.load(temp_list)
            for key, value in loaded_list.items():
                value.append(self.get_current_template())
                updated_json = {"templates": value}
                with open('../data/templates/template_list.json', 'w') as update:
                    json.dump(updated_json, update, indent=4)


xml_obj = xml2json("../data/xml_files/Audio_DMP64_CP108.drawio.xml")
xml_obj.write_json()
