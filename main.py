import sqlite3
from pathlib import Path


from jinja2 import Environment, FileSystemLoader


p = Path('.') / 'out'
try:
    sqlite_connection = sqlite3.connect('workers.db')
    cursor = sqlite_connection.cursor()

    sqlite_select_query = "select * from documents;"
    cursor.execute(sqlite_select_query)
    record = cursor.fetchall()
    cursor.close()
except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (sqlite_connection):
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")

doc = {value[2]: value[1] for value in record}
instrOt = [value[1] for value in record if value[3] or value[5]]
instrOtElectromonterLulka = [value[1] for value in record if value[3]]
instrOtElectromonter = [value[1] for value in record if value[3] and (value[2] != 'Для люльки')]
p1 = [value[1] for value in record if value[3] and (value[2] != 'Для люльки')]
env = Environment(loader=FileSystemLoader('templates'))

menu = [['list_instr_ot.html',
         'Перечень инструкций по охране труда для электромонтёра по ремонту аппаратуры РЗАИ с правом работы в рабочей платформе мобильной подъёмной рабочей платформы.',
         'Перечень инструкций по ОТ для электромонтёра с люлькой.html',
         instrOtElectromonterLulka],
        ['list_instr_ot.html',
         'Перечень инструкций по охране труда для электромонтёра по ремонту аппаратуры РЗАИ.',
         'Перечень инструкций по ОТ для электромонтёра без люльки.html',
         instrOtElectromonter],
        ['list_instr_ot.html',
         'Перечень инструкций по охране труда по службе РЗАИ.',
         'Перечень инструкций по охране труда по службе РЗАИ.html',
         instrOt],
        ['progr_pervich_instrukt.html',
         'Программа первичного инструктажа на рабочем месте для мастера (старшего мастера) СРЗАИ.',
         'Программа первичного инструктажа на рабочем месте для мастера (старшего мастера) СРЗАИ.html',
         doc],
        ['progr_pervich_instrukt_kladov.html',
         'Программа первичного инструктажа на рабочем месте для старшего мастера СРЗАИ с совмещением профессии кладовщика.',
         'Программа первичного инструктажа на рабочем месте для старшего мастера СРЗАИ с совмещением профессии кладовщика.html',
         doc],
        ['progr_pervich_instrukt_tehnik.html',
         'Программа первичного инструктажа на рабочем месте для техника СРЗАИ.',
         'Программа первичного инструктажа на рабочем месте для техника СРЗАИ.html',
         doc],
        ['progr_pervich_instrukt_zam_nach.html',
         'Программа первичного инструктажа на рабочем месте для заместителя начальника СРЗАИ.',
         'Программа первичного инструктажа на рабочем месте для заместителя начальника СРЗАИ.html',
         doc],
        ['progr_pervich_instrukt_ingener.html',
         'Программа первичного инструктажа на рабочем месте для инженера СРЗАИ.',
         'Программа первичного инструктажа на рабочем месте для инженера СРЗАИ.html',
         doc],
        ['progr_pervich_instrukt_tehnik_metrolog.html',
         'Программа первичного инструктажа на рабочем месте для техника (по метрологии) СРЗАИ.',
         'Программа первичного инструктажа на рабочем месте для техника (по метрологии) СРЗАИ.html',
         doc],
        ]
prompt = [str(i)+' '+s[1] for i,s in enumerate(menu)]
sel = int(input('\n'.join(prompt)+'\n>'))
template = env.get_template(menu[sel][0])
html = template.render(data=menu[sel][3],
                       name=menu[sel][1])

with open(p / menu[sel][2], 'w') as file:
	file.write(html)
