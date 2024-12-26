from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, ChatMemberMember, ChatMemberAdministrator, ChatMemberOwner
from aiogram.types import ErrorEvent
from aiogram.types import FSInputFile

from typing import Any, Callable, Dict, Awaitable

from handlers import mainh, admin, navigator_events, handler_edit_list_personal
from notify_admins import on_startup_notify
import logging as lg
import asyncio
import traceback
from settings import conf, scheduler, kb
logger = lg.getLogger(__name__)

class SubscribeOnChannel(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        u_status = await event.bot.get_chat_member(chat_id=int(conf.get_env_key('CHANNEL_ID')),
                                                   user_id=event.from_user.id)
        if isinstance(u_status, ChatMemberMember) or isinstance(u_status, ChatMemberAdministrator) \
                or isinstance(u_status, ChatMemberOwner):
            return await handler(event, data)

        await event.bot.send_message(chat_id=event.from_user.id,
                                     text="Ты не подписался на канал!",
                                     reply_markup=await kb.subscribe_kb())


async def main():
    lg.basicConfig(
        level=lg.INFO,
        # filename="py_log.log",
        # filemode='w',
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    bot, dp = conf.bot, conf.dp

    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup_notify(bot=bot)
    dp.include_routers(mainh.router, admin.router, navigator_events.router, handler_edit_list_personal.router)
    dp.callback_query.outer_middleware(SubscribeOnChannel())
    dp.message.outer_middleware(SubscribeOnChannel())
    await scheduler.archiever.start_scheduler(bot)

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

