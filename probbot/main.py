import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import keyboards as nav
import db
TOKEN = '8322661609:AAEhNQWpp0ZeIIYO1z5HHZsJMSmmax-gLGA'
ADMIN_ID = 1970597210
CHANNEL_IDS = [ -1003129813974,
               -1002359663519
]
NOTSUB_MESSAGE = 'Чтобы узнать название фильма, подпишись на канал👇'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def check_sub_channel(user_id: int) -> bool:
    for channel_id in CHANNEL_IDS:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        if member.status == 'left':
            return False
    return True


@dp.message(Command("start"))
async def start(message: types.Message):
    if message.chat.type == 'private':
        db.add_user(message.from_user.id)
        if await check_sub_channel(message.from_user.id):
            if message.from_user.id == ADMIN_ID:
                await message.answer('👋<b>Привет, Админ!</b> Твоя панель управления готова:',
                                     parse_mode='HTML', reply_markup=nav.adminKeyboard)
            else:
                await message.answer('👋<b>Привет это кинобот</b>, чтобы искать жми на кнопку',
                                     parse_mode='HTML', reply_markup=nav.profileKeyboard)
        else:
            await message.answer(NOTSUB_MESSAGE, reply_markup=nav.checkSubMenu)


@dp.message(F.text)
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        if message.text == '📊 СТАТИСТИКА' and message.from_user.id == ADMIN_ID:
            total_users = db.get_users_count()
            await message.answer(
                f"📊 <b>Статистика бота</b>\nВсего пользователей запустили бота: <code>{total_users}</code>",
                parse_mode='HTML')
            return
        if await check_sub_channel(message.from_user.id):
            if message.text == '🔎ИСКАТЬ ФИЛЬМ ПО КОДУ':
                await message.answer('🔎Для поиска отправьте код фильма')
            elif message.text == '001':
                await message.answer('🍿Код: 001 \n<b>Американские животные</b>', parse_mode='HTML')
            elif message.text == '002':
                await message.answer('🍿 Код: 002 \n<b>Остров харпера</b>', parse_mode='HTML')
            elif message.text == '102':
                await message.answer('🍿 Код: 102 \n<b>Сериал "На льду"</b>', parse_mode='HTML')
            elif message.text == '003':
                await message.answer('🍿Код: 003 \n<b>Полусвет</b>', parse_mode='HTML')
            elif message.text == '104':
                await message.answer('🍿 Код: 104 \n<b>Герда</b>', parse_mode='HTML')
            elif message.text == '106':
                await message.answer('🍿 Код: 106 \n<b>Одаренная</b>', parse_mode='HTML')
            elif message.text == '107':
                await message.answer('🍿 Код: 107 \n<b>Шоу Трумана</b>', parse_mode='HTML')
            else:
                await message.answer('<b>🚫Нет фильма с таким кодом</b>', parse_mode='HTML')
        else:
            await message.answer(NOTSUB_MESSAGE, reply_markup=nav.checkSubMenu)


@dp.callback_query(F.data == "subchanneldone")
async def subchanneldone(callback: types.CallbackQuery):
    await callback.message.delete()
    if await check_sub_channel(callback.from_user.id):
        db.add_user(callback.from_user.id)
        if callback.from_user.id == ADMIN_ID:
            await callback.message.answer('👋<b>Привет, Админ!</b> Твоя панель управления готова:',
                                          parse_mode='HTML', reply_markup=nav.adminKeyboard)
        else:
            await callback.message.answer('👋<b>Привет это кинобот</b>, чтобы искать жми на кнопку',
                                          parse_mode='HTML', reply_markup=nav.profileKeyboard)
    else:
        await callback.message.answer(NOTSUB_MESSAGE, reply_markup=nav.checkSubMenu)

if __name__ == '__main__':
    dp.run_polling(bot)



