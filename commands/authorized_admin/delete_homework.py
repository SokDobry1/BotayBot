from commands import UseDataBase as db
from commands.listCreator import createList, listHandler
from commands.template import gen_buttons

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
    db.set_multiline_status( 3, user_info, 'delete_homework;2')

    list_of_items = []
    for i in db.get_items(user_info):
        if db.check_homework(i['name'], user_info)[1]:
            list_of_items += [i['name']]

    return ('Выбери предмет по которому хочешь удалить дз:','', createList(list_of_items, end_button=['Назад', 'negative']))
#=================================================================

def get_an_answer_2(data, user_info):
    list_of_items = []
    for i in db.get_items(user_info):
        if db.check_homework(i['name'], user_info)[1]:
            list_of_items += [i['name']]

    if data['body'].lower() == 'назад':
        return db.go_main(user_info, 'admin_panel')

    if data['body'] in list_of_items:
        item = data['body']
        db.clear_multiline_status(user_info['vk_id'])
        if db.delete_homework(item, user_info):
            return ('Дз было успешно удалено','', gen_buttons('Удалить дз', True))
        return ('По этому предмету не было дз','', gen_buttons('Удалить дз', True))

    handler = listHandler(data, user_info, db, list_of_items,
    'Выбери предмет по которому хочешь удалить дз:', end_button=['Назад', 'negative'])

    if handler != False:
        return handler

    db.clear_multiline_status(user_info['vk_id'])
    return ('Такого предмета нет в списке','', gen_buttons('Удалить дз', True))













