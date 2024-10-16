# Import utils
from utils.update import *
from utils.pathfinder import PathFinder

# Init pathfiner class
pf = PathFinder()
# Get file path
json_path = pf.JSON_DIR + 'CampMujak_Test_3_2024-10-11_15-00-26.json'
# Convert json to dict
json_dir = json_to_dict(json_path)
# Get mxCell count 
cell_count = get_cell_count(json_dir)

check_connection(json_dir)

