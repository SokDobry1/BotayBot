#!/home/4LcHEM1ST/.local/bin/python3

import os

exceptions = [f'./{i}' for i in os.listdir('./')]

files_list = []
for address, dirs, files in os.walk('./'):
    for file in filter(lambda x: x.endswith('.py'), files):
        file_name = os.path.join(address, file)
        if not file_name in exceptions:
            files_list += [file_name]

find_text = r"db.set_multiline_status"
replace_text = r"(user_info, "

data = []
filesWithReplace = []

input('Ты точно хочешь это сделать?')

for i in files_list:
    do_replace = False
    with open(i,'r', encoding='utf-8') as file:
        line = file.readline()
        while line:
            if find_text in line:
                pos = line.find(find_text)
                prev = len(line[0:pos])
                start_replace = line[pos:].find('(') + prev
                end_replace = line[start_replace + 1:].find(')') + start_replace + 2

                start = line[pos:].find("'") + prev#
                end = line[start + 1:].find("'") + 2 + start #
                #line = line[0:pos] + replace_text + line[len(find_text) + pos:]
                line = line[0:pos] + find_text + replace_text + line[start:end] + ')' + line[end_replace:]
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













