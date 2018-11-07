import json
import requests

def file_dowloader():
	with open('refs.txt', 'r') as links_file:
		files = []
		for link in links_file:
			link = link[:-1]
			data = link.split('/', 6)
			user = data[3]
			data = {'branch' : data[5], 'filename' : data[-1]}
			print(data)
			
			r = requests.get(link)
			# print(link)
			# assert r.status_code == 200

			if link[-3:] == '.py':
				print('got python raw')
				file = {**data, **python_file_parser(r.text)}
			elif link[-6:] == '.ipynb':
				print('got notebook')
				file = {**data, **notebook_parser(r.text)}
			
			for entry in files:
				if entry['user'] == user:
					entry['files'].append(file)
					break
			else:
				files.append({'user' : user, 'files' : [file,]})

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