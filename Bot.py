import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

# ===== ТВОИ НАСТРОЙКИ =====
BOT_TOKEN = "9000957505:AAEGEKUsvf_v9UiCi-HaySktu1rJU-7XCA4"
# ==========================

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# Игрушечная база данных (хранит баланс в памяти)
wallets = {} 

# Функция для получения баланса
def get_balance(user_id):
    if user_id not in wallets:
        wallets[user_id] = 0.0
    return wallets[user_id]

# Главное меню (кнопки)
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Мой баланс", callback_data="check_balance")],
        [InlineKeyboardButton(text="🎁 Получить бонус", callback_data="get_bonus")],
        [InlineKeyboardButton(text="📤 Вывести 5 USDT (Фейк)", callback_data="withdraw")]
    ])
    return keyboard

# Обработка команды /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    get_balance(user_id)
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n"
        f"Это симулятор крипто-кошелька 🪙\n\n"
        f"Твой текущий баланс: **{get_balance(user_id)} USDT**\n"
        f"(Это игра, тут нет реальных денег)",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

# Обработка кнопки "Мой баланс"
@dp.callback_query(F.data == "check_balance")
async def check_balance(callback: CallbackQuery):
    user_id = callback.from_user.id
    balance = get_balance(user_id)
    await callback.answer(f"Твой баланс: {balance} USDT", show_alert=True)

# Обработка кнопки "Получить бонус"
@dp.callback_query(F.data == "get_bonus")
async def get_bonus(callback: CallbackQuery):
    user_id = callback.from_user.id
    bonus = round(random.uniform(1.0, 5.0), 2)
    wallets[user_id] = get_balance(user_id) + bonus
    
    await callback.answer(f"Тебе начислено {bonus} USDT! 🎉", show_alert=True)
    
    await callback.message.edit_text(
        f"Привет, {callback.from_user.first_name}!\n"
        f"Это симулятор крипто-кошелька 🪙\n\n"
        f"Твой текущий баланс: **{wallets[user_id]} USDT**\n"
        f"(Это игра, тут нет реальных денег)",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

# Обработка кнопки "Вывести"
@dp.callback_query(F.data == "withdraw")
async def withdraw(callback: CallbackQuery):
    user_id = callback.from_user.id
    balance = get_balance(user_id)
    
    if balance >= 5.0:
        wallets[user_id] = balance - 5.0
        await callback.answer("Успешно выведено 5 USDT! (Ну как выведено... списано 😂)", show_alert=True)
        
        await callback.message.edit_text(
            f"Привет, {callback.from_user.first_name}!\n"
            f"Это симулятор крипто-кошелька 🪙\n\n"
            f"Твой текущий баланс: **{wallets[user_id]} USDT**\n"
            f"(Это игра, тут нет реальных денег)",
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await callback.answer("Недостаточно средств! Сначала жми 'Получить бонус'.", show_alert=True)

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
