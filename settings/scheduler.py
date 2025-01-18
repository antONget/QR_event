from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.schedulers import Tim
from aiogram import Bot
from database import req

import datetime


class EventsArchiver:
    def __init__(self):
        # self.scheduler = AsyncIOScheduler(timezone=datetime.timezone(datetime.timedelta(hours=6)))
        self.scheduler = AsyncIOScheduler(timezone='Asia/Omsk')
        self.interval_minutes = 3

    async def put_events_to_archive(self):
        events = await req.get_all_events()
        for event in events:
            if event.active and datetime.datetime.now() + datetime.timedelta(hours=1) > event.started_at:
                await req.add_event(id=event.id, active=False)

    async def remember_events(self, bot: Bot):
        now = datetime.datetime.now()
        events = await req.get_all_events()
        for event in events:
            if event.started_at - now <= datetime.timedelta(hours=24) and\
                    event.started_at - now > datetime.timedelta(hours=23):
                #  Получаем список зарегистрированных пользователей для этого события
                registered_users = await req.get_users()
                for user_data in registered_users:
                    if str(event.id) in user_data.events_ids.split(','):
                        await bot.send_message(chat_id=user_data.user_id,
                                               text=f'Напоминаю! Вы зарегистрировались на {event.name}\n'
                                               f'Начало {event.started_at.strftime("%d/%m/%Y-%H:%M")}')

    async def start_scheduler(self, bot: Bot):
        self.scheduler.add_job(self.put_events_to_archive, 'cron', hour='*')
        self.scheduler.add_job(self.remember_events, 'cron', hour='*', args=(bot,))
        self.scheduler.start()


archiever = EventsArchiver()
