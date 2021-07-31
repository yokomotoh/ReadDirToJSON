import json

from read_directry import read_directry

fpath = '/Users/vincent/Desktop/'
filename =  '/Users/vincent/PycharmProjects/ReadDirToJSON/json_res.txt'
result = {}
read_directry(fpath, result)
json_res = json.dumps(result, indent=2)
print(json_res)
with open(filename, 'w') as fp:
    fp.write(json_res)
