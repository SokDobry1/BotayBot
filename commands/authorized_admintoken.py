from commands import UseDataBase as db
from commands.readJson import readJson as readJ
from commands.listCreator import createList

def main(data, user_info, page=1):
    message = ''
    attachment = ''
    keyboard = ''
    if page == 1:
        message, attachment, keyboard = get_an_answer_1(data,user_info)
    return message, attachment, keyboard

#=================================================================

def get_an_answer_1(data, user_info):
    return ('Ok','', '')



