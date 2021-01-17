import random
import sqlite3
from os.path import abspath
try:
    from vkapi import debug_message
except:
    pass

non_authotized_community = 2

def get_path():
    import os
    path = os.path.abspath(__file__)
    _pos = path.rfind("/")
    path = path[0:_pos]
    return path


def get(request):
    con = sqlite3.connect(f'{get_path()}/botay_database.sqlite')
    cur = con.cursor()
    cur.execute(request)
    result = cur.fetchall()
    con.close()
    return result


def insert(request):
    con = sqlite3.connect(f'{get_path()}/botay_database.sqlite')
    cur = con.cursor()
    cur.execute(request)
    con.commit()
    con.close()

if __name__ == "__main__":
    print(get("SELECT * FROM users;"))


#==================================COMMUNITY BLOCK==================================



def password_generator(table_name, column_name): #  <====== Генератор паролей
    key = random.randint(10**8, 10**9)
    data_list = [1]

    while len(data_list) != 0:
        key = random.randint(10**8, 10**9)
        data_list = get('SELECT id FROM {t_name} WHERE {c_name} = {key};'.format(
        t_name = table_name, c_name = column_name, key = key))

    return key

#--------------------------------------------

def name_generator(table_name, column_name): # <============ Генератор имен
    from commands import template as temp, readJson as rJ
    def rand_name(_name, _alfabet):
        for i in range(10):
            _name += _alfabet[random.randint(0, len(_alfabet) - 1)]
        return _name

    alfabet = temp.alfabet

    name = ''
    data_list = [1]

    while len(data_list) != 0:
        name = rand_name('', alfabet)
        data_list = get('SELECT id FROM {t_name} WHERE {c_name} = {key!r};'.format(
        t_name = table_name, c_name = column_name, key = name))

    return name

#------------------------------------------

#USE IN CODE
def create_community(community_name=None): #  <====== Создание группы
    if community_name == None:
        community_name = name_generator('community','name')
    guest_key = password_generator('community', 'guest_key')
    key_for_admins = password_generator('community', 'key_for_admins')

    insert(f'INSERT INTO community (name, guest_key, key_for_admins) VALUES ({community_name!r},{guest_key},{key_for_admins});')

    return (community_name, guest_key, key_for_admins)


#------------------------------------------

def check_password(password): #  <====== Проверка пароля в базе (для проверки при регистрации)
    community_info = get(f'SELECT id FROM community WHERE guest_key = {password};')
    if len(community_info) != 0:
        return (community_info[0][0], 0)
    community_info = get(f'SELECT id FROM community WHERE key_for_admins = {password};') #проверка id, паролей
    if len(community_info) != 0:
        return (community_info[0][0], 1)
    return (False, False)

#------------------------------------------

def get_community_info(community_name=False, community_id=False): #  <====== Информация о группе
    info = get('SELECT * FROM community WHERE id = 1')
    if community_name:
        info = get('SELECT * FROM community WHERE name = {name!r};'.format(name = community_name))
    if community_id:
        info =  get('SELECT * FROM community WHERE id = {id};'.format(id = community_id))
    return {'id': info[0][0], 'name': info[0][1], 'guest_key': info[0][2],'key_for_admin': info[0][3]}

#------------------------------------------

#USE IN CODE
def check_what_list(user_info):  #  <====== В зависимости от информации пользователя возвращает его статус в базе
    if user_info['isAdmin']:
        return 3
    if user_info['id_community'] == non_authotized_community:
        return 1
    return 2


#-----------------------------------------

def delete_community(id_community):
    if len(get(f"SELECT * FROM users WHERE id_community = {id_community};")) == 0:
        items = get(f"SELECT id FROM list_of_item WHERE id_community = {id_community};")
        for i in items:
            insert(f"DELETE FROM homework WHERE id_item = {i[0]};")
            insert(f"DELETE FROM list_of_item WHERE id = {i[0]};")

        weeks = get(f"SELECT id FROM week WHERE id_community = {id_community};")
        for i in weeks:
            insert(f"DELETE FROM day WHERE id_week = {i[0]};")
            insert(f"DELETE FROM week WHERE id = {i[0]};")

        insert(f"DELETE FROM teacher WHERE id_community = {id_community};")
        insert(f"DELETE FROM community WHERE id = {id_community};")

#-----------------------------------------

def change_group_name(id_community, name):
    insert(f"UPDATE community SET name = {name!r} WHERE id = {id_community};")


#==================================USER BLOCK==================================




def create_user(user_id, community_id=1):  #  <====== Создание пользователя
    insert(f'INSERT INTO users (id_community, name, isAdmin, vk_id) VALUES ({community_id}, "", 0, {user_id});')

#---------------------------------------

#USE IN CODE
def check_user(user_id):  #  <====== Проверяет есть ли пользователь в базе и создает его если что
    user_info = get('SELECT * FROM users WHERE vk_id = {user_id};'.format(user_id = user_id))
    if len(user_info) == 0:
        create_user(user_id, non_authotized_community)
        user_info = get('SELECT * FROM users WHERE vk_id = {user_id};'.format(user_id = user_id))
    user_info = {'id' : user_info[0][0], 'id_community': user_info[0][1], 'name' : user_info[0][2], 'isAdmin' : user_info[0][3], 'vk_id' : user_info[0][4]}
    return  user_info

#------------------------------------------

#USE IN CODE
def change_group(user_id, password):  #  <====== Перемещает пользователя в группу если пароль совпадает
    try:
        password = int(password)
    except:
        return False

    group_status = check_password(password)
    if group_status[0]:
        insert('UPDATE users SET id_community = {g_id} WHERE vk_id = {vk_id};'.format(
        g_id = group_status[0], vk_id = user_id))

        insert('UPDATE users SET isAdmin = {u_stat} WHERE vk_id = {vk_id};'.format(
        u_stat = group_status[1], vk_id = user_id))
        return True
    return False




#==================================COMMANDS_BLOCK==================================



def create_command(list_id, message, attachment, script, jsonFile, keywords):  #  <====== Создает комманду (используется только внутри сервера)
    insert("INSERT INTO commands (mode, message, attachment, keyboard,script,jsonFile) VALUES (4, {0!r}, {1!r}, '', {2!r}, {3!r});".format(message, attachment, script, jsonFile))
    id_command = get('select id from commands where mode = 4;')[0][0]
    for i in keywords:
        insert(f"INSERT INTO keyword (id_command, name) values ({id_command},{i!r});")
    insert(f'update commands set mode = {list_id} where mode = 4;')
    return True

#------------------------------------------

#USE IN CODE
def get_command(body, status):  #  <====== Возвращает одну подходящую комманду по статусу, иначе стандартная
    command = get(f"SELECT * FROM commands WHERE id = 11;")[0]
    keywords = get(f"SELECT id_command FROM keyword WHERE name = {body!r};")
    for i in keywords:
        id_command = i[0]
        _command = get(f"SELECT * FROM commands WHERE id = {id_command};")[0]
        if status == _command[1]:
            command = _command
            break
        if status == 3 and _command[1] == 2:
            command = _command
    command = {'id': command[0], 'mode': command[1], 'message': command[2], 'attachment': command[3], 'keyboard': command[4], 'script': command[5], 'jsonFile': command[6]}
    return command

#-----------------------------------------------

def get_doubleWord_command(body, status):
    if len(body) == 1:
        return get_command(body[0], status)

    ans = get_command(body[0] + ' ' + body[1], status)
    if ans['id'] == 11:
        ans = get_command(body[0], status)
    return ans




#==================================MULTILINE_BLOCK==================================




def set_multiline_status(list_id, user_info, name):
    vk_id = user_info['vk_id']
    from commands import template as temp
    insert(f"UPDATE users SET name = '{temp.path + 'commands/' + temp.list_of_item[list_id - 1] + '/' + str(name).split(';')[0] + '.py' + ';' + str(name).split(';')[1]}' WHERE vk_id = {vk_id};")

#----------------------------------------------------------------------

def clear_multiline_status(vk_id):
    insert(f"UPDATE users SET name = '' WHERE vk_id = {vk_id};")

#----------------------------------------------------------------------

def set_data_buffer(num_1, num_2, text):
    insert(f"INSERT INTO data_buffer (num_1, num_2, text) VALUES ({num_1}, {num_2}, {text!r});")

#----------------------------------------------------------------------

def find_data_buffer(num_1=None, num_2=None, text=None):
    info = []
    if num_1 != None:
        info = get(f"SELECT * FROM data_buffer WHERE num_1 = {num_1}")
        if len(info) != 0:
            insert(f"DELETE FROM data_buffer WHERE num_1 = {num_1}")
    if num_2 != None:
        info = get(f"SELECT * FROM data_buffer WHERE num_2 = {num_2}")
        if len(info) != 0:
            insert(f"DELETE FROM data_buffer WHERE num_2 = {num_2}")
    if text != None:
        info = get(f"SELECT * FROM data_buffer WHERE text = {text!r}")
        if len(info) != 0:
            insert(f"DELETE FROM data_buffer WHERE text = {text!r}")
    info += ((False, False, False),)
    return info[0]

#----------------------------------------------------------------------


def go_main(user_info, page='main'):
    from commands.readJson import readJson as readJ
    user_id = user_info['vk_id']
    list_id = check_what_list(user_info)

    find_data_buffer(user_id)
    clear_multiline_status(user_id)

    if page == 'admin_panel':
        answer = get(f"SELECT * FROM commands WHERE id = 18;")[0]
        return (answer[2], answer[3], readJ(answer[6]))

    if page == 'main':
        answer = []
        if list_id == 1:
            answer = get(f"SELECT * FROM commands WHERE id = 13;")[0]
            return (answer[2], answer[3], readJ(answer[6]))
        elif list_id == 2:
            from commands.authorized_user.home import main as ans
            answer = ans({}, user_info)
        else:
            from commands.authorized_admin.admin_home import main as ans
            answer = ans({}, user_info)
        return answer



#==================================LIST OF ITEMS=============================




def create_item(name, user_info):
    if len(get(f"SELECT * FROM list_of_item WHERE id_community = {user_info['id_community']} and name = {name!r};")) != 0 :
        return 1
    if len(name)>= 40 :
        return 2
    insert(f"INSERT INTO list_of_item (id_community, name) VALUES ({user_info['id_community']}, {name!r});")
    return 0

#--------------------------------------------------------------------

def delete_item(name, user_info):
    item_info = get(f"SELECT * FROM list_of_item WHERE name = {name!r} and id_community = {user_info['id_community']};")
    if len(item_info) != 0:
        insert(f"DELETE FROM homework WHERE id_item = {item_info[0][0]};")
        insert(f"DELETE FROM list_of_item WHERE id = {item_info[0][0]};")
        return True
    return False

#--------------------------------------------------------------------

def get_items(user_info):
    ans = []
    list_of_items = get(f"SELECT id, name FROM list_of_item WHERE id_community = {user_info['id_community']};")
    for i in list_of_items:
        ans += [{'id': i[0], 'name': i[1]}]
    return ans

#-----------------------------------------------------------------

def get_item_info(item_name, user_info, item_id=None):
    if item_id == None:
        item_id = get(f"SELECT * FROM list_of_item WHERE name = {item_name!r} and id_community = {user_info['id_community']};")
    else:
        item_id= get(f"SELECT * FROM list_of_item WHERE id = {item_id};")
    if len(item_id) == 0:
        item_id = ((False, False, False),)
    return {'id': item_id[0][0], 'id_community': item_id[0][1], 'name': item_id[0][2]}




#==================================HOMEWORK==================================




def check_homework(item_name, user_info):
    item_id = get_item_info(item_name, user_info)
    if item_id['id'] == False:
        return (False, False)
    item_id = item_id['id']
    if len(get(f"SELECT * FROM homework WHERE id_item = {item_id};")) == 0:
        return (True, False)
    return (True, True)

#-------------------------------------------------------------------

def add_homework(item_id, text, date):
    insert(f"INSERT INTO homework (id_item, description, date) VALUES ({item_id}, {text!r}, {date!r});")

#-------------------------------------------------------------------

def delete_homework(item_name, user_info):
    status = check_homework(item_name, user_info)
    if status[1]:
        item_id = get_item_info(item_name, user_info)['id']
        insert(f"DELETE FROM homework WHERE id_item = {item_id};")
        return True
    return False

#-------------------------------------------------------------------

def get_info_homework(item_name, user_info):
    status = check_homework(item_name, user_info)
    if status[0]:
        if status[1]:
            item_id = get_item_info(item_name, user_info)['id']
            ans = get(f"SELECT description, date FROM homework WHERE id_item = {item_id};")[0]
            temp = ans[1].split(".")
            date = f"{temp[2]}.{temp[1]}.{temp[0]}"
            return {'text': ans[0], 'date': date}
        return {'text': False, 'date': False}

    return False




#==================================SCHEDULE==================================


def get_week_id(user_info, name):
    return get(f"SELECT id FROM week WHERE id_community = {user_info['id_community']} and name = {name!r};")[0][0]

#----------------------------------------------------------------

def add_week(user_info, name):
    weeks = get(f"SELECT name FROM week WHERE id_community = {user_info['id_community']};")
    weeks_copy = []
    for i in range(len(weeks)):
        weeks_copy += weeks[i]

    if len(weeks) >= 4:
        return -1
    if name in weeks_copy:
        return -2
    if len(name)>=40:
        return -3
    insert(f"INSERT INTO week (id_community, name) VALUES ({user_info['id_community']}, {name!r});")
    return 0

#----------------------------------------------------------------

def del_week(user_info, name):
    weeks = get(f"SELECT name FROM week WHERE id_community = {user_info['id_community']};")
    weeks_copy = []
    for i in range(len(weeks)):
        weeks_copy += weeks[i]

    if not name in weeks_copy:
        return -1
    id_week = get(f"SELECT id FROM week WHERE id_community = {user_info['id_community']} and name = {name!r};")[0][0]
    insert(f"DELETE FROM day WHERE id_week = {id_week};")
    insert(f"DELETE FROM week WHERE id_community = {user_info['id_community']} and name = {name!r};")
    return 0

#----------------------------------------------------------------

def check_what_day(name_day):
    from commands.template import days
    for i in range(len(days)):
        if name_day == days[i]:
            return i + 1
    return False

#----------------------------------------------------------------

def update_day(user_info, id_week, day_name, text):
    num_day = check_what_day(day_name)
    insert(f"DELETE FROM day WHERE id_week = {id_week} and day_of_the_week = {num_day};")
    insert(f"INSERT INTO day (id_week, description, day_of_the_week) VALUES ({id_week}, {text!r}, {num_day});")

#----------------------------------------------------------------

def get_day_info(week_id, name_day, user_info):
    num_day = check_what_day(name_day)
    info = get(f"SELECT description FROM day WHERE id_week = {week_id} and day_of_the_week = {num_day};")
    if len(info) != 0:
        return info[0][0]
    return False

#-----------------------------------------------------------------

def get_names_schedule(user_info):
    ans = []
    for i in get(f"SELECT name FROM week WHERE id_community = {user_info['id_community']};"):
        ans += [i[0]]
    return ans

#==================================TEACHERS==================================




def update_teachers(id_community, text):
    insert(f"DELETE FROM teacher WHERE id_community = {id_community};")
    insert(f"INSERT INTO teacher (id_community, description) VALUES ({id_community}, {text!r});")

def get_teachers_info(id_community):
    info = get(f"SELECT description FROM teacher WHERE id_community = {id_community};")
    if len(info) != 0:
        return info[0][0]
    return False

#==================================LIST_OF_USERS==================================





#==================================MAILING==================================

def send_users(user_info, message):
    from vkapi import send_message
    users = get(f"SELECT vk_id FROM users WHERE id_community = {user_info['id_community']};")
    for i in users:
        vk_id = int(i[0])
        if vk_id != user_info['vk_id']:
            send_message(vk_id, f'Пришла рассылка от https://vk.com/id{user_info["vk_id"]} для всех:', '', '')
            send_message(vk_id, message, '', '')

#----------------------------------------------------------------

def send_admins(user_info, message):
    from vkapi import send_message
    users = get(f"SELECT vk_id FROM users WHERE id_community = {user_info['id_community']} and isAdmin = 1;")
    for i in users:
        vk_id = int(i[0])
        if vk_id != user_info['vk_id']:
            send_message(vk_id, f'Пришла рассылка от https://vk.com/id{user_info["vk_id"]} для администраторов:', '', '')
            send_message(vk_id, message, '', '')














