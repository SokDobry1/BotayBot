from commands import UseDataBase as db
from commands.readJson import readJson as readJ
from commands import template as temp
from commands.payload import get_element

def main(data, user_info, page=1):
    message = ''
    attachment = ''
    keyboard = ''
    if page == 1:
        message, attachment, keyboard = get_an_answer_1(data,user_info)
    elif page == 2:
        message, attachment, keyboard = get_an_answer_2(data,user_info)
    return (message, attachment, keyboard)


def get_an_answer_1(data, user_info):
    db.set_multiline_status( 1, user_info, 'create_community;2')
    return ("Введите название группы", '', readJ("cancel"))

def get_an_answer_2(data, user_info):
    special = get_element(data, 'special')
    db.clear_multiline_status(user_info['vk_id'] )
    if special == "отмена":
        db.go_main(user_info)

    if (len(data['body']) > 40): data['body'] = data['body'][0:41]
    community_name, guest_key, admin_key = db.create_community(data['body'])
    db.change_group(user_info['vk_id'], admin_key)

    return (temp.create_community_printer(community_name, guest_key, admin_key),'', '')













