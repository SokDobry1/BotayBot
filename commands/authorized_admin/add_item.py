from commands import UseDataBase as db
from commands.readJson import readJson as readJ
from commands.payload import get_element
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
    text = '''Введи название предмета:
    (Подсказка: Ограничение на названия = 40 символов.
    Сокращайте названия. Например: "Программирование в алгоритмах" можно сократить в "Прогр-ие в алг."'''

    db.set_multiline_status( 3, user_info, 'add_item;2')
    return (text,'', readJ('cancel.json'))
#=================================================================

def get_an_answer_2(data, user_info):
    special = get_element(data, 'special')
    if special == 'отмена':
        return db.go_main(user_info, 'admin_panel')

    db.clear_multiline_status(user_info['vk_id'] )

    case = db.create_item(data['body'], user_info)

    if case == 0:
        text = "Предмет добавлен успешно"
    elif case==1:
        text = "Это имя занято"
    elif case==2:
        text = "Слишком длинное название (максимум 40 символов)"

    return (text,'', gen_buttons('Добавить предмет', True))









