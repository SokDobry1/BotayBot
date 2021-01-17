from commands import UseDataBase as db
from commands.readJson import readJson as readJ
from commands.listCreator import createList, createButtons

def main(data, user_info, page=1):
    message = ''
    attachment = ''
    keyboard = ''
    if page == 1:
        message, attachment, keyboard = get_an_answer_1(data,user_info)
    elif page == 2:
        message, attachment, keyboard = get_an_answer_2(data,user_info)
    elif page == 31:
        message, attachment, keyboard = get_an_answer_31(data,user_info)
    elif page == 32:
        message, attachment, keyboard = get_an_answer_32(data,user_info)
    return message, attachment, keyboard

#=================================================================

def get_an_answer_1(data, user_info):
    keyboard = createButtons([
        [['Администраторам', 'primary'], ['Всем'],],
        [['Главная', 'positive'],]
    ])

    db.set_multiline_status( 3, user_info, 'auto_sender_admin;2')
    return ('Кому отправить рассылку?','', keyboard)

#=================================================================

def get_an_answer_2(data, user_info):
    body = data['body'].lower()
    if body == 'главная':
        return db.go_main(user_info)

    if body == 'администраторам':
        db.set_multiline_status(3, user_info, 'auto_sender_admin;31')

    if body == 'всем':
        db.set_multiline_status(3, user_info, 'auto_sender_admin;32')

    return ('Введи текст рассылки:','', readJ('cancel'))

#=================================================================

def get_an_answer_31(data, user_info):
    if data['body'].lower() != 'отмена':
        db.send_admins(user_info, data['body'])

    return db.go_main(user_info)

#=================================================================

def get_an_answer_32(data, user_info):
    if data['body'].lower() != 'отмена':
        db.send_users(user_info, data['body'])

    return db.go_main(user_info)











