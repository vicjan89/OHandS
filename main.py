import sqlite3


from jinja2 import Environment, FileSystemLoader


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
# template = env.get_template('list_instr_ot.html')
# html = template.render(data=instrOtElectromonterLulka,
#                        name='Перечень инструкций по охране труда для электромонтёра по ремонту аппаратуры РЗАИ с правом работы в рабочей платформе мобильной подъёмной рабочей платформы.')
#
# with open('Перечень инструкций по ОТ для электромонтёра с люлькой.html', 'w') as file:
# 	file.write(html)
#
# html = template.render(data=instrOtElectromonter,
#                        name='Перечень инструкций по охране труда для электромонтёра по ремонту аппаратуры РЗАИ.')
#
# with open('Перечень инструкций по ОТ для электромонтёра без люльки.html', 'w') as file:
# 	file.write(html)
#
# html = template.render(data=instrOt,
#                        name='Перечень инструкций по охране труда по службе РЗАИ.')
#
# with open('Перечень инструкций по охране труда по службе РЗАИ.html', 'w') as file:
# 	file.write(html)
# template = env.get_template('progr_pervich_instrukt.html')
# html = template.render(data=doc,
#                        name='Программа первичного инструктажа на рабочем месте для мастера (старшего мастера) СРЗАИ.')
#
# with open('out\Программа первичного инструктажа на рабочем месте для мастера (старшего мастера) СРЗАИ.html', 'w') as file:
# 	file.write(html)
#
# template = env.get_template('progr_pervich_instrukt_kladov.html')
# html = template.render(data=doc,
#                        name='Программа первичного инструктажа на рабочем месте для старшего мастера СРЗАИ с совмещением профессии кладовщика.')
#
# with open('out\Программа первичного инструктажа на рабочем месте для старшего мастера СРЗАИ с совмещением профессии кладовщика.html', 'w') as file:
# 	file.write(html)
#
# template = env.get_template('progr_pervich_instrukt_tehnik.html')
# html = template.render(data=doc,
#                        name='Программа первичного инструктажа на рабочем месте для техника СРЗАИ.')
#
# with open('out\Программа первичного инструктажа на рабочем месте для техника СРЗАИ.html', 'w') as file:
# 	file.write(html)

# template = env.get_template('progr_pervich_instrukt_zam_nach.html')
# html = template.render(data=doc,
#                        name='Программа первичного инструктажа на рабочем месте для заместителя начальника СРЗАИ.')
#
# with open('out\Программа первичного инструктажа на рабочем месте для заместителя начальника СРЗАИ.html', 'w') as file:
# 	file.write(html)
#
# template = env.get_template('progr_pervich_instrukt_ingener.html')
# html = template.render(data=doc,
#                        name='Программа первичного инструктажа на рабочем месте для инженера СРЗАИ.')
#
# with open('out\Программа первичного инструктажа на рабочем месте для инженера СРЗАИ.html', 'w') as file:
# 	file.write(html)

template = env.get_template('progr_pervich_instrukt_tehnik_metrolog.html')
html = template.render(data=doc,
                       name='Программа первичного инструктажа на рабочем месте для техника (по метрологии) СРЗАИ.')

with open('out\Программа первичного инструктажа на рабочем месте для техника (по метрологии) СРЗАИ.html', 'w') as file:
	file.write(html)