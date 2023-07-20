from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_settings import bot
from threading import Thread
from browser import run_browser
from payme import payme










@bot.on_message(filters.private)
def send_link(_, message):
	bot.send_message(
		chat_id = message.chat.id,
		text = f'Переведите указанную сумму по ссылке ниже и <b><u>обязательно укажите в комментарии ваш user_id</u>:</b> <code>{message.from_user.id}</code>\n\nhttps://payme.uz/618e670475752e8a58e1c5e7',
		reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Проверить', callback_data = f'{message.from_user.id}')]])
		)


@bot.on_callback_query()
def callback_handler(_, callback_query):
	answ = payme(callback_query.message.chat.id, 1000)
	bot.send_message(
		chat_id = callback_query.message.chat.id,
		text = str(answ)
		)
























Thread(target=run_browser).start()

bot.run()







