from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

btnProfile = KeyboardButton(text='🔎ИСКАТЬ ФИЛЬМ ПО КОДУ')
profileKeyboard = ReplyKeyboardMarkup(keyboard=[[btnProfile]], resize_keyboard=True)

btnUrlChannel = InlineKeyboardButton(text='Подпишись на канал', url='https://t.me/+MQWs5W2aQVI0MDEy')
btnUrlChannel2 = InlineKeyboardButton(text='Наш второй канал', url='https://t.me/cult_films20_21')
btnDoneSub = InlineKeyboardButton(text='Я ПОДПИСАЛСЯ👍', callback_data='subchanneldone')

checkSubMenu = InlineKeyboardMarkup(inline_keyboard=[[btnUrlChannel],[btnUrlChannel2],[btnDoneSub]])
