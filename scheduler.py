from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import Database


class Scheduler:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.db = Database()
        self.scheduler = AsyncIOScheduler()

    async def send_morning_message(self):
        users = self.db.get_all_users()
        for user_id in users:
            await self.bot.send_message(user_id, "Доброе утро!")

    def start(self):
        self.scheduler.add_job(self.send_morning_message, "cron", hour=8, minute=0)
        self.scheduler.start()
