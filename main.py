import asyncio
from aiogram import Bot, Dispatcher, Router


from bot_tools.handlers import router


from aiogram.fsm.storage.memory import MemoryStorage

from config import API_TOKEN
from record_log import log_error, log_info



log_info('бот запущен')

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()


dp = Dispatcher(storage=storage)






async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
