import os
import json

XML_DIRECTORY = '/home/landotech/Documents/GitHub/drawmate.me/data/xml_files/'
TEMPLATE_DIR = '/home/landotech/Documents/GitHub/drawmate.me/data/templates/'


def export_xml_files():
    directory = XML_DIRECTORY
    with os.scandir(directory) as entries:
        file_paths = [entry.path for entry in entries if entry.is_file()]

    return file_paths


def export_template():
    with open('../data/templates/template_list.json', 'r') as export:
        exported_data = json.load(export)

    return exported_data["templates"][-1]


def view_templates():
    directory = TEMPLATE_DIR
    num_templates = 0
    template_list = []
    with open(f'{directory}/template_list.json', 'r') as view:
        template_view = json.load(view)
        
        for key, value in template_view.items():
            template_list.append(f'[{num_templates}] {value}')

        return template_list

