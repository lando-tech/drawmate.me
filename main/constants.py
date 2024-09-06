import os
import json

XML_DIRECTORY = '/home/landotech/Documents/GitHub/drawmate.me/data/xml_files/'
TEMPLATE_DIR = '/home/landotech/Documents/GitHub/drawmate.me/data/templates/'
JSON_DIRECTORY = '/home/landotech/Documents/GitHub/drawmate.me/data/json_files/'


def export_xml_files():
    directory = XML_DIRECTORY
    with os.scandir(directory) as entries:
        file_paths = [entry.path for entry in entries if entry.is_file()]

    return sorted(file_paths, key=lambda x: os.path.getmtime(x)) 

def export_json_templates():
    directory = JSON_DIRECTORY
    with os.scandir(directory) as entries:
        file_paths = [entry.path for entry in entries if entry.is_file()]

    return sorted(file_paths, key=lambda x: os.path.getmtime(x))

def export_template():
    with open('../data/templates/template_list.json', 'r') as export:
        exported_data = json.load(export)

    return exported_data["templates"][-1]


def view_templates():
    directory = TEMPLATE_DIR
    with open(f'{directory}/template_list.json', 'r') as view:
        template_view = json.load(view)
        
        for key, value in template_view.items():
            template_list = value
        
        return template_list

