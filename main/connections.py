import json
import re

path_var = '/home/landotech/Documents/GitHub/drawmate.me/data/json_files/VideoNew-2024-09-06 13:21:08.825787.json'
pattern1 = r'\{\{.*?\}\}'


def update_json_template(temp_name: str):
    # Update current list of templates inside the json file
    with open('../data/templates/template_list.json', 'r') as temp_list:
        loaded_list = json.load(temp_list)
        for key, value in loaded_list.items():
            value.append(self.get_current_template(temp_name))
            updated_json = {"templates": value}
            with open('../data/templates/template_list.json', 'w') as update:
                json.dump(updated_json, update, indent=4)



with open(path_var, 'r', encoding='utf-8') as new_connection:
    data = json.load(new_connection)
    
    for keys, values in data["diagram"]["mxGraphModel"]["root"].items():
        result = re.sub(pattern1, '{{test}}', str(values.get('value')))
        values["value"] = result
    
    with open('/home/landotech/Documents/GitHub/drawmate.me/data/json_files/ConnectionsModuleTest.json', 'w', encoding='utf-8') as update_connects:
        json.dump(data, update_connects, indent=4)
        update_json_template(update_connects)
        print("Connections Updated")



