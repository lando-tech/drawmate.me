import json

        

#def update_json(json_file_path):
    #with open(json_file_path, 'r', encoding='utf-8') as json_file:
        #data = json.load(json_file)

    # Apply updates to the data
    # for key, value in updates.items():
        # Implement more complex logic as needed for nested updates
        # if isinstance(value, dict):
        # data[key].update(value)
        # else:
        # data[key] = value

    # Write the updated JSON back to the file
    #with open(json_file_path, 'w', encoding='utf-8') as json_file:
        #json.dump(data, json_file, indent=4, ensure_ascii=False)


# Example updates: adjust according to JSON structure
#updates = {
    #'mxCell': [
        #{'id': 'new_id', 'value': 'new_value'}
    #]
#}

# update_json(json_file_path)

file_path = 'C:/Users/aaron/GitHub/drawmate.me/data/template.json'
search_pattern = ['HDMI', 'DTP', 'USB',  r'\{\{.*?\}\}']

with open(file_path, 'r', encoding='utf-8') as data:
    search_ = json.load(data)
    
    for key, value in search_['diagram']['mxGraphModel']['root'].items():
        for match in search_pattern:
            if match in value:
                print(value)
