import telebot
from telebot import *

import config
from config import translate
from gtts import gTTS

bot = telebot.TeleBot(config.TOKEN)

def start_buttons(chat_id, text, lang):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
	buttons = [translate("Скорость ⏱", lang), translate("Языки 🌎", lang), translate("Поддержка 💰", lang)]
	keyboard.add(*buttons)
	bot.send_message(chat_id, translate(text, lang), reply_markup = keyboard)

@bot.message_handler(commands = ["start"])
def send_welcome(message):
	bot.send_message(message.from_user.id, f"Привествую {message.from_user.first_name}, это простой бот для создание голосового сообщине с набраного текста, протестируй и узнаешь как работает")
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
	buttons = ["Скорость ⏱", "Языки 🌎", "Поддержка 💰"]
	keyboard.add(*buttons)
	bot.send_message(message.chat.id, "Просто види текст который ты хочиш зделать в виде голосового сообшение", reply_markup=keyboard)
	
	verify = []
	chat_id = message.chat.id
	data = config.load("user_settings.json")
	for arr in data:
		for user_id in arr:
			if user_id == str(chat_id):
				verify.append("good")
	if len(verify) == 0:
		new_user = {str(chat_id): {"speed": 1, "lang": "ru", "user_name": message.from_user.username}}
		data.append(new_user)
		config.save("user_settings.json", data)

@bot.message_handler(content_types = ["text"])
def get_text(message):
	lang = config.get_lang(message.chat.id)
	theText = message.text
	if theText == translate("Скорость ⏱", lang):
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
		buttons = ["x0.5", "x1", "x2"]
		keyboard.add(*buttons)
		bot.send_message(message.chat.id, translate("Выбери жилаемою скорость...", lang), reply_markup = keyboard)

	elif theText == "x0.5" or theText == "x1" or theText == "x2":
		start_buttons(message.chat.id, translate("Ускарение голоса пока не доступна, буде добавленно в следуйших обновлений!", lang), lang)
			# keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
			# buttons = [translate("Скорость ⏱", lang), translate("Языки 🌎", lang), translate("Поддержка 💰", lang)]
			# keyboard.add(*buttons)
			# bot.send_message(message.chat.id, translate("Параметры были обновлени", lang), reply_markup = keyboard)

	elif theText == translate("Языки 🌎", lang):
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
		keyboard.add("Русский")
		keyboard.add("English")
		keyboard.add(translate("Не нашли язык?", lang))
		bot.send_message(message.chat.id, translate("Выберите жилаемый язык...", lang), reply_markup = keyboard)

	# Языки перевода
	elif theText == "Русский":
		data = config.load("user_settings.json")
		for users in data:
			for user_id in users:
				if user_id == str(message.chat.id):
					users[user_id]["lang"] = "ru"
					config.save("user_settings.json", data)
					break
		start_buttons(message.chat.id, "Параметры были обновлени", "ru")

	elif theText == "English":
		data = config.load("user_settings.json")
		for users in data:
			for user_id in users:
				if user_id == str(message.chat.id):
					users[user_id]["lang"] = "en"
					config.save("user_settings.json", data)
					break
		start_buttons(message.chat.id, "Параметры были обновлени", "en")

	elif theText == translate("Не нашли язык?", lang):
		keyboard = types.InlineKeyboardMarkup()
		keyboard.row(types.InlineKeyboardButton(text = "> @kentyxa14 <", url = "https://t.me/kentyxa14"))
		bot.send_message(message.chat.id, translate("Обратитесь в помощь у этого человека он ответит на ваш вопрос на вашем языке, если вы не русский)", lang), reply_markup = keyboard)

	elif theText == translate("Поддержка 💰", lang):
		keyboard = types.InlineKeyboardMarkup()
		keyboard.row(types.InlineKeyboardButton(text = "> DONATE <", url = config.DONATE))
		bot.send_message(message.chat.id, translate("Вот силлка на донат поддержку, зарание спасибо)", lang), reply_markup = keyboard)

	else:
		filename = "voicetext.ogg"
		tts = gTTS(text = theText, lang = lang)
		tts.save(filename)
		print(f"[{message.from_user.username}] > {message.text}")
		voice = open(filename, mode = 'rb')
		bot.send_voice(chat_id = message.chat.id, voice = voice)

bot.polling(none_stop = True)