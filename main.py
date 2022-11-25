import csv

class Rights:
	def __init__(self):
		self.rights = []
		with open('Права.csv', 'r', encoding='UTF-8') as file:
			reader = csv.reader(file)
			for row in reader:
				self.rights.append(row)

	def electro(self, right):
		'''Если право по электробезопасности то возвращает True иначе False'''
		for i in self.rights:
			if i[0] == right:
				if i[5] == '1':
					return True
				else:
					return False
		raise Exception('Нет такого права по электробезопасности!')

	def spec(self, right):
		'''Если право cgt то возвращает True иначе False'''
		for i in self.rights:
			if i[0] == right:
				if i[6] == '1':
					return True
				else:
					return False
		raise Exception('Нет такого специального права!')

person = []
with open('Персонал.csv', 'r', encoding='UTF-8') as file:
	reader = csv.reader(file)
	for row in reader:
		person.append(row)
	person.sort(key=lambda prsn: prsn[1])

select = []
with open('Выбор.csv', 'r', encoding='UTF-8') as file:
	reader = csv.reader(file)
	for row in reader:
		select.append(row)

rights_persons = []
with open('Права работников.csv', 'r', encoding='UTF-8') as file:
	reader = csv.reader(file)
	for row in reader:
		rights_persons.append(row)

rights = Rights()

with open('Заявка на экзамен.csv', 'w', newline="", encoding='UTF-8') as file:
	writer = csv.writer(file)
	for i in select:
		out = []
		for p in person:
			if i[0] == p[0]:
				out.append(p[0])
				out.append(p[1])
				out.append(p[3])
				out.append(p[4])
				out.append(p[4])
		ri = ''
		ri_spec = ''
		for r in rights_persons:
			if r[0] == i[0]:
				if rights.electro(r[1]):
					ri += r[1] + ','
				if rights.spec(r[1]):
					ri_spec += r[1] + ','
		out.insert(3, ri[:-1])
		out.insert(4, ri_spec[:-1])
		writer.writerow(out)

with open('Персонал оформленный в СРЗАИ для СОТЭиОТ.csv', 'w', newline="", encoding='UTF-8') as file:
	writer = csv.writer(file)
	writer.writerow(['Информация по персоналу СРЗАИ, который оформляется в подразделении при проведении периодической проверки знаний в январе 2022 года.'])
	for ni, i in enumerate(select):
		out = []
		out.append(ni+1)
		for p in person:
			if i[0] == p[0]:
				out.append(p[0])
				out.append(p[1])
				out.append(p[5])
		ri = ''
		ri_spec = ''
		for r in rights_persons:
			if r[0] == i[0]:
				if rights.electro(r[1]):
					ri += r[1] + ','
				if rights.spec(r[1]):
					ri_spec += r[1] + ','
		out.append(ri[:-1])
		out.append(ri_spec[:-1])
		out.append('прошёл')
		out.append('прошёл')
		writer.writerow(out)

with open('График проверки знаний.csv', 'w', newline="", encoding='UTF-8') as file:
	writer = csv.writer(file)
	for i, p in enumerate(person):
		out = []
		out.append(i+1)
		out.append(p[0])
		out.append(p[1])
		out.append(p[3])
		out.append(p[4])
		out.append(p[4])
		out.append(p[5])
		out.append('')
		out.append(p[5])
		out.append('')
		ri = ''
		ri_spec = ''
		for r in rights_persons:
			if r[0] == p[0]:
				if rights.electro(r[1]):
					ri += r[1] + ','
				if rights.spec(r[1]):
					ri_spec += r[1] + ','
		out.insert(4, ri[:-1])
		out.insert(5, ri_spec[:-1])
		writer.writerow(out)


