import os

JSON_DIRECTORY = '/home/landotech/Documents/GitHub/drawmate.me/data/json_files/'


def export_json_templates():
    directory = JSON_DIRECTORY
    with os.scandir(directory) as entries:
        file_paths = [entry.path for entry in entries if entry.is_file()]

    return file_paths


for i in export_json_templates():
    print(i)

