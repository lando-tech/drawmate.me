# import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from database.db import MyDB

# conn = MyDB()

# query = conn.query_db('templates.db', 'audio_templates')

# for i in query:
#     print(i[1].split('_')[0])
import toml

with open("/home/landotech/Documents/config_templates/color_palettes/one_dark.toml", "r", encoding="utf-8") as file:
    data = toml.load(file)
    color_list = [] 
    for k, v in data.items():
        if isinstance(v, dict):
            for color_name, color_value in v.items():
                print(color_name, color_value)
