from commands import UseDataBase as db
from commands.listCreator import createList, createButtons
from commands.template import days
from commands.payload import get_element

def get_weeks(user_info):
    ans_buttons = []
    names = db.get_names_schedule(user_info)
    for i in range(len(names)):
        button_name = names[i]
        ans_buttons += [[[f'{button_name}', 'primary']]]

    return ans_buttons + [
        [['Главная', 'positive', {'special': 'главная'}]],
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
    return message, attachment, keyboard

#=================================================================

def get_an_answer_1(data, user_info):
    weeks = db.get_names_schedule(user_info)
    if len(weeks) == 1:
        week_id = db.get_week_id(user_info, weeks[0])
        db.set_data_buffer(user_info['vk_id'], week_id, '')
        db.set_multiline_status( 2, user_info, 'schedule;3')
        return ('Выбери день недели:','', createList(days, end_button=['Назад','negative']))

    db.set_multiline_status( 2, user_info, 'schedule;2')
    return ('Выбери неделю:','', createButtons(get_weeks(user_info)))

#================================================================

def get_an_answer_2(data, user_info):
    special = get_element(data, 'special')
    names_schedule = db.get_names_schedule(user_info)

    if special == 'главная':
        return db.go_main(user_info)

    if data['body'] in names_schedule:
        week_id = db.get_week_id(user_info, data['body'])
        db.set_data_buffer(user_info['vk_id'], week_id, '')
        db.set_multiline_status( 2, user_info, 'schedule;3')
        return ('Выбери день недели:','', createList(days, end_button=['Назад','negative']))
    return('Такой недели нет', '', createButtons(get_weeks(user_info)))

#=================================================================

def get_an_answer_3(data, user_info):
    special = get_element(data, 'special')

    if special == 'назад':
        weeks = db.get_names_schedule(user_info)
        if len(weeks) == 1:
            return db.go_main(user_info)

        db.find_data_buffer(user_info['vk_id'])
        return get_an_answer_1(data, user_info)

    ans_text = 'Такого дня нет'
    if data['body'] in days:
        week_id = db.find_data_buffer(user_info['vk_id'])[1]
        text = db.get_day_info(week_id, data['body'], user_info)
        db.set_data_buffer(user_info['vk_id'], week_id, '')
        if text != False:
            ans_text = 'Вот расписание на этот день:\n' + text
        else: ans_text = 'На этот день ещё не было заполнено расписание.\nПопросите администратора вашей группы заняться этим'

    return (ans_text,'', createList(days, end_button=['Назад','negative']))











