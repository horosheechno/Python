import datetime
#import database
from httpx import get
#import time
#import asyncio
#import feedparser
from database import calendar_db

# variables
calendar_db = calendar_db
list_id: list = []
start_date: str = '2023-07-01'  # ISO формат: YYYY-MM-DD
end_date: str = '2023-07-31'  # ISO формат: YYYY-MM-DD
URL: str = f'https://stockstrategy.ru/api/server/calendar?start={start_date}T00%3A00%3A00%2B03%3A00&end={end_date}T00%3A00%3A00%2B03%3A00'


def is_correct_date(string: str) -> bool:
	try:
		if datetime.datetime.strptime(string, '%d.%m.%Y'):
			return True
		else:
			return False
	except Exception:
		return False


def date1_before_date2(date1: str, date2: str) -> bool:
	try:
		D1 = datetime.datetime.strptime(date1, '%d.%m.%Y')
		D2 = datetime.datetime.strptime(date2, '%d.%m.%Y')
		if D1 <= D2:
			return True
		else:
			return False
	except Exception:
		return False


#st1, st2 = input('date1: '), input('date2: ')
#print(date1_before_date2(st1, st2))


def prav_date(iso_date: str) -> str:
	if '-' in iso_date:
		rezult = iso_date.split('-')
	elif '.' in iso_date:
		rezult = iso_date.split('.')
	else:
		return
	rezult[0] = '0' + rezult[0] if len(rezult[0]) == 1 else rezult[0]
	rezult[1] = '0' + rezult[1] if len(rezult[1]) == 1 else rezult[1]
	rezult[2] = '0' + rezult[2] if len(rezult[2]) == 1 else rezult[2]
	if len(rezult[0]) == 4:
		rezult[2], rezult[0] = rezult[0], rezult[2]
	rezult = '.'.join(rezult)
	return rezult


def us_date(rus_date: str) -> str:
	if '-' in rus_date:
		rezult = rus_date.split('-')
	elif '.' in rus_date:
		rezult = rus_date.split('.')
	else:
		return
	rezult[0] = '0' + rezult[0] if len(rezult[0]) == 1 else rezult[0]
	rezult[1] = '0' + rezult[1] if len(rezult[1]) == 1 else rezult[1]
	rezult[2], rezult[0] = rezult[0], rezult[2]
	rezult = '.'.join(rezult)
	return rezult


async def calendar_parser():
	global calendar_db
	print('================ Запрос календаря ===')
	resp = get(URL)
	print('Статус:', resp.status_code)
	rez = resp.json()
	#with open('rez.txt', 'w') as file:
	#	file.write(str(rez))
	#file.write('======== новости ===\n\n' + str(rez))
	#list_id = [str(rez[i]['id']) for i in range(len(rez))]
	for item in range(len(rez)):  #range(10):
		list_id.append(str(rez[item]['id']))
		if list_id[item] not in (str(calendar_db.keys())):
			calendar_db[str(rez[item]['id'])] = [
			 rez[item]['code_event'], rez[item]['div_cur'], rez[item]['div_rec'],
			 rez[item]['dividend_period'],
			 prav_date(rez[item]['end_event']), rez[item]['event_text'],
			 rez[item]['isin'], rez[item]['repo'],
			 prav_date(rez[item]['start']), rez[item]['tiker'], rez[item]['title']
			]
		#print(*calendar_db[rez[item]['id']], end='\n')

	#	if not link_dict[key] in moex_db:
	#		moex_db[link_dict[key]] = [rez['response']['text'][key], rez['response']['exchenge'][key]]
	#print('==> Число записей:', *list_id, sep='\n')
	#list_keys = list(calendar_db.keys())
	#list_keys =
	#return  # calendar_db


#st = input()
#print(prav_date(st))
#calendar_parser()
#list_start_date = [calendar_db[id][8] for id in calendar_db.keys()]

#print(datetime.datetime.strptime(stroka, '%d.%m.%Y'))
#print(calendar_db, end='\n')
#print(calendar_db, sep='\n')
