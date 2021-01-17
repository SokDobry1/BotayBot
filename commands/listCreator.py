import json
from commands.payload import payload_to_str

def returnItem(text, color, dictionary={'nodata': None}):
    return '''        {
            "action": {
            "type": "text",
            "payload": "''' + payload_to_str(dictionary) + '''",
            "label": ''' + f'"{text}"' + '''
            },
            "color": ''' + f'"{color}"' + '''
        },'''

#---------------------------------------------------------------


def add_line(itemsList):
    ans = '''\n    ['''
    for item in itemsList:
        if not 'payload' in item:
            item.update({'payload': {'nodata': None}})
        ans += '\n' + returnItem(item['text'], item['color'], item['payload'])
    return ans[0:-1] + '\n    ],'

#========================================================



def createList(itemsList, page_num=1, end_button = ['Главная', 'positive']): # USE IT
    file = '''{\n   "one_time": true,\n
  "buttons": [
      '''
    back = '''
    [
        ''' + returnItem(end_button[0], end_button[1], {'special': end_button[0].lower()})[0:-1] + '''
    ]
   ]
}'''

    needNext = True
    needBack = False

    if len(itemsList) <= 6 * (page_num - 1) and page_num > 1:
        page_num -= 1

    if len(itemsList) <= 6 * page_num:
        needNext = False

    if page_num > 1: needBack = True
    while len(itemsList) < 6 * page_num:
        itemsList += ['(Пусто)']
    page_num -= 1

    for i in range(3):
        file += add_line([{'text': itemsList[i * 2 + 6 * page_num], 'color': 'secondary'}, {'text': itemsList[i * 2 + 1 + 6 * page_num], 'color': 'secondary'}])

    manage_buttons = []
    if needBack: manage_buttons += [{'text': '< < <', 'color': 'primary', 'payload': {'special': '< < <'}}]
    if needNext: manage_buttons += [{'text': '> > >', 'color': 'primary', 'payload': {'special': '> > >'}}]

    if len(manage_buttons) != 0:
        file += add_line(manage_buttons)

    return file + back


#========================================================



def createButtons(itemsList): # FORMAT: [
                              #          [[text, color, payload], [text, color], [text],],
                              #         ]

    file = '''{\n   "one_time": true,\n
  "buttons": [
      '''
    back = '''
   ]
}'''

    for itemsLine in itemsList:
        line = []
        for item in itemsLine: # '' = 'secondary'
            if len(item) == 1:
                item += ['secondary']
            if len(item) == 2:
                item += [{'data': None}]
            line += [{'text': item[0], 'color': item[1], 'payload': item[2]}]
        file += add_line(line)

    return json.dumps(json.loads(file[0:-1] + back))


#========================================================


def listHandler(data, user_info, db, list_of_items, text, end_button=['Главная', 'positive']):
    from commands.payload import payload_to_dict
    special = None
    if 'special' in payload_to_dict(data):
        special = payload_to_dict(data)['special']

    page = db.find_data_buffer(user_info['vk_id'])[1]
    if not page:
        page = 1

    if special == '> > >':
        if len(list_of_items) > 6 * page:
            page += 1
        db.set_data_buffer(user_info['vk_id'], page, '')
        return (text,'', createList(list_of_items, page, end_button))

    if special == '< < <':
        if page > 1:
            page -= 1
        db.set_data_buffer(user_info['vk_id'], page, '')
        return (text,'', createList(list_of_items, page, end_button))

    return False
















