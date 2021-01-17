#!/home/4LcHEM1ST/.local/bin/python3

import os

def get_path():
    path = os.path.abspath(__file__)
    for i in range(2):
        _pos = path.rfind("/")
        path = path[0:_pos]
    return path

main_path = get_path()
exceptions = ['./backup.txt']
read_only = [] #['/commands/authorized_admin/add_homework.py']

num, status = 0, 0

if len(read_only) > 0:
    exceptions = []

with open(f'{main_path}/backup/backup.txt', 'r', encoding='utf-8') as backup:
    files_count = int(backup.readline().strip()) - 1
    backup.readline()
    file_name = backup.readline().strip()
    while file_name != '1234567890end':
        method = 'w'
        if not os.path.exists(file_name):
            dir = file_name[0:file_name.rfind(r'/')]
            if not os.path.exists(dir):
                os.mkdir(dir)
            method = 'x'

        for i in range(3):
            backup.readline()

        text = ''
        line = backup.readline()
        while line.strip() != '#' * 30:
            text += line
            line = backup.readline()

        if not file_name in exceptions:
            if len(read_only) == 0 or file_name in read_only:
                with open(file_name, method, encoding='utf-8') as file:
                    file.write(text)

        backup.readline()
        file_name = backup.readline().strip()

        num += 1
        status_now = int(num / files_count * 10)
        if status_now != status:
            status = status_now
            print(str(status * 10) + '%')

print('OK')










