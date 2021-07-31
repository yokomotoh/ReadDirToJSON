import os
import json

def read_directry(path, result):
    paths = os.listdir(path)
    for i, item in enumerate(paths):
        # print item
        sub_path = os.path.join(path, item)
        if os.path.isdir(sub_path):
            result[item] = {}
            read_directry(sub_path, result[item])
        else:
            result[item] = item
            # print(item)