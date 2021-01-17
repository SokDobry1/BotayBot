'''Содержит в себе кучу грамоздкого хлама,
который необходим файлам'''

import os

#CommandsCreator.py
python_file = """from commands import UseDataBase as db
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
    return ('Ok','', '')"""

json_file = '''{
  "one_time": true,
  "buttons": [
    [
      {
        "action": {
          "type": "text",
          "label": "Главная"
        },
        "color": "positive"
      }
    ]
  ]
}'''

#UseDataBase.py
alfabet = []
for i in [[48,58],[65,91],[97,123]]:
    for j in range(i[0],i[1]):
        alfabet += [chr(j)]

#/not_authorized/create_community.py
def create_community_printer(name, user_pass, admin_pass):
    return f"""Группа под названием {name} создана успешно.
    Пароль user: {user_pass}
    Пароль admin: {admin_pass}"""

path = '/home/4LcHEM1ST/mysite/'
list_of_item = ['not_authorized','authorized_user','authorized_admin', 'not_ok_command']

#actually_homework_2.py
def actually_homework_text(text, date):
    return f"Вот текст домашнего задания:\n{text}\nНа день: {date}"

#schedule
days = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота']

days_buttons = [
    [['Изменить название недели', 'primary', {'special': 'Изменить название недели'}]],
    [['Понедельник'],['Вторник']],
    [['Среда'],['Четверг']],
    [['Пятница'],['Суббота']],
    [['Назад', 'negative', {'special': 'Назад'}]],
    ]

#buttons
def gen_buttons(name, admin_panel=False):
    from commands.readJson import readJsonText as readJT
    if not admin_panel:
        texter = '''{
  "one_time": true,
  "buttons": [
    [
      {
        "action": {
          "type": "text",
          "label": "''' + f'{name}' + '''"
        },
        "color": "secondary"
      },
      {
        "action": {
          "type": "text",
          "label": "Главная"
        },
        "color": "positive"
      }
    ]
  ]
}'''
    else:
        texter = '''{
  "one_time": true,
  "buttons": [
    [
        {
        "action": {
          "type": "text",
          "label": "Панель администратора"
        },
        "color": "primary"
      }
    ],
    [
      {
        "action": {
          "type": "text",
          "label": "''' + f'{name}' + '''"
        },
        "color": "secondary"
      },
      {
        "action": {
          "type": "text",
          "label": "Главная"
        },
        "color": "positive"
      }
    ]
  ]
}'''

    return readJT(texter)

#message_handler
admin_id = [228179762, 195823782]
helpers = []

if __name__ == "__main__":
    print('No errors')

















