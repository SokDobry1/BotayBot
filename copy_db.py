from commands.UseDataBase import get, insert

data_trash = get('SELECT * FROM schedule;')
data = []
for i in range(len(data_trash)):
    data += [{'id_community': data_trash[i][1], 'description': data_trash[i][2], 'day_of_the_week': data_trash[i][3], 'week': data_trash[i][4]}]

insert("DELETE FROM day;")
insert("DELETE FROM week;")

for i in data:
    if len(get(f"SELECT id FROM week WHERE id_community = {i['id_community']};")) == 0:
        insert(f"INSERT INTO week (id_community, name) VALUES ({i['id_community']}, {str(i['week']) + ' неделя'!r});")
    id_week = get(f"SELECT id FROM week WHERE id_community = {i['id_community']};")[0][0]
    insert(f"INSERT INTO day (id_week, day_of_the_week, description) VALUES ({id_week}, {i['day_of_the_week']}, {i['description']!r});")
print('Ok')









