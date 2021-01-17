from commands import UseDataBase as db
from commands.readJson import readJson as readJ

def main(data, user_info, page=1):

	name_group = db.get_community_info(community_id = user_info['id_community'])['name'];

	return (f"Группа {name_group}\nВыбирай:",'', readJ('3_main_page.json'))













