import json
import re

       

def update_json(json_file_path):
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


# Example updates: adjust according to JSON structure
updates = {
    'mxCell': [
        {'id': 'new_id', 'value': 'new_value'}
    ]
}

json_file_path = ""
update_json(json_file_path)



def update_connections(path_var):
   
    pattern1 = r'\{\{.*?\}\}'

    with open(path_var, 'r', encoding='utf-8') as new_connection:
        data = json.load(new_connection)
       
        for keys, values in data["diagram"]["mxGraphModel"]["root"].items():
            result = re.sub(pattern1, '{{test}}', str(values.get('value')))
            values["value"] = result
       
        with open('<file path>',
                  'w',
                  encoding='utf-8') as update_connects:
            json.dump(data, update_connects, indent=4)
            print("Connections Updated")

