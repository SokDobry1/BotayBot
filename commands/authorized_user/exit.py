from commands import UseDataBase as db
from commands.readJson import readJson as readJ

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
    db.set_multiline_status( 2, user_info, 'exit;2')
    text = ''
    if len(db.get(f"SELECT * FROM users WHERE id_community = {user_info['id_community']};")) == 1:
        text = '\nВ группе больше нет людей, она будет удалена'
    return ('Ты уверен(а)?' + text,'', readJ('yes_no'))

#=================================================================

def get_an_answer_2(data, user_info):
    if data['body'].lower() != 'да':
        return db.go_main(user_info)

    id_community = user_info['id_community']

    db.clear_multiline_status(data['user_id'])
    db.change_group(data['user_id'], 12344325)

    db.delete_community(id_community)

    return ('Вы успешно вышли из группы','', readJ('main_buttons'))











