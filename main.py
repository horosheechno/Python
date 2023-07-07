import os
import asyncio
import logging
import calendar_handlers
from aiogram import Bot, Dispatcher
from service import calendar_parser  #, list_id
#from database import calendar_db

BOT_TOKEN: str = os.environ['BOT_TOKEN']

# Инициализируем логгер
logger = logging.getLogger(__name__)


#list_dates = [calendar_db[c][4] for c in list_id]
async def main():
	logging.basicConfig(level=logging.INFO,
	                    format='%(filename)s:%(lineno)d #%(levelname)-8s '
	                    '[%(asctime)s] - %(name)s - %(message)s')
	# Инициализируем логгер
	logger = logging.getLogger(__name__)
	# Выводим в консоль информацию о начале запуска бота
	logger.info('Стартуем!..')

	# Создаем объекты бота и диспетчера
	bot: Bot = Bot(BOT_TOKEN, parse_mode='HTML')
	dp: Dispatcher = Dispatcher()

	dp.include_router(calendar_handlers.router)

	# Пропускаем накопившиеся апдейты и запускаем polling
	await bot.delete_webhook(drop_pending_updates=True)
	await dp.start_polling(bot)
	await calendar_parser()
	#cal_p = asyncio.create_task(calendar_parser())
	#await cal_p


# запускаем polling
if __name__ == '__main__':
	asyncio.run(main())
