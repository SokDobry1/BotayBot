#!/home/4LcHEM1ST/.local/bin/python3
# -*- coding: utf-8 -*-

import UseDataBase as db #Программа для автоматического создания команд в базе данных
import os
import template as temp

os.system('clear')
l_names = ['not_authorized', 'authorized_user', 'authorized_admin']
print('-' * 30 + '\n\n1. not_authorized, 2. authorized_user, 3. authorized_admin\n')

list_name, list_num = 0, 0
while list_num not in [1, 2, 3]:
    try:
        list_num = int(input('Выбери для кого создаешь комманду: '))
    except:
        continue
list_name = l_names[list_num - 1]
print('Ok\n')



message = ""
line = input('Сообщение для вывода\n(если накосячил "1" и пиши заново):\n' )
while line:
    message += line + " \n"
    if line == '1':
        message = ""
    line = input()
print('Ok\n')

attachment = input('Attachment: ')
print('Ok\n')


template = os.path.abspath(__file__)
_pos = template.rfind("/")
if _pos == -1:
    _pos = template.rfind('\\')
template = os.path.join(template[0:_pos], list_name)
script = template + input('Имя скрипта(иначе пропусти): ') + '.py'
if script[len(template):] == '.py':
    script = ''
else:
    if not os.path.exists(script):
        with open(script, 'x') as file:
            file.write(temp.python_file)
print('Ok')



template = '/home/4LcHEM1ST/mysite/commands/jsons/'
jsonFile = template + input('Имя JSON файла(иначе пропусти): ') + '.json'
if jsonFile[len(template):] == '.json':
    jsonFile = template + 'main_buttons.json'
else:
    if not os.path.exists(jsonFile):
        with open(jsonFile, 'x') as file:
            file.write(temp.json_file)

print('Ok\n')



keywords = []
line = input('Слова-ключи, пиши с новой строки каждое\n(если накосячил "1" и пиши заново):\n ')
while line:
    keywords += [line]
    if line == '1':
        keywords = []
    line = input()


if db.create_command(list_num, message, attachment, script, jsonFile, keywords):
    print('Ready')
else:
    print('Error')











