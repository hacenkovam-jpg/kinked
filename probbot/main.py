import os
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
import keyboards as nav
import db
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [1970597210, 756544829, 8919722055]
CHANNEL_IDS = [ -1003129813974,-1002359663519, -1003744227147]
NOTSUB_MESSAGE = 'Чтобы узнать название фильма, подпишись на канал👇'

logging.basicConfig(level=logging.INFO)
session = AiohttpSession()

if not TOKEN:
    raise ValueError("Критическая ошибка: Переменная BOT_TOKEN не задана в настройках хостинга!")

bot = Bot(token=str(TOKEN), session=session)
dp = Dispatcher()

async def check_sub_channel(user_id: int) -> bool:
    for channel_id in CHANNEL_IDS:
        try:
            member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception as e:
            logging.error(f"Ошибка проверки подписки {user_id} в {channel_id}: {e}")
            return False
    return True


@dp.message(Command("start"))
async def start(message: types.Message):
    if message.chat.type == 'private':
        db.add_user(message.from_user.id)

        # 1. СНАЧАЛА проверяем админа (им подписка не нужна)
        if message.from_user.id in ADMIN_IDS:
            await message.answer('👋 <b>Привет, Админ!</b> Твоя панель управления готова:', parse_mode='HTML',
                                 reply_markup=nav.adminKeyboard)
            return

        # 2. Логика для обычных пользователей
        if await check_sub_channel(message.from_user.id):
            await message.answer('👋 <b>Привет, это кинобот</b>, чтобы искать жми на кнопку', parse_mode='HTML',
                                 reply_markup=nav.profileKeyboard)
        else:
            await message.answer(NOTSUB_MESSAGE, reply_markup=nav.checkSubMenu)


@dp.callback_query(F.data == "subchanneldone")
async def check_subscription_callback(callback: types.CallbackQuery):
    """Обработка кнопки 'Я ПОДПИСАЛСЯ👍'"""
    user_id = callback.from_user.id

    if await check_sub_channel(user_id):
        await callback.message.delete()  # Удаляем сообщение с кнопками каналов

        if user_id in ADMIN_IDS:
            await callback.message.answer('🎉 Спасибо за подписку! Панель управления готова:', parse_mode='HTML',
                                          reply_markup=nav.adminKeyboard)
        else:
            await callback.message.answer('🎉 Спасибо за подписку! Нажми на кнопку ниже для поиска:', parse_mode='HTML',
                                          reply_markup=nav.profileKeyboard)
    else:
        await callback.answer("❌ Вы подписались не на все каналы! Проверьте подписку.", show_alert=True)

@dp.message(F.text)
async def bot_message(message: types.Message):
        if message.text == '📊 СТАТИСТИКА ЗА ВСЕ ВРЕМЯ' and message.from_user.id in ADMIN_IDS:
            total_users = db.get_users_count()
            await message.answer(f"📊 <b>Статистика бота</b>\nВсего пользователей за всё время: <code>{total_users}</code>", parse_mode='HTML')
            return

        if message.text == '📅 СТАТИСТИКА ЗА СЕГОДНЯ' and message.from_user.id in ADMIN_IDS:
            today_users = db.get_today_users_count()
            await message.answer(f"📅 <b>Статистика за сегодня</b>\nНовых пользователей за сегодня: <code>{today_users}</code>", parse_mode='HTML')
            return

        if not await check_sub_channel(message.from_user.id) and message.from_user.id not in ADMIN_IDS:
            await message.answer(NOTSUB_MESSAGE, reply_markup=nav.checkSubMenu)
            return

        if await check_sub_channel(message.from_user.id):
            if message.text == '🔎ИСКАТЬ ФИЛЬМ ПО КОДУ':
                await message.answer('🔎Для поиска отправьте код фильма')
            elif message.text == '001':
                await message.answer('🍿Код: 001 \n<b>Американские животные</b>', parse_mode='HTML')
            elif message.text == '002':
                await message.answer('🍿Код: 002 \n<b>Остров харпера</b>', parse_mode='HTML')
            elif message.text == '003':
                await message.answer('🍿Код: 003 \n<b>Полусвет</b>', parse_mode='HTML')
            elif message.text == '004':
                await message.answer('🍿Код: 004 \n<b>Поворот не туда</b>', parse_mode='HTML')
            elif message.text == '005':
                await message.answer('🍿Код: 005 \n<b>Белый шум</b>', parse_mode='HTML')
            elif message.text == '006':
                await message.answer('🍿Код: 006 \n<b>Обряд</b>', parse_mode='HTML')
            elif message.text == '007':
                await message.answer('🍿Код: 007 \n<b>Прости, Чарли</b>', parse_mode='HTML')
            elif message.text == '008':
                await message.answer('🍿Код: 008 \n<b>Форрест Гамп</b>', parse_mode='HTML')
            elif message.text == '009':
                await message.answer('🍿Код: 009 \n<b>30 дней ночи</b>', parse_mode='HTML')
            elif message.text == '010':
                await message.answer('🍿Код: 010 \n<b>Невозможное</b>', parse_mode='HTML')
            elif message.text == '011':
                await message.answer('🍿Код: 011 \n<b>Колония дигнидад</b>', parse_mode='HTML')
            elif message.text == '012':
                await message.answer('🍿Код: 012 \n<b>Массовый побег</b>', parse_mode='HTML')
            elif message.text == '013':
                await message.answer('🍿Код: 013 \n<b>Волк одиночка</b>', parse_mode='HTML')
            elif message.text == '104':
                await message.answer('🍿 Код: 104 \n<b>Герда</b>', parse_mode='HTML')
            elif message.text == '106':
                await message.answer('🍿 Код: 106 \n<b>Одаренная</b>', parse_mode='HTML')
            elif message.text == '107':
                await message.answer('🍿Код: 107 \n<b>Шоу Трумана</b>', parse_mode='HTML')
            elif message.text == '247':
                await message.answer('🍿Код: 247 \n<b>Семейный план 2023</b>', parse_mode='HTML')
            else:
                await message.answer('<b>🚫Нет фильма с таким кодом</b>', parse_mode='HTML')
        else:
            await message.answer(NOTSUB_MESSAGE, reply_markup=nav.checkSubMenu)


@dp.callback_query(F.data == "subchanneldone")
async def subchanneldone(callback: types.CallbackQuery):
    await callback.message.delete()
    if await check_sub_channel(callback.from_user.id):
        db.add_user(callback.from_user.id)
        if callback.from_user.id in ADMIN_IDS:
            await callback.message.answer('👋<b>Привет, Админ!</b> Твоя панель управления готова:',
                                          parse_mode='HTML', reply_markup=nav.adminKeyboard)
        else:
            await callback.message.answer('👋<b>Привет это кинобот</b>, чтобы искать жми на кнопку',
                                          parse_mode='HTML', reply_markup=nav.profileKeyboard)
    else:
        await callback.message.answer(NOTSUB_MESSAGE, reply_markup=nav.checkSubMenu)

if __name__ == '__main__':
    db.init_db()
    dp.run_polling(bot)



