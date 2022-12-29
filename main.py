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
instrOt = '\n'.join(['1. '+value[1] for value in record if value[3] and not value[4]])
instrOtIfWork = '\n'.join(['1. '+value[1] for value in record if value[3] and value[4]])
instrOtDriver = '\n'.join(['1. ' + value[1] for value in record if value[5] and not value[4]])
instrOtDriverIfWork = '\n'.join(['1. ' + value[1] for value in record if value[5] and value[4]])
instrOtElectromonterLulka = [value[1] for value in record if value[3]]
instrOtElectromonter = [value[1] for value in record if value[3] and (value[2] != 'Для люльки')]

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('list_instr_ot.html')
html = template.render(data=instrOtElectromonterLulka,
                       name='Перечень инструкций по охране труда для электромонтёра по ремонту аппаратуры РЗАИ с правом работы в рабочей платформе мобильной подъёмной рабочей платформы.')

with open('Перечень инструкций по ОТ.html', 'w') as file:
	file.write(html)