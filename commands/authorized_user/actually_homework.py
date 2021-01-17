from commands import UseDataBase as db
from commands.readJson import readJson as readJ
from commands.listCreator import createList, listHandler

def main(data, user_info, page=1):
    message = ''
    attachment = ''
    keyboard = ''
    if page == 1:
        message, attachment, keyboard = get_an_answer_1(data,user_info)
    elif page == 2:
        message, attachment, keyboard = get_an_answer_2(data,user_info)
    return message, attachment, keyboard

#=================================================================

def get_an_answer_1(data, user_info):
    db.find_data_buffer(user_info['vk_id'])
    db.set_multiline_status( 2, user_info, 'actually_homework;2')

    list_of_items = []
    for i in db.get_items(user_info):
        if db.check_homework(i['name'], user_info)[1]:
            list_of_items += [i['name']]

    return ('Выбери предмет по которому хочешь получить дз:','', createList(list_of_items))

#=================================================================

def get_an_answer_2(data, user_info):
    from commands.template import actually_homework_text as text_dz

    list_of_items = []
    for i in db.get_items(user_info):
        if db.check_homework(i['name'], user_info)[1]:
            list_of_items += [i['name']]

    if data['body'].lower() == 'главная':
        return db.go_main(user_info)

    if db.check_homework(data['body'], user_info)[0]:
        item = data['body']
        db.set_multiline_status( 2, user_info, 'actually_homework;2')
        info_dz = db.get_info_homework(item, user_info)

        text = None
        if info_dz['text'] != False:
            text = text_dz(info_dz['text'], info_dz['date'])
        else: text = 'По этому предмету нет дз'
        return(text, '', createList(list_of_items))

    handler = listHandler(data, user_info, db, list_of_items,
    'Выбери предмет по которому хочешь получить дз:')

    if handler != False:
        return handler

    return ('Такого предмета нет в списке','', '')











