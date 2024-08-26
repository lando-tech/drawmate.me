import json
from xml.etree import ElementTree as et


# noinspection PyTypeChecker
class xml2json:

    def __init__(self, file_path):
        self.file_path = file_path
        self.xml_string = et.fromstring(self._read_file_as_bytes())
        self.tree = et.parse(f'{self.file_path}')
        self.root = self.tree.getroot()
        self.mxfile = {
            'mxfile': {
                'diagram': {
                    'mxGraphModel': {
                        'root': {

                        }
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
        for item in self.xml_string.iter():
            if item.tag == "mxfile":
                self.mxfile["mxfile"].update(
                    dict(self._preserve_escape_chars(item.attrib)))
            elif item.tag == "diagram":
                self.mxfile["mxfile"]["diagram"].update(
                    dict(self._preserve_escape_chars(item.attrib)))
            elif item.tag == "mxGraphModel":
                self.mxfile["mxfile"]["diagram"]["mxGraphModel"].update(
                    dict(self._preserve_escape_chars(item.attrib)))
            elif item.tag == "mxCell":
                num_cells += 1
                self.mxfile["mxfile"]["diagram"]["mxGraphModel"]["root"].update(
                    dict({f"mxCell-{num_cells}": self._preserve_escape_chars(item.attrib)}))
            elif item.tag == "mxGeometry":
                self.mxfile["mxfile"]["diagram"]["mxGraphModel"]["root"][f"mxCell-{num_cells}"].update(
                    dict({"mxGeometry": self._preserve_escape_chars(item.attrib)}))
            elif item.tag == "mxPoint":
                num_points += 1
                self.mxfile["mxfile"]["diagram"]["mxGraphModel"]["root"][f"mxCell-{num_cells}"].update(
                    dict({f"mxPoint-{num_points}": self._preserve_escape_chars(item.attrib)}))

        return self.mxfile

    def write_json(self):

        with open('../data/json_files/template2.json', 'w') as cell:
            json.dump(obj=self.create_dict(), fp=cell, indent=4, ensure_ascii=False)

    def from_string(self):
        return self.xml_string


xml_path = '/home/landotech/PythonProjects/diagram_me/data/xml_files/Video_CP108_2codec.drawio.xml'
xml_obj = xml2json(xml_path)
xml_obj.write_json()
