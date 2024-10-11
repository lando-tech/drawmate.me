import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.pathfinder import PathFinder
from db import MyDB 
import json


pf = PathFinder()


def check_for_updates():
    template_dir = pf.TEMPLATE_DIR
    if os.path.isfile(f'{template_dir}template_list.json'):
        with open(f'{template_dir}template_list.json', 'r', encoding='utf-8') as updates:
            data = json.load(updates)


conn = MyDB()
conn.query_db()
