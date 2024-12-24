from apscheduler.schedulers.asyncio import AsyncIOScheduler

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

    async def start_scheduler(self):
        self.scheduler.add_job(self.put_events_to_archive, 'interval', minutes=self.interval_minutes)
        self.scheduler.start()


archiever = EventsArchiver()
