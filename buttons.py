from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

markup = ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(KeyboardButton(text='My Info'))
markup.add(KeyboardButton(text='User Info'))
markup.add(KeyboardButton(text='Channel Info'))
markup.add(KeyboardButton(text='Group Info'))

cancel_b=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='cancel'))