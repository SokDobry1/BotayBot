from commands import UseDataBase as db
from commands.readJson import readJson as readJ

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
	add = ''
	db.set_multiline_status( 3, user_info, 'update_teachers;2')
	text = db.get_teachers_info(user_info['id_community'])
	if text != False:
		add += 'Нынешний текст:\n' + text + '\n\n'

	return (add + 'Введи текст, который будет появляться после нажатия кнопки "преподаватели":','', readJ('cancel'))
#=================================================================

def get_an_answer_2(data, user_info):
	if data['body'].lower() == 'отмена':
		return db.go_main(user_info, 'admin_panel')

	db.update_teachers(user_info['id_community'], data['body'])
	db.clear_multiline_status(user_info['vk_id'])
	return ('Текст обновлен успешно','', readJ('admin-main'))











