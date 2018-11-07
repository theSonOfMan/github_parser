import json
import requests

def file_dowloader():
	with open('refs.txt', 'r') as links_file:
		files = []
		for link in links_file:
			link = link[:-1]
			data = link.split('/', 6)
			data = {'user' : data[3], 'branch' : data[5], 'filename' : data[-1]}
			print(data)
			r = requests.get(link)
			# print(link)
			assert r.status_code == 200
			# print(r.status_code)
			# break
			if link[-3:] == '.py':
				print('got python raw')
				files.append({**data, **python_file_parser(r.text)})
			else:
				print('got notebook')
				files.append({**data, **notebook_parser(r.text)})

	with open('files.json', 'w') as result:
		json.dump(files, result)

	# link = 'https://raw.githubusercontent.com/a-gataullin/PrPythonAtom/homework_02/homeworks/02/my_python_functions/fib_functions/my_functions.py'
	# r = requests.get(link)
	# print(r.text)

def python_file_parser(content):
	return {'type':'python', 'content':content}

def notebook_parser(content):
	content = json.loads(content)
	content = [{'cell_type':cell['cell_type'], 'source':cell['source']} for cell in content['cells'] if cell['cell_type'] == 'code']
	return {'type':'notebook', 'content':content}

file_dowloader()