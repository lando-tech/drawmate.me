import json
import re   


def update_connections(path_var):
    
    pattern1 = r'\{\{.*?\}\}'

    with open(path_var, 'r', encoding='utf-8') as new_connection:
        data = json.load(new_connection)
        
        for keys, values in data["diagram"]["mxGraphModel"]["root"].items():
            result = re.sub(pattern1, '{{test}}', str(values.get('value')))
            values["value"] = result
        
        with open('/home/landotech/Documents/GitHub/drawmate.me/data/json_files/VideoCodecTest3-2024-09-08 23:13:30.752556.json',
                  'w',
                  encoding='utf-8') as update_connects:
            json.dump(data, update_connects, indent=4)
            print("Connections Updated")


f_path = '/home/landotech/Documents/GitHub/drawmate.me/data/json_files/VideoCodecTest3-2024-09-08 23:13:30.752556.json'
 
update_connections(f_path)

