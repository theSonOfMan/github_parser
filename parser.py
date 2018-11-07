import requests
from bs4 import BeautifulSoup
#import json
import re
import sys

# Получение имени ветки из консоли
branch = sys.argv[1]
branch = branch + "/homeworks/" + branch[-2:]

# Константы
github = "https://github.com"
raw = "https://raw.githubusercontent.com"
type_refs = {
	-1: 'trash file',
	 0: 'Directory',
	 1: '.ipynb file',
	 2: '.py file'
}

# Отправка запроса на страницу со всеми форками
r = requests.get("https://github.com/Kinetikm/PrPythonAtom/network/members")

# Находим ссылки на все репозитории
soup = BeautifulSoup(r.text, "html.parser")
mas = soup.findAll("div", attrs={"class": ["repo"]})[1:]

# Определить тип ссылки
def get_type_ref(ref):
	result = re.search(r'\.ipynb$', ref)
	if result:
		return 1
	result = re.search(r'\.py$', ref)
	if result:
		return 2
	result = re.findall(r'\/[^\.]+$', ref)
	if result:
		return 0
	return -1

# Все репозитории
repos = []
for i in mas:
	repos.append(github + i.findAll('a')[1]['href'] + "/tree/" + branch)

# Запись в файл
f = open('refs.txt', 'w')	

# Здесь можешь записывать в словарь или еще куда-то
def write_res(ref):
	f.write(ref + "\n")

# Собрать все рекурсивно из папки
def parse_dir(directory):
	r = requests.get(directory)
	soup = BeautifulSoup(r.text, "html.parser")
	mas = soup.findAll("td", attrs={"class": ["content"]})[1:]
	for refs in mas:
		ref = refs.find('a')['href']
		type_ref = get_type_ref(ref)
		if type_ref > 0:
			ref = re.sub(r'/blob', '', raw + ref)
			write_res(ref)
		elif type_ref == 0:
			parse_dir(github + ref)

# Собрать все из репозиториев
for repo in repos:
	parse_dir(repo)

# Закрытие файла
f.close()