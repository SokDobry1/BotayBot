#!/home/4LcHEM1ST/.local/bin/python3

import UseDataBase as db

commands = db.get('SELECT id, script FROM commands;')
find_range = 4
print('Start...')

for id, script_name in commands:
    for j in range(1, find_range + 1):
        finder = f'_{j}'
        if finder in script_name:
            pos = script_name.find(finder)
            answer = script_name[0:pos] + script_name[pos + len(finder):]
            db.insert(f"UPDATE commands SET script = {answer!r} WHERE id = {id};")
            #print(script_name + '\nNew: ' + answer + '\n')
print('Ready')











