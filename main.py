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
    cursor.execute('''SELECT names.name, Должность, names.'Группа по ЭБ', names.'Дата проверки знаний', 
GROUP_CONCAT(CASE
                WHEN rights.'По электробезопасности' THEN rights.right
                END, ', ') as rights_sel1,
GROUP_CONCAT(CASE
                WHEN rights.'Зона' THEN rights.right
                END, ', ') as rights_sel2,
GROUP_CONCAT(CASE
WHEN rights.'На выполнение специальных работ' THEN rights.right
END, ', ') as rights_spec,
names.'Номера билетов'
FROM names 
LEFT JOIN connections ON connections.name=names.nameID
LEFT JOIN rights ON connections.right=rights.rightID
WHERE names.nameID=34 OR names.nameID=32
GROUP BY names.name
''')
    knowledge_check = cursor.fetchall()
    cursor.execute('SELECT rights.right, rights.rightID FROM rights')
    rights = cursor.fetchall()
    cursor.execute('SELECT names.name, names.nameID FROM names')
    names = cursor.fetchall()
    cursor.execute('SELECT connections.name, connections.right FROM connections')
    connections = cursor.fetchall()
    cursor.close()
    rights_names = ['Ф.И.О']
    rights_names.extend([(i[0]+'('+str(i[1])+')') for i in rights])
    rights_rows = []
    rights_rows.append(rights_names)
    for n in names:
        names_rows = []
        names_rows.append(n[0]+'('+str(n[1])+')')
        for r in rights:
            names_rows.append(connections.count((n[1], r[1])))
        rights_rows.append(names_rows)
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
        ['Список персонала на проверку знаний.htm',
         'Список персонала на проверку знаний.',
         'Список персонала на проверку знаний.html',
         knowledge_check],
        ['Протокол проверки знаний.htm',
         'Протоколы проверки знаний.',
         'Протоколы проверки знаний.html',
         knowledge_check],
        ['Таблица прав.htm',
         'Таблица прав.',
         'Таблица прав.html',
         rights_rows],
        ]
prompt = [str(i)+' '+s[1] for i,s in enumerate(menu)]
sel = int(input('\n'.join(prompt)+'\n>'))
if 0 <= sel < len(menu):
    template = env.get_template(menu[sel][0])
    html = template.render(data=menu[sel][3],
                           name=menu[sel][1])

    with open(p / menu[sel][2], 'w') as file:
        file.write(html)
else:
    print('Выход')
