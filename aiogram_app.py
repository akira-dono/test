import asyncio
from aiogram import types
from config import bot_token
from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import get_user_by_tg_id, insert_user, update_text

bot = Bot(token=bot_token)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)


class UserText(StatesGroup):
    text = State()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    chat_id = message.from_user.id
    if not get_user_by_tg_id(chat_id):
        insert_user(chat_id)
    await message.answer("Введите ключевое слово, по которому будут определяться важные сообщения.")
    await UserText.text.set()


@dp.message_handler(state=UserText.text)
async def answer(message: types.Message, state: FSMContext):
    update_text(message.from_user.id, message.text)
    await state.finish()
    await message.answer("Готово.")


async def start_bot():
    print("Bot started")
    try:
        await dp.start_polling()

    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.close()


if __name__ == "__main__":
    asyncio.run(start_bot())
