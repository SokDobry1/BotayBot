from api.user_class import users
import os
#----------------------------------------------

home_path = '/home/4LcHEM1ST/mysite/api/users/'

#----------------------------------------------

def fix_headers(data):
    headers = data['headers']
    answer = {}
    for pair in headers:
        answer.update({pair[0]: pair[1]})
    data.update({'headers': answer})

#----------------------------------------------

def login(data):
    headers = data['headers']
    if headers['User'] in users.keys():
        if headers['Password'] == users[headers['User']].password:
            return True
    return False

#==================================================

def api(data):
    fix_headers(data)
    if login(data):
        answer = {'connection_status': True}

        if 'task' in data.keys():
            from api import _list
            try:
                answer.update(
                    getattr(_list, data['task_folder'])(
                        data['task'])(data)
                        )
            except:
                answer.update(
                    {'task_status': 'None'})
        else:
            answer.update({'task_status': 'TEST REQUEST'})
        return answer

    return {'connection_status': False}

#==================================================

def upload(data):
    from werkzeug.utils import secure_filename

    def check_filename(name):
        forbidden_steps = ['../']
        forbidden_step_pos = None
        while forbidden_step_pos != -1:
            for x in forbidden_steps:
                forbidden_step_pos = name.find(x)
                if forbidden_step_pos != -1:
                    name = name[0:forbidden_step_pos] + name[forbidden_step_pos + len(x):]
        return name


    def save_file(data, _filename, _file):
        username = data['headers']['User']
        users_path = home_path + f'{username}'
        path_r_pos = _filename.rfind(r'/')
        if path_r_pos != -1:
            _dir = os.path.join(users_path, _filename[0:path_r_pos])
            if not os.path.exists(_dir):
                os.makedirs(_dir)
        file.save(os.path.join(users_path, _filename))

    fix_headers(data)
    if login(data):
        answer = {'connection_status': True}
        if data['method'] == 'POST':
            status = {}
            for filename in data['files'].keys():
                try:
                    file = data['files'][filename]
                    filename = check_filename(filename)
                    save_file(data, filename, file)
                    status.update({secure_filename(filename): 'OK'})
                except:
                    status.update({secure_filename(filename): 'ERROR'})

            answer.update({'files_status': status})
            return answer

        if data['method'] == 'GET':
            def create_files_list(username):
                _files_list = {}
                for address, dirs, files in os.walk(f'./users/{username}'):
                    for file in files:#filter(lambda x: x.endswith('.py'), files):
                        filename_sys = os.path.join(address, file)
                        filename_client = os.path.join(address[len(f'./users/{username}') + 1:], file)
                        _files_list.update({filename_client: open(filename_sys, 'rb')})
                return _files_list

            files_list = create_files_list(data['headers']['User'])
            return files_list

    return {'connection_status': False}

#==============================================================

def download(data):
    fix_headers(data)
    if login(data):
        answer = {'connection_status': True}
        username = data['headers']['User']
        if not os.path.exists(os.path.join(home_path, username, data['path_name'])):
            answer.update({'files_list': [], 'dirs_list': []})
            return answer

        if os.path.isfile(data['path_name']):
            filename = data['path_file']
            sys_name = os.path.join(home_path, username, filename)
            client_name = filename
            return {'file': {'sys': sys_name, 'client': client_name}}

        else:
            files_list, dirs_list = [], []
            scan_path = os.path.join(home_path, username)
            objects_list = os.listdir(scan_path)
            for _object in objects_list:
                if os.path.isfile(_object):
                    files_list += [_object]
                else:
                    dirs_list += [_object]

            answer.update({'files_list': files_list,
                        'dirs_list': dirs_list })
            return answer

    return {'connection_status': False}

#==============================================================

if __name__ == '__main__':
    from user_class import users
    print(users)











