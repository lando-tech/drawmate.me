import os 
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.json2xml import JsonUtils
from utils.pathfinder import PathFinder
import json
import re

js = JsonUtils()
pf = PathFinder()
json_dir = pf.JSON_DIR + 'VideoMatrix_test1_2024-10-07_11-20-46.json'


def update_json(json_file_path, updates):
    """Update JSON data based on the provided updates."""
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    #Apply updates to the data
    for key, value in updates.items():
        #Implement more complex logic as needed for nested updates
        if isinstance(value, dict):
            data[key].update(value)
        else:
            data[key] = value

    #Write the updated JSON back to the file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def update_connections(file_path, file_name):
    pattern1 = r'\{\{.*?\}\}'

    with open(file_path, 'r', encoding='utf-8') as new_connection:
        data = json.load(new_connection)
        for keys, values in data["diagram"]["mxGraphModel"]["root"].items():
            result = re.sub(pattern1, '{{test}}', str(values.get('value')))
            values["value"] = result
        with open(file_name,
                  'w',
                  encoding='utf-8') as update_connects:
            json.dump(data, update_connects, indent=4)
            print("Connections Updated")


def get_cell_count(json_data: dict):
    cell_count = None
    for k, v in json_data.items():
        if isinstance(v, dict) and 'root' in v:
            for key, value in v.items():
                cell_count = len(value.values())
                return cell_count
        if isinstance(v, dict):
            result = get_cell_count(v)
            if result is not None:
                return result
    return None
                

def json_to_dict(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data 


def get_connections(json_data):
    pattern1 = r'\{\{.*?\}\}'
    matches = []
    for k, v in json_data['diagram']['mxGraphModel']['root'].items():
        result = re.findall(pattern=pattern1, string=str(v.get('value')))
        if not result:
            pass
        else:
            matches.append(result)
    return matches

