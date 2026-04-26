from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

btnProfile = KeyboardButton(text='🔎ИСКАТЬ ФИЛЬМ ПО КОДУ')
profileKeyboard = ReplyKeyboardMarkup(keyboard=[[btnProfile]], resize_keyboard=True)

btnUrlChannel = InlineKeyboardButton(text='Подпишись на канал', url='https://t.me/rodjhdlcmnd') #ссылка на канал
btnDoneSub = InlineKeyboardButton(text='Я ПОДПИСАЛСЯ👍', callback_data='subchanneldone')

checkSubMenu = InlineKeyboardMarkup(inline_keyboard=[[btnUrlChannel], [btnDoneSub]])
