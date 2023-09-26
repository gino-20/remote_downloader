import asyncio
import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config


async def main():
    router = Router()

    @router.message(Command("start"))
    async def start_handler(msg: Message):
        await msg.answer("Привет! Чем помочь?")

    @router.message()
    async def message_handler(msg: Message):
        if (msg.from_user.id not in config.ALLOWED_IDS) or not msg.document:
            await msg.answer("Прости,брат. Не знаю, что с этим делать :-(")
            return
        await msg.answer("Так, кажется, знаю, что с этим делать, момент...")
        if not msg.document.file_name.endswith('.torrent'):
            await msg.answer("С таким работать пока не умею :-(")
            return
        file_id = msg.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        await bot.download_file(file_path, '/torrent/'+msg.document.file_name)
        await msg.answer("Супер! Процесс должен начаться с минуты на минуту!")

    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
