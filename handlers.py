from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import wikipediaapi

from config import USER_AGENT
from database import Database

db = Database()


class Handlers:
    def __init__(self):
        self.router = Router()
        self.wiki = wikipediaapi.Wikipedia(user_agent=USER_AGENT, language="ru")
        self.setup_handlers()

    def setup_handlers(self):
        self.router.message.register(self.wiki_handler, F.text.startswith("/wiki"))
        self.router.message.register(
            self.echo_handler, F.text & ~F.text.startswith("/")
        )

    async def echo_handler(self, message: types.Message):
        user_id = message.from_user.id
        if user_id not in db.get_all_users():
            db.add_user(user_id)
        await message.answer(message.text)

    async def wiki_handler(self, message: types.Message):
        query = message.text.replace("/wiki", "").strip()
        if not query:
            await message.answer("Введите запрос после /wiki")
            return

        page = self.wiki.page(query)
        if not page.exists():
            await message.answer("Страница не найдена.")
            return

        summary = page.summary[:1000]
        url = page.fullurl
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Читать дальше", url=url)]]
        )
        await message.answer(summary + "...", reply_markup=keyboard)
