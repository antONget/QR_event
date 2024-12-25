from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from database import req

import datetime


class EventsArchiver:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.interval_minutes = 3

    async def put_events_to_archive(self):
        events = await req.get_all_events()
        for event in events:
            if event.active and datetime.datetime.now() > event.started_at:
                await req.add_event(id=event.id, active=False)

    async def remember_events(self, bot: Bot):
        now = datetime.datetime.now()
        events = await req.get_all_events()
        for event in events:
            if event.started_at - now <= datetime.timedelta(days=1) and event.started_at - now > datetime.timedelta(days=0):
                registered_users = await req.get_users()  # Получаем список зарегистрированных пользователей для этого события
                for user_data in registered_users:
                    if str(event.id) in user_data.events_ids.split(','):
                        await bot.send_message(chat_id=user_data.user_id,
                                               text=f'<b>Напоминаю! Вы зарегестрировались на {event.name}\n'
                                               f'Оно начинается <b>{event.started_at.strftime('%d/%m/%Y-%H:%M')}</b></b>')
                        
        
        # print("Запланированная рассылка напоминаний завершена")

    async def start_scheduler(self, bot: Bot):
        self.scheduler.add_job(self.put_events_to_archive, 'interval', minutes=self.interval_minutes)
        self.scheduler.add_job(self.remember_events, 'interval', minutes=1, args=(bot,))
        self.scheduler.start()


archiever = EventsArchiver()

# import asyncio
# asyncio.run(archiever.start_scheduler())