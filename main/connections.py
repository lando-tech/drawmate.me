import json
import re

pattern1 = r'\{\{.*?\}\}'

av_connections = {}

with open('data/json_files/template2.json') as new_connection:
    data = json.load(new_connection)

for key, value in data['mxfile']['diagram']['mxGraphModel']['root'].items():
    av_connections.update(dict({value.get('id'): value.get('value')}))

values_list = []
for key, value in av_connections.items():
    values_list.append(str(value).strip().split())

connections = []
for i in values_list:
    found = re.findall(pattern1, str(i))
    if found:
        connections.append(found)

connections_dict = {item[0]: item[1] for item in connections if len(item) == 2}

for key, value in connections_dict.items():
    print(key, value)

