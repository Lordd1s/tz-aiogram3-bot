import asyncio

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import Handlers
from scheduler import Scheduler


class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)
        self.dp = Dispatcher()
        self.handlers = Handlers()
        self.scheduler = Scheduler(self.bot)

    async def start(self):
        self.dp.include_router(self.handlers.router)
        self.scheduler.start()
        await self.dp.start_polling(self.bot)


async def delete_webhook():
    bot = Bot(token=BOT_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()


asyncio.run(delete_webhook())
