#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import pytesseract
import pandas as pd
import numpy as np
import optparse, getpass
import sys
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

__author__ = "consachapi@gmail.com"
__copyright__ = "Copyright 2018, Waqar"
__version__ = "Version 1.0.0"

res = requests.Session()


def welcome():
	print("""
        _______ _  __   __ ____ __  _ __  __ _____
       / _____/ /_/ /  / / __  / / / /  \/ / _____/
      /____    __ /   / / / / / / / / /\  /____   
     _____/ / / \ \  / / /_/ / /_/ / / / /____/ /
    /______/_/   \_\/_/ ____/_____/_/ /_/______/
                     /_/
    		Version 1.0.0 """)

def get_captcha():
	captcha_url = 'http://ccomputo.unsaac.edu.pe/alumno/CaptchaSecurityImages.php?width=100&height=40&characters=6'
	print('[*] Extract capcha from the url: ', captcha_url)
	print('')
	try:
		captcha = res.get(captcha_url, timeout=6)
		state_code = captcha.status_code
		print('[*] State code:', captcha.status_code)
		if state_code == 200:
			sessionID = captcha.cookies['PHPSESSID']
			print('[+] Session ID: ', sessionID)
			image = Image.open(BytesIO(captcha.content))
			captcha_text = pytesseract.image_to_string(image)
			print('[+] Captcha Text: ', captcha_text)
			return captcha_text
	except Exception as e:
		print('[!] Checking internet connection failed: ', format(e))
		sys.exit()

def login(user, password):
	captcha_text = get_captcha()
	pyload = {
		'user': user,
		'pass': password,
		'security_code': captcha_text
	}
	print('')
	print('[*] Connecting to the website http://ccomputo.unsaac.edu.pe/alumno/')
	res_login = res.post("http://ccomputo.unsaac.edu.pe/alumno/validate.php", data=pyload)
	url_login = res_login.url
	msg_2 = 'http://ccomputo.unsaac.edu.pe/alumno/?msg=2'
	msg_3 = 'http://ccomputo.unsaac.edu.pe/alumno/?msg=3'
	msg_4 = 'http://ccomputo.unsaac.edu.pe/alumno/?msg=4'
	if url_login == msg_2:
		print('[!] Checking user: ', user)
		return ''
	elif url_login == msg_3:
		print('[!] Checking password')
		return ''
	elif url_login == msg_4:
		print('[!] Checking captcha')
		return ''
	else:
		print('[!] Url access: ', url_login)
		return url_login

def get_report(url_login):
	res_report = res.get(url_login + "&op=2")
	url_report = res_report.url
	print('')
	print('[*] Access report: CONSTACIA DE MATRICULA')
	print('[+] Url reports: ', url_report)
	return url_report

def get_const(url_report):
	data_matr = {
		'semestre':'2018-1'
	}
	print('')
	print('[*] Loading reporting...')
	res_cons_matr = res.post(url_report, data=data_matr)
	print('[+] Url const. matr: ', res_cons_matr.url)
	return res_cons_matr

def generate_report(content):
	soup = BeautifulSoup(content, 'html.parser')
	table = soup.table
	print('')
	print('[+] DATOS:')
	table_td = table.find_all('td')
	for k in table_td:
		print(k.text)
		
	print('')
	table = soup.find('table', {'class': 'ttexto'})
	cursos = []
	for row in table.find_all('tr'):
		cols = row.find_all('td')
		if len(cols) == 6:
			cursos.append((cols[0].text.strip(), cols[1].text.strip(), cols[2].text.strip(), cols[3].text.strip(),cols[4].text.strip()))
	return cursos

def save_report(cursos):
	print('[*] Creating report...')
	cursos_array = np.asarray(cursos)
	df = pd.DataFrame(cursos_array)
	df.columns = ['Nro', 'Curso', 'Nombre', 'Cred.', 'Cat.']
	print('[+] CONTANCIA DE MATRICULA')
	print('')
	print(df)
	df.to_csv('cursos.csv')
	print('')
	print('[+] Save report file type csv: OK')
	
def main():
	welcome()
	print('')
	parser = optparse.OptionParser("python" + " " + "%prog -u <<User>>", version=__version__)
	parser.add_option("-u", "--user", dest='user', help='Insert the user to enter the websiter')
	(options, args) = parser.parse_args()
	mandatories = 'user'
	if not options.__dict__[mandatories]:
		parser.print_help()
		sys.exit()
	pass_login = getpass.getpass('[*] Insert password: ')
	url_login = login(options.user, pass_login)
	if url_login == '':
		sys.exit()
	else:
		url_report = get_report(url_login)
		res_cons_matr = get_const(url_report)
		content = res_cons_matr.content
		cursos = generate_report(content)
		save_report(cursos)

if __name__ == '__main__':
    main()