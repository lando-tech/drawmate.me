import json
import re


path_var = '/home/landotech/Documents/GitHub/drawmate.me/data/json_files/VideoNew-2024-09-06 13:21:08.825787.json'
pattern1 = r'\{\{.*?\}\}'


with open(path_var, 'r', encoding='utf-8') as new_connection:
    data = json.load(new_connection)
    
    for keys, values in data["diagram"]["mxGraphModel"]["root"].items():
        result = re.sub(pattern1, '{{test}}', str(values.get('value')))
        values["value"] = result
    
    with open('/home/landotech/Documents/GitHub/drawmate.me/data/json_files/ConnectionsModuleTest.json', 'w', encoding='utf-8') as update_connects:
        json.dump(data, update_connects, indent=4)
        print("Connections Updated")

