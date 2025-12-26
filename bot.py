import random
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from database import *
import asyncio

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

wheel = [
    ("Не повезло", 40),
    ("Энергетик", 5),
    ("Отгул «Лаки»", 2),
    ("Свалить на 2 часа раньше", 3),
    ("Удар по каске", 10),
    ("Удар в пресс", 10),
    ("Удар по жопе", 10),
    ("Отдых от заявок", 5),
    ("Ты должен каждому по энергетику", 5),
    ("Ходишь на 1 заявку, которую попросит другой пользователь", 10)
]

def spin_wheel():
    r = random.randint(1, 100)
    total = 0
    for prize, chance in wheel:
        total += chance
        if r <= total:
            return prize

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await init_db()
    user = await get_user(message.from_user.id)

    if user:
        return await message.answer("Ты уже зарегистрирован! Используй /spin")

    await message.answer("Привет! Введи своё имя:")
    dp.register_message_handler(get_name, state="enter_name")

async def get_name(message: types.Message):
    name = message.text
    await add_user(message.from_user.id, name)
    await message.answer(f"Отлично, {name}! У тебя есть 4 токена. Команда /spin 🎡")
    dp.unregister_message_handler(get_name)

@dp.message_handler(commands=["profile"])
async def profile(message: types.Message):
    user = await get_user(message.from_user.id)
    if not user:
        return await message.answer("Сначала /start и введи имя!")

    _, name, tokens = user
    await message.answer(f"👤 Имя: {name}\n🔋 Токены: {tokens}")

@dp.message_handler(commands=["spin"])
async def spin(message: types.Message):
    user = await get_user(message.from_user.id)
    if not user:
        return await message.answer("Сначала /start")

    user_id, name, tokens = user

    if tokens <= 0:
        return await message.answer("❌ У тебя нет токенов")

    result = spin_wheel()
    await update_tokens(user_id, tokens - 1)
    await save_stat(user_id, name, result)

    await message.answer(f"🎡 Результат: **{result}**")
    await message.answer(f"🔋 Осталось токенов: {tokens - 1}")

@dp.message_handler(commands=["top"])
async def top(message: types.Message):
    records = await get_stats()

    if not records:
        return await message.answer("📊 Статистика пока пустая.")

    text = "📊 Статистика выбиваний:\n\n"
    for name, result in records:
        text += f"• {name} — {result}\n"

    await message.answer(text)

executor.start_polling(dp)
