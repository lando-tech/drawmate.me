import json
import re


path_var = '/home/landotech/Documents/GitHub/drawmate.me/data/json_files/VideoNew-2024-09-06 13:21:08.825787.json'
pattern1 = r'\{\{.*?\}\}'

av_connections = {}

with open(path_var, 'r', encoding='utf-8') as new_connection:
    data = json.load(new_connection)

for key, value in data['diagram']['mxGraphModel']['root'].items():
    av_connections.update(dict({value.get('id'): value.get('value')}))

values_list = []
for key, value in av_connections.items():
    values_list.append(str(value).strip().split())

connections = []
for i in values_list:
    found = re.findall(pattern1, str(i))
    for match in found:
        filtered_ = match.strip('{').strip('}') 
        print(filtered_)
connections_dict = {item[0]: item[1] for item in connections if len(item) == 2}

#for keys, values in connections_dict.items():
#    print(keys)
