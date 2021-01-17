from commands import UseDataBase as db
from commands.readJson import readJson as readJ
from commands.listCreator import createList, listHandler
from commands.template import gen_buttons, admin_id
from commands.payload import get_element

def main(data, user_info, page=1):
    message = ''
    attachment = ''
    keyboard = ''

    if page == 1:
        message, attachment, keyboard = get_an_answer_1(data,user_info)
    elif page == 2:
        message, attachment, keyboard = get_an_answer_2(data,user_info)
    elif page == 3:
        message, attachment, keyboard = get_an_answer_3(data,user_info)
    elif page == 4:
        message, attachment, keyboard = get_an_answer_4(data,user_info)
    elif page == 5:
        message, attachment, keyboard = get_an_answer_5(data,user_info)
    return message, attachment, keyboard

#=================================================================

def get_an_answer_1(data, user_info):
    db.find_data_buffer(user_info['vk_id'])
    db.set_multiline_status( 3, user_info, 'add_homework;2')

    list_of_items = []
    for i in db.get_items(user_info):
        list_of_items += [i['name']]

    return ('Выбери предмет по которому хочешь добавить дз:','', createList(list_of_items, end_button=['Назад', 'negative']))

#=================================================================

def get_an_answer_2(data, user_info):
    special = get_element(data, 'special')
    if special == 'назад':
        return db.go_main(user_info, 'admin_panel')

    list_of_items = []
    for i in db.get_items(user_info):
        list_of_items += [i['name']]

    if data['body'] in list_of_items:
        db.set_multiline_status( 3, user_info, 'add_homework;3')
        db.find_data_buffer(user_info['vk_id'])
        db.set_data_buffer(user_info['vk_id'], 0, data['body'])
        if not db.check_homework(i['name'], user_info)[1]:
            return('Введи текст домашнего задания:', '', readJ('cancel'))
        else:
            return("По этому предмету есть дз.\nУдалить?",'', readJ('yes_no'))

    handler = listHandler(data, user_info, db, list_of_items,
    'Выбери предмет по которому хочешь добавить дз:', end_button=['Назад', 'negative'])

    if handler != False:
        return handler

    db.clear_multiline_status(user_info['vk_id'])
    return ('Такого предмета нет в списке','', gen_buttons('Добавить дз', True))

#=================================================================

def get_an_answer_3(data, user_info):
    special = get_element(data, 'special')
    if special == "нет":
        return get_an_answer_1(data, user_info)
    if special == "да":
        item = db.find_data_buffer(user_info["vk_id"])[2]
        data["body"] = item
        db.delete_homework(item, user_info)
        return get_an_answer_2(data, user_info)

    if special == 'отмена':
        return get_an_answer_1(data, user_info)

    item = db.find_data_buffer(user_info['vk_id'])[2]
    db.set_data_buffer(user_info['vk_id'], db.get_item_info(item, user_info)['id'], data['body'])

    db.set_multiline_status( 3, user_info, 'add_homework;4')
    return ('''Введи дату, когда дз будет актуально, в формате [День].[Месяц].[Год]
    (На следующий день в 3:00 по МСК дз будет удалено)''','', readJ('cancel.json'))

#=================================================================

def get_an_answer_4(data, user_info):
    import datetime
    special = get_element(data, 'special')
    if special == 'отмена':
        return db.go_main(user_info, 'admin_panel')

    day = []
    go_back = False

    try:
        day = data['body'].split('.')
        now_day = datetime.datetime.today().strftime("%d.%m.%Y").split('.')

        if len(day) != 3:
            f = int('for_except')

        for i in range(3):
            day[i] = int(day[i])
            now_day[i] = int(now_day[i])

        if day[0] <= now_day[0]:
            if day[1] <= now_day[1]:
                if day[2] <= now_day[2]:
                    f = int('for_except')

        if day[1] < now_day[1]:
            if day[2] <= now_day[2]:
                f = int('for_except')

        if day[2] < now_day[2]:
            f = int('for_except')

        datetime.date(day[2], day[1], day[0])
    except:
        go_back = True

    if go_back:
        db.set_multiline_status( 3, user_info, 'add_homework;4')
        return('''Неверная дата. Введите дату на  в формате [День].[Месяц].[Год]
    (На следующий день в 3:00 по МСК дз будет удалено))''', '',  readJ('cancel'))

    else:
        vk_id, id_item, text_dz = db.find_data_buffer(user_info['vk_id'])

        if vk_id == False:
            db.clear_multiline_status(user_info['vk_id'])
            return ('Ошибка, повторите запрос','', gen_buttons('Добавить дз', True))

        db.set_multiline_status( 3, user_info, 'add_homework;5')
        db.add_homework(id_item, text_dz, f"{day[2]}.{day[1]}.{day[0]}")
        item_name = db.get_item_info('', user_info, id_item)['name']
        db.set_data_buffer(user_info['vk_id'], 0, item_name)
        return ('Дз было добавлено успешно\nОповестить участников группы?','', readJ('yes_no'))

#=======================================================================

def get_an_answer_5(data, user_info):
    special = get_element(data, 'special')
    item_name = db.find_data_buffer(user_info['vk_id'])[2]
    if special == 'да':
        db.send_users(user_info, f'Добавлено домашнее задание по предмету "{item_name}"')

    db.clear_multiline_status(user_info['vk_id'])
    return('Готово', '', gen_buttons('Добавить дз', True))























