from commands import UseDataBase as db
from commands.readJson import readJson as readJ
from commands.listCreator import createList, createButtons
from commands.template import days, days_buttons, admin_id, gen_buttons
from commands.payload import get_element

def get_weeks(user_info):
    ans_buttons = []
    names = db.get_names_schedule(user_info)
    for i in range(len(names)):
        button_name = names[i]
        ans_buttons += [[[f'{button_name}'], ['Удалить', 'primary', {'button': button_name}]]]

    return ans_buttons + [
        [['Добавить неделю', 'primary', {'special': 'добавить неделю'}]],
        [['Назад', 'negative', {'special': 'назад'}]],
    ]

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
    elif page == 31:
        message, attachment, keyboard = get_an_answer_31(data,user_info)
    elif page == 4:
        message, attachment, keyboard = get_an_answer_4(data,user_info)
    return message, attachment, keyboard

#=================================================================

def get_an_answer_1(data, user_info):
    db.set_multiline_status( 3, user_info, 'change_schedule;2')
    return ('Что делать с неделями?','', createButtons(get_weeks(user_info)))

#=================================================================

def get_an_answer_2(data, user_info):
    button, special = get_element(data, 'button'), get_element(data, 'special')
    names_schedule = db.get_names_schedule(user_info)

    if special == 'назад':
        return db.go_main(user_info, 'admin_panel')

    if special == 'добавить неделю':
        db.set_multiline_status( 3, user_info, 'change_schedule;31')
        return ('Введи название недели', '', readJ('cancel'))

    if button in names_schedule:
        db.clear_multiline_status(user_info['vk_id'])
        db.del_week(user_info, button)
        return (f'Неделя "{button}" была успешно удалена', '', gen_buttons('Изменить расписание', True))

    if data['body'] in names_schedule:
        db.set_data_buffer(user_info['vk_id'], db.get_week_id(user_info,data['body']), '')
        db.set_multiline_status( 3, user_info, 'change_schedule;3')
        return ('Выбери день недели', '', createList(days, end_button=['Назад','negative']))

    return ('Такой недели нет','', createList(days, end_button=['Назад','negative']))

#=================================================================

def get_an_answer_3(data, user_info):
    if data['body'].lower() == 'назад':
        db.find_data_buffer(user_info['vk_id'])
        return get_an_answer_1(data, user_info)

    if data['body'] in days:
        week_id = db.find_data_buffer(user_info['vk_id'])[1]
        db.set_multiline_status( 3, user_info, 'change_schedule;4')
        db.set_data_buffer(user_info['vk_id'], week_id, data['body'])
        text = db.get_day_info(week_id, data['body'], user_info)
        if text != False:
            return ('Вот нынешнее на этот день:\n' + text + '\n\nВведи текст нового расписания:', '', readJ('cancel'))
        return ('Расписания на этот день ещё не было\nВведи текст нового расписания:', '', readJ('cancel'))

    return ('Такого дня нету','', createList(days, end_button=['Назад','negative']))

#================================================================

def get_an_answer_31(data, user_info):
    if get_element(data, 'special') == 'отмена':
        return db.go_main(user_info, 'admin_panel')

    db.clear_multiline_status(user_info['vk_id'])
    answer = db.add_week(user_info, data['body'])
    text = 'Неделя добавлена успешно'
    if answer == -1:
        text = 'Достигнут лимит количества недель'
    elif answer == -2:
        text = 'Неделя с таким названием уже существует'
    elif answer == -3:
        text = 'Слишком длинное название (максимум 40 символов)'
    return(text, '', gen_buttons('Изменить расписание', True))

#=================================================================

def get_an_answer_4(data, user_info):
    if data['body'].lower() == 'отмена':
        return db.go_main(user_info, 'admin_panel')

    db.clear_multiline_status(user_info['vk_id'])
    trash, week_id, day = db.find_data_buffer(user_info['vk_id'])
    db.update_day(user_info, week_id, day, data['body'])
    db.find_data_buffer(user_info['vk_id'])

    return ('Расписание обновлено успешно','', gen_buttons('Изменить расписание', True))












