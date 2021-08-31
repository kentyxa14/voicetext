import telebot
import config
from gtts import gTTS

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands = ["start"])
def send_welcome(message):
	bot.send_message(message.from_user.id, f"Привествую {message.from_user.first_name}, это простой бот для создание голосового сообщине с набраного текста, протестируй и узнаешь как работает")
	bot.send_message(message.from_user.id, "Просто види текст который ты хочиш зделать в виде голосового сообшение")

@bot.message_handler(content_types = ["text"])
def the_text_to_voice(message):
	theText = message.text
	filename = "voicetext.ogg"
	tts = gTTS(text = theText, lang = "ru")
	tts.save("voicetext.ogg")

	voice = open(filename, mode = 'rb')
	bot.send_voice(chat_id = message.chat.id, voice = voice)

bot.polling(none_stop = True)