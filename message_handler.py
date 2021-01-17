import vkapi
import importlib
from commands import UseDataBase as db, template as temp
from commands.readJson import readJson as readJ
from commands.template import admin_id

pls_wait = False

def get_importer_line(path):
    importer = path[len(temp.path):].split(r'/')
    line = ''
    for i in importer:
        line += i + '.'
    return line



def get_answer(body, data, user_info):
    if user_info['vk_id'] in admin_id:
        if 'attachments' in data:
            att = data['attachments']
            ans = ''
            for i in att:
                ans += f"{i['type']}{i['photo']['owner_id']}_{i['photo']['id']}_{i['photo']['access_key']},"
            return(str(ans), ans[0:-1], '')

    if pls_wait and not user_info['vk_id'] in admin_id:
        return ('Бот отошел немного отдохнуть, возвращайтесь позже', '', readJ('main_buttons'))

    if data['body'].lower() == '!помоги':
        return db.go_main(user_info)

    message, keyboard, attachment = '', '', ''
    list_id = db.check_what_list(user_info)

    command_info = db.get_doubleWord_command(body.lower().split(' '), list_id)
    keyboard = readJ(command_info['jsonFile'])
    script_path = ''
    page = 1

    if user_info['name']: script_path, page = user_info['name'].split(';')
    elif command_info['script']: script_path = command_info['script']
    else: message, attachment = command_info['message'], command_info['attachment']

    if script_path: # Обработка скриптов
        line = get_importer_line(script_path)
        message, attachment, _keyboard= importlib.import_module(line[0:-4]).main(data, user_info, int(page))
        if _keyboard != '': keyboard = _keyboard
        else: keyboard = readJ('main_buttons.json')

    message = message.replace("!E!", "\n")
    return message, attachment, keyboard


def create_answer(data):
   user_id = data['user_id']
   user_info = db.check_user(user_id)

   data['body'] = data['body'].replace("\n", "!E!")

   message, attachment, keyboard = '', '', ''

   if user_id in admin_id:
       message, attachment, keyboard = get_answer(data['body'], data, user_info)
   else:
      try:
         message, attachment, keyboard = get_answer(data['body'], data, user_info)
      except:
         for i in admin_id:
            vkapi.send_message(i, f'У пользователя https://vk.com/gim194144255?sel={user_id} ошибка!\nБегом исправлять!\nВот его id: {user_id}', attachment, keyboard)
         message, attachment, keyboard = 'Произошла ошибка.\nЯ отправил в тех. поддержку уведомление.\nПопробуй ещё раз, если ничего не произошло - мы все исправим через некоторое время', '', readJ('main_buttons')

   vkapi.send_message(user_id, message, attachment, keyboard)













