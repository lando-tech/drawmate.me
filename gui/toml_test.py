import toml
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.pathfinder import PathFinder

pf = PathFinder()


with open(pf.GRAPH_CONFIG_TOML, 'r', encoding='utf-8') as file:
    configs = toml.load(file)

    for k, v in configs.items():
        if isinstance(v, dict):
            for key, value in v.items():
                print(value)
