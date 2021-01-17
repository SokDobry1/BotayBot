from commands import UseDataBase as db
from vkapi import send_message
from commands.readJson import readJson as readJ

def main(data, user_info, page=1):
    message = ''
    attachment = ''
    keyboard = ''

    if page == 1:
        message, attachment, keyboard = get_an_answer_1(data,user_info)
    return message, attachment, keyboard

def get_an_answer_1(data,user_info):
    info = db.get_community_info(community_id=user_info["id_community"])
    send_message(user_info["vk_id"], 
                 f"Токен администратора:\n{info['key_for_admin']}", '', '')
                 
    send_message(user_info["vk_id"], 
                 f"Токен пользователя:\n{info['guest_key']}", '', readJ("3_admin_panel"))

    return("", "", "")







