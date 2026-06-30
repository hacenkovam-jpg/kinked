import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import keyboards as nav

TOKEN = '8322661609:AAEhNQWpp0ZeIIYO1z5HHZsJMSmmax-gLGA'
CHANNEL_ID = '-1003129813974'
NOTSUB_MESSAGE = 'Чтобы узнать название фильма, подпишись на канал👇'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def check_sub_channel(user_id: int) -> bool:
    chat_member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
    return chat_member.status != 'left'

@dp.message(Command("start"))
async def start(message: types.Message):
    if message.chat.type == 'private':
        if await check_sub_channel(message.from_user.id):
            await message.answer('👋<b>Привет это кинобот</b>, чтобы искать жми на кнопку',
                                 parse_mode='HTML', reply_markup=nav.profileKeyboard)
        else:
            await message.answer(NOTSUB_MESSAGE, reply_markup=nav.checkSubMenu)

@dp.message(F.text)
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        if await check_sub_channel(message.from_user.id):
            if message.text == '🔎ИСКАТЬ ФИЛЬМ ПО КОДУ':
                await message.answer('🔎Для поиска отправьте код фильма')
            elif message.text == '100':
                await message.answer('🍿 Код: 100 \n<b>Как взломать экзамен</b>', parse_mode='HTML')
            elif message.text == '101':
                await message.answer('🍿 Код: 101 \n<b>Миссис Медоуз (2014)</b>', parse_mode='HTML')
            elif message.text == '102':
                await message.answer('🍿 Код: 102 \n<b>Сериал "На льду"</b>', parse_mode='HTML')
            elif message.text == '103':
                await message.answer('🍿 Код: 103 \n<b>Поймай меня если сможешь 2002</b>', parse_mode='HTML')
            elif message.text == '104':
                await message.answer('🍿 Код: 104 \n<b>Герда</b>', parse_mode='HTML')
            elif message.text == '105':
                await message.answer('🍿 Код: 105 \n<b>Мое прекрасное несчастье 2023</b>', parse_mode='HTML')
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
        await callback.message.answer('👋<b>Привет это кинобот</b>, чтобы искать жми на кнопку',
                                      parse_mode='HTML', reply_markup=nav.profileKeyboard)
    else:
        await callback.message.answer(NOTSUB_MESSAGE, reply_markup=nav.checkSubMenu)

if __name__ == '__main__':
    dp.run_polling(bot)



