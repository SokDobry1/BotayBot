from commands import UseDataBase as db

def main(data, user_info, page=1):
    text = db.get_teachers_info(user_info['id_community'])
    if text != False:
        return ('Вот ваши преподаватели:\n' + text,'', '')
    return ('Список преподавателей ещё не был заполнен.\nПопросите администратора вашей группы заняться этим','', '')











