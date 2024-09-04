import os
import json

XML_DIRECTORY = '/home/landotech/Documents/GitHub/diagram_me/data/xml_files/'


def export_xml_files():
    directory = XML_DIRECTORY
    with os.scandir(directory) as entries:
        file_paths = [entry.path for entry in entries if entry.is_file()]

    return file_paths


def export_template():
    with open('../data/templates/template_list.json', 'r') as export:
        exported_data = json.load(export)

    return exported_data["templates"][-1]

