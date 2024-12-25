from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, ChatMemberMember, ChatMemberAdministrator, ChatMemberOwner
from typing import Any, Callable, Dict, Awaitable


from handlers import mainh, admin, navigator_events

import logging as lg
import asyncio

from settings import conf, scheduler, kb






class SubscribeOnChannel(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

            u_status = await event.bot.get_chat_member(chat_id=int(conf.get_env_key('CHANNEL_ID')), user_id=event.from_user.id)
            if isinstance(u_status, ChatMemberMember) or isinstance(u_status, ChatMemberAdministrator) \
                or isinstance(u_status, ChatMemberOwner) :
                return await handler(event, data)  

            await event.bot.send_message(text="Ты не подписался на канал!", chat_id=event.from_user.id, reply_markup=await kb.subscribe_kb())
    









async def main():
    lg.basicConfig(level=lg.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
                    filename='logs.txt',
                    filemode='w'
                        )
    bot, dp = conf.bot, conf.dp
    
    await bot.delete_webhook(drop_pending_updates=True)
    
    dp.include_routers(mainh.router, admin.router, navigator_events.router)
    dp.callback_query.outer_middleware(SubscribeOnChannel())
    dp.message.outer_middleware(SubscribeOnChannel())
    await scheduler.archiever.start_scheduler(bot)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
    

