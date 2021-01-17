#!/home/4LcHEM1ST/.local/bin/python3

import os

def get_path():
    path = os.path.abspath(__file__)
    for i in range(2):
        _pos = path.rfind("/")
        path = path[0:_pos]
    return path

exceptions = ['./backup.txt', './commands/botay_database.sqlite']

main_path = get_path()
files_list = []
for address, dirs, files in os.walk(main_path):
    for file in filter(lambda x: x.endswith('.py') or x.endswith('.json'), files):
        file_name = os.path.join(address, file)
        if not file_name in exceptions:
            files_list += [file_name]

status = 0

with open(f'{main_path}/backup/backup.txt','w', encoding='utf-8') as backup:
    backup.write(f"{len(files_list)}\n\n")
    for x in range(len(files_list)):
        i = files_list[x]
        with open(i, 'r', encoding='utf-8') as file:
            backup.write(i + '\n\n' + '-' * 30 + '\n\n' + file.read() + '\n\n' + '#' * 30 + '\n\n')

        status_now = int(x / (len(files_list) - 1) * 10)
        if status_now != status:
            status = status_now
            print(str(status * 10) + '%')
    backup.write('1234567890end')

print('OK')













