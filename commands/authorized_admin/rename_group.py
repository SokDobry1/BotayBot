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
	db.find_data_buffer(user_info['vk_id'])
	db.set_multiline_status( 3, user_info, 'rename_group;2')

	return ('Введите название группы:','', readJ('cancel.json'))
#=================================================================

def get_an_answer_2(data, user_info):
	db.clear_multiline_status(user_info['vk_id'])

	if data['body'].lower() == 'отмена':
		return db.go_main(user_info, 'admin_panel')

	db.change_group_name(user_info['id_community'], data['body']);

	return ('Название изменено успешно','', readJ('admin-main'))












