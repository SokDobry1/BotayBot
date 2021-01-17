from commands import UseDataBase as db
from commands.template import gen_buttons
from commands.listCreator import createList, listHandler
from commands.payload import get_element

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
    list_of_items = []
    for i in db.get_items(user_info):
        list_of_items += [i['name']]
    db.set_multiline_status( 3, user_info, 'delete_item;2')

    return ('Выбери предмет, который хочешь удалить:','', createList(list_of_items, end_button=['Назад', 'negative']))

#=================================================================

def get_an_answer_2(data, user_info):
    special = get_element(data, 'special')
    if special == 'назад':
        return db.go_main(user_info, 'admin_panel')

    list_of_items = []
    for i in db.get_items(user_info):
        list_of_items += [i['name']]

    handler = listHandler(data, user_info, db, list_of_items,
    'Выбери предмет, который хочешь удалить:', end_button=['Назад', 'negative'])

    if handler != False:
        return handler

    db.clear_multiline_status(user_info['vk_id'] )

    text = "Предмет не существует"
    if db.delete_item(data['body'], user_info):
        text = "Предмет удален успешно"

    return (text,'', gen_buttons('Удалить предмет', True))










