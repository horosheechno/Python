import datetime
from contextlib import suppress
from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
#from keyboards.calendar_kb import create_calendar_kb
from calendar_kb import create_calendar_kb
from aiogram.filters import Text, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from service import is_correct_date, calendar_parser, list_id
from database import calendar_db

router: Router = Router()

# ========= ветка работы с календарем ==========
'''Переменные '''

#list_keys = list(calendar_db.keys())
day: int = 0
curr_month: int = datetime.datetime.today().month
curr_month_name: str = datetime.datetime.today().strftime('%B')
curr_year: int = datetime.datetime.today().year


@router.message(Command(commands='calendar'))
async def show_calendar(message: Message):
	await calendar_parser()
	list_dates = [calendar_db[c][4] for c in list_id]
	#print(*list_keys, sep='\n')
	await message.answer(
	 text='ДД - День пуст\n<u><b>ДД</b></u> - Есть записи\n📆 - добавление КД\n'
	 '👁 - просмотреть день',
	 reply_markup=create_calendar_kb(datetime.datetime.today().day, curr_month,
	                                 curr_year, list_dates))


@router.message(lambda message: is_correct_date(message.text))
async def ok_fun(message: Message):
	await message.answer(text='Правильный формат')


@router.callback_query(Text(startswith='dobav'))
async def press_calendar_title(callback: CallbackQuery):
	#await callback.answer()
	await callback.answer(
	 text=f'Добавление нового события на {callback.data[5:]}', show_alert=True)
	await callback.message.edit_text(
	 text=(
	  f'Выбрана дата <b>{callback.data[5:]}</b>\n'
	  f'Дальше отправь мне <b>ISIN</b> бумаги\n(12 символов) или нажми кнопку <b>Отмены</b>'
	 ),
	 reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
	  InlineKeyboardButton(text='Нет даты 🥨', callback_data='no_date_button')
	 ], [InlineKeyboardButton(text='Отмена ❌', callback_data='cancel_button')]]))
	# [InlineKeyboardButton(text='Отмена ❌', callback_data='cancel_button')]


@router.callback_query(Text(text='no_day'))
async def press_no_day(callback: CallbackQuery):
	await callback.answer()


@router.callback_query(Text(text='forward_calendar_button'))
async def press_forward_month(callback: CallbackQuery):
	global curr_month, curr_year
	await callback.answer()
	curr_month = curr_month + 1
	if curr_month > 12:
		curr_month = 1
		curr_year = curr_year + 1
	await callback.message.edit_text(
	 text='ДД - День пуст\n<u><b>ДД</b></u> - Есть записи\n📆 - добавление КД\n'
	 '👁 - просмотреть день',
	 reply_markup=create_calendar_kb(None, curr_month, curr_year, List_Date))


@router.callback_query(Text(text='backward_calendar_button'))
async def press_backward_month(callback: CallbackQuery):
	global curr_month, curr_year
	await callback.answer()
	curr_month = curr_month - 1
	if curr_month < 1:
		curr_month = 12
		curr_year = curr_year - 1
	await callback.message.edit_text(
	 text='ДД - День пуст\n<u><b>ДД</b></u> - Есть записи\n📆 - добавление КД\n'
	 '👁 - просмотреть день',
	 reply_markup=create_calendar_kb(None, curr_month, curr_year, List_Date))


@router.callback_query(Text(startswith='day_'))
async def press_day(callback: CallbackQuery):
	global day
	if day != int(callback.data[4:6]):
		await callback.message.edit_text(
		 text='ДД - День пуст\n<u><b>ДД</b></u> - Есть записи\n📆 - добавление КД\n'
		 '👁 - просмотреть день',
		 reply_markup=create_calendar_kb(int(callback.data[4:6]), curr_month,
		                                 curr_year, None))
		day = int(callback.data[4:6])
	else:
		await callback.answer()


@router.callback_query(Text(text='comeback'))
async def press_comeback(callback: CallbackQuery):
	await callback.answer()
	global curr_month, curr_year
	with suppress(TelegramBadRequest):
		curr_month = datetime.datetime.today().month
		curr_year = datetime.datetime.today().year
		await callback.message.edit_text(
		 text='ДД - День пуст\n<u><b>ДД</b></u> - Есть записи\n📆 - добавление КД\n'
		 '👁 - просмотреть день',
		 reply_markup=create_calendar_kb(datetime.datetime.today().day, curr_month,
		                                 curr_year, List_Date))


@router.callback_query(Text(text='browse_day'))
async def press_no_day(callback: CallbackQuery):
	await callback.answer('Нажат глаз')


@router.callback_query(Text(text='cancel_calendar'))
async def press_cancel_calendar(callback: CallbackQuery):
	global curr_month, curr_year
	await callback.answer()
	curr_month = datetime.datetime.today().month
	curr_year = datetime.datetime.today().year
	await callback.message.edit_text(text='📆 <b>Календарь закрыт</b>')
