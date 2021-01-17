from commands import UseDataBase as db
from commands.readJson import readJson as readJ
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
    db.set_multiline_status( 1, user_info, 'connect_community;2')
    return ('Введите токен группы:','', readJ('cancel.json'))

#=================================================================

def get_an_answer_2(data, user_info):
    if data['body'].lower() == 'отмена':
        return db.go_main(user_info)

    status = db.change_group(data['user_id'], data['body'])
    db.clear_multiline_status(data['user_id'])

    if status:
        return ("Вы успешно вошли в группу",'', '')

    return ("Неправильный токен группы",'', gen_buttons('Присоединиться'))











