import json

with open('../data/json_files/VideoCodec2024-09-04 16:05:47.237098.json', 'r') as data:
    iter_data = json.load(data)

    for key, value in iter_data["diagram"]["mxGraphModel"]["root"].items():
        print(value)

