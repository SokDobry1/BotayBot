#!/home/4LcHEM1ST/.local/bin/python3

import os

exceptions = [f'./{i}' for i in os.listdir('./')]

files_list = []
for address, dirs, files in os.walk('./'):
    for file in filter(lambda x: x.endswith('.py'), files):
        file_name = os.path.join(address, file)
        if not file_name in exceptions:
            files_list += [file_name]

find_text = r"db.set_multiline_status("
replace_text = r"db.set_multiline_status( "

data = []
filesWithReplace = []

input('Ты точно хочешь это сделать?')

for i in files_list:
    do_replace = False
    with open(i,'r', encoding='utf-8') as file:
        line = file.readline()
        while line:
            if find_text in line:
                num = 1
                path = i.split(r'/')[1]
                if path == 'authorized_admin':
                    num = 3
                if path == 'authorized_user':
                    num = 2
                if path == 'not_authorized':
                    num = 1

                pos = line.find(find_text)
                line = line[0:pos] + replace_text + str(num) + ', ' + line[len(find_text) + pos:]
                do_replace = True
            data += [line]
            line = file.readline()

    if do_replace:
        filesWithReplace += [str(i)]

    with open(i,'w', encoding='utf-8') as file:
        for j in data:
            file.write(j)
    data = []

for i in filesWithReplace:
    print(i)
print('OK')













