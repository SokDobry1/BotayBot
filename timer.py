import datetime
from time import sleep
from commands import UseDataBase as db

hours_now = int(datetime.datetime.today().strftime("%H"))
minutes_now = int(datetime.datetime.today().strftime("%M"))
seconds_now = int(datetime.datetime.today().strftime("%S"))

day_now = int(datetime.datetime.today().strftime("%d"))
mounth_now = int(datetime.datetime.today().strftime("%m"))
year_now = int(datetime.datetime.today().strftime("%Y"))

def main(day_now, mounth_now, year_now):
    from vkapi import debug_message
    debug_message("OK")
    print(day_now)
    db.insert(f"DELETE FROM homework WHERE date < '{year_now}-{mounth_now}-{day_now}';")

main(day_now, mounth_now, year_now)

delta = 24 * 60 * 60 - (hours_now * 60 * 60 + minutes_now * 60 + seconds_now)
print(f'Засыпаю, проснусь через {delta // 60 // 60}:{delta // 60 % 60}:{delta % 60 % 60}')
sleep(delta)

while True:
    day_now = int(datetime.datetime.today().strftime("%d"))
    mounth_now = int(datetime.datetime.today().strftime("%m"))
    year_now = int(datetime.datetime.today().strftime("%Y"))
    main(day_now, mounth_now, year_now)
    print('Работа сделана, засыпаю...')
    sleep(24 * 60 * 60)











