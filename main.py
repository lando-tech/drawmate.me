# Import database class
from database.db import MyDB
# Instantiate database class
conn = MyDB()
# Query database and get iterator
rows = conn.query_db('templates.db', 'video_templates')
# Iteration goes here:


# Import utils
from utils.update import *
from utils.pathfinder import PathFinder

# Init pathfiner class
pf = PathFinder()
# Get file path
json_path = pf.JSON_DIR + 'VideoMatrixTest1_2024-10-11_08-21-05.json'
# Convert json to dict
json_dir = json_to_dict(json_path)
# Get mxCell count 
cell_count = get_cell_count(json_dir)
update_var = r'{{input}}' 
print(update_var)


# update_connections(json_path, 'new_test.json')
