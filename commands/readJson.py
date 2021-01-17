import json
from os.path import abspath

def get_path():
    import os
    path = os.path.abspath(__file__)
    _pos = path.rfind("/")
    path = path[0:_pos]
    return path

def readJson(name):
    if name[0:len('/home')] != '/home':
        if name[-5:] == '.json': name = name[0:-5]
        name = f"{get_path()}/jsons/{name}.json"
    with open(name) as f:
        return json.dumps(json.load(f))

def readJsonText(text):
    return json.dumps(json.loads(text))












