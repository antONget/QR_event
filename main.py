from aiogram import Bot, Dispatcher
from handlers import mainh, admin, navigator_events

import logging as lg
import asyncio
from aiogram.types import ErrorEvent
from aiogram.types import FSInputFile
import traceback
from typing import Any, Dict

from settings import conf, sheduler
logger = lg.getLogger(__name__)


async def main():
    lg.basicConfig(level=lg.INFO,
                   # filename="py_log.log",
                   # filemode='w',
                   format='%(filename)s:%(lineno)d #%(levelname)-8s '
                          '[%(asctime)s] - %(name)s - %(message)s')
    bot, dp = conf.bot, conf.dp
    
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_routers(mainh.router, admin.router, navigator_events.router)
    await sheduler.archiever.start_scheduler()

    @dp.error()
    async def error_handler(event: ErrorEvent):
        logger.critical("Критическая ошибка: %s", event.exception, exc_info=True)
        await bot.send_message(chat_id=843554518,
                               text=f'{event.exception}')
        formatted_lines = traceback.format_exc()
        text_file = open('error.txt', 'w')
        text_file.write(str(formatted_lines))
        text_file.close()
        await bot.send_document(chat_id=843554518,
                                document=FSInputFile('error.txt'))

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
    

