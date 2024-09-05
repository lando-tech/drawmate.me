import json

with open('../data/json_files/VideoCodec2024-09-04 16:05:47.237098.json', 'r') as data:
    iter_data = json.load(data)

    for key, value in iter_data["diagram"]["mxGraphModel"]["root"].items():
        print(value)



def update_json(json_file_path):
    """Update JSON data based on the provided updates."""
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Apply updates to the data
    # for key, value in updates.items():
        # Implement more complex logic as needed for nested updates
        # if isinstance(value, dict):
        # data[key].update(value)
        # else:
        # data[key] = value

    # Write the updated JSON back to the file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


# Example updates: adjust according to JSON structure
updates = {
    'mxCell': [
        {'id': 'new_id', 'value': 'new_value'}
    ]
}

# update_json(json_file_path)