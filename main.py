import telebot
import config
from gtts import gTTS

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands = ["start"])
def send_welcome(ctx):
	bot.send_message(ctx.from_user.id, f"Привествую {ctx.from_user.first_name}, это простой бот для создание голосового сообщине с набраного текста, протестируй и узнаешь как работает")
	bot.send_message(ctx.from_user.id, "Просто види текст который ты хочиш зделать в виде голосового сообшение")

@bot.message_handler(commands = ["help"])
def send_help(ctx):
	text_help = """Как работать с ботом?

1. Отправте боту любой текст и даже эмоджик (Кроме: голосового, видео, фото, и т.д)
2. Вы получаете сообщение в виде голосового сообщение
3. Вы можите его прослушать и сохранить для потребностей, или отправить пользователю нажав "ПЕРЕСЛАТЬ" и выбрать пользователя.

Надеюсь вы поняли как пользоваться, а я пошол даже работать!
"""
	bot.send_message(ctx.from_user.id, text_help)

@bot.message_handler(content_types = ["text"])
def the_text_to_voice(ctx):
	theText = ctx.text
	filename = "voicetext.ogg"
	tts = gTTS(text = theText, lang = "ru")
	tts.save("voicetext.ogg")

	voice = open(filename, mode = 'rb')
	bot.send_voice(chat_id = ctx.chat.id, voice = voice)

bot.polling(none_stop = True)