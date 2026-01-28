import os
import json5


def list_json5_files(root_dir):
    json5_files = []
    for root, _, files in os.walk(root_dir):
        for f in files:
            if f.endswith(".json5"):
                json5_files.append(os.path.join(root, f))
    return json5_files


def read_json5(path):
    with open(path, "r", encoding="utf-8") as f:
        return json5.load(f)


def write_json5(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json5.dump(data, f, indent=2)
