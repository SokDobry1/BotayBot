class User:
    def __init__(self,
                password, vk_id,
                forbidden_tasks, allowed_files):
        self.password = password
        self.vk_id = vk_id
        self.allowed_files = allowed_files

    def fix_allowed_files(self):
        import os
        files_list = []
        if len(self.allowed_files) != 0:
            if self.allowed_files[0] == '*':
                for address, dirs, files in os.walk('/home/4LcHEM1ST/mysite'):
                    for file in files:
                        file_name = os.path.join(address, file)
                        files_list += [file_name]
                self.allowed_files = files_list
            else:
                self.allowed_files = files_list + allowed_files

    def task_permission(self, task_folder, task_name):
        for i in foribidden_tasks:
            pair = {'task_folder': i.split('/')[0],
                    'task_name': i.split('/')[1]}
            if task_folder == pair['task_folder'] and task_name == pair['task_name']:
                return False
        return True

users = {
    'alf': User('1234',
            228179762,
            [], ['*'],
                ),
    'victor': User('001234',
            195823782,
            [], ['*'],
                ),
    }












