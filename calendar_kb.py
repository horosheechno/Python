import calendar, datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import calendar_db
from service import list_id, prav_date

#from calendar_handlers import keys


#list_dates = [calendar_db[c][4] for c in list_id]
#print(list_dates)
def create_calendar_kb(Day: None | int in range(1, 32), Month: int
                       in range(1, 13), Year: int,
                       List_Date: list | None) -> InlineKeyboardMarkup:
	#global list_dates

	print('Записей в календаре:', len(List_Date))
	kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
	list_button: list[list[InlineKeyboardButton]] = []
	cal = calendar.Calendar()
	if Day is None:
		curr_month_name: str = datetime.datetime(Year, Month, 15).strftime('%B')
	else:
		curr_month_name: str = datetime.datetime(Year, Month, Day).strftime('%B')

	for i in cal.itermonthdays(year=Year, month=Month):
		if i != 0:
			#print('Формирование дат: ', prav_date(f'{i}.{Month}.{Year}'), end='\n')
			if prav_date(f'{i}.{Month}.{Year}') in List_Date:
				text = f'{i} ❕'
				#print('Совпало: ', text, end='\n')
			else:
				text = f'{i}'
				#print('Не совпало: ', text, end='\n')

			if i < 10:
				callback_text = f'day_0{i}.{Month}.{Year}'
			else:
				callback_text = f'day_{i}.{Month}.{Year}'

		else:
			text = ' '
			callback_text = 'no_day'

		list_button.append(
		 InlineKeyboardButton(text=text, callback_data=callback_text))

	if Day is None:
		text = f'📆 	{curr_month_name} {Year}'
	else:
		text = f'📆		{Day} {curr_month_name} {Year}'
		callback_text = f'dobav{Day}.{datetime.datetime(Year, Month, Day).strftime("%m")}.{Year}'

	kb_builder.row(InlineKeyboardButton(text=text, callback_data=callback_text))
	kb_builder.row(*[
	 InlineKeyboardButton(text=c, callback_data='no_day')
	 for c in ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс')
	])
	kb_builder.row(*list_button, width=7)
	kb_builder.row(
	 InlineKeyboardButton(text='Закрыть ❌', callback_data='cancel_calendar'),
	 InlineKeyboardButton(text='👁', callback_data='browse_day'),
	 InlineKeyboardButton(text='🔃 Тек.дата', callback_data='comeback'))
	kb_builder.row(
	 InlineKeyboardButton(text='⬅ Месяц',
	                      callback_data='backward_calendar_button'),
	 InlineKeyboardButton(text='Месяц ➡',
	                      callback_data='forward_calendar_button'))
	return kb_builder.as_markup()
