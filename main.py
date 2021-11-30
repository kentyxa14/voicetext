import telebot
from telebot import *

import config
from gtts import gTTS

bot = telebot.TeleBot(config.TOKEN)

def start_buttons(chat_id, text):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
	buttons = ["Скорость ⏱", "Языки 🌎", "Поддержка 💰"]
	keyboard.add(*buttons)
	bot.send_message(chat_id, text, reply_markup = keyboard)

@bot.message_handler(commands = ["start"])
def send_welcome(message):
	bot.send_message(message.from_user.id, f"Привествую {message.from_user.first_name}, это простой бот для создание голосового сообщине с набраного текста, протестируй и узнаешь как работает")
	start_buttons(message.chat.id, "Просто види текст который ты хочиш зделать в виде голосового сообшение")
	
	verify = []
	data = config.load("user_settings.json")
	for arr in data:
		for user_id in arr:
			if user_id == str(message.chat.id):
				verify.append("good")
	if len(verify) == 0:
		new_user = {str(message.chat.id): {"speed": 1, "lang": "ru", "user_name": message.from_user.username}}
		data.append(new_user)
		config.save("user_settings.json", data)

@bot.message_handler(content_types = ["text"])
def get_text(message):
	theText = message.text
	chat_id = message.chat.id
	if theText == "Скорость ⏱":
		bot.send_message(chat_id, "На данный момент 'Скорость ⏱' не доступни.\nОни будут добавлени в следуйших обновлений!.")
		bot.send_message(chat_id, "Этот параметр нужен для того чтоб ускорять голос или же тон звука.")

	elif theText == "Языки 🌎":
		bot.send_message(chat_id, "На данный момент 'Языки 🌎' не доступни.\nОни будут добавлени в следуйших обновлений!.")
		bot.send_message(chat_id, "Этот параметр нужен для того чтоб поменять язык вашего сообшение.")

	elif theText == "Поддержка 💰":
		keyboard = types.InlineKeyboardMarkup()
		keyboard.row(types.InlineKeyboardButton(text = "> DONATE <", url = config.DONATE))
		bot.send_message(chat_id, "Вот силлка на донат поддержку, зарание спасибо)", reply_markup = keyboard)

	else:
		filename = "voicetext.ogg"
		tts = gTTS(text = theText, lang = "ru")
		tts.save(filename)
		print(f"[{message.from_user.username}] > {theText}")
		voice = open(filename, mode = 'rb')
		bot.send_voice(chat_id = chat_id, voice = voice)

bot.polling(none_stop = True)