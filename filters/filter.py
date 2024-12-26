from aiogram.filters import Filter
from aiogram.types import Message
from settings import conf


class AdminProtect(Filter):
    async def __call__(self, message: Message) -> bool:
        return str(message.from_user.id) in conf.get_env_key('ADMIN_IDS').split(',')
