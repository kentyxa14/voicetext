import json
from googletrans import Translator

TOKEN = "1998008539:AAEYMZWMeZ7VboHI8aP5m7jDVJrDP9fQXqY"
NAME = "Voite Bot"
DONATE = str("https://www.privat24.ua/rd/transfer_to_card/?hash=rd%2Ftransfer_to_card%2F%7B%22from%22%3A%22%22%2C%22to%22%3A%224149499392280507%22%2C%22amt%22%3A%220%22%2C%22ccy%22%3A%22UAH%22%7D")

# loading json file
def load(file):
    with open(file, "r") as json_file:
        data = json.load(json_file)
    return data

# update/save json file
def save(file, data):
    with open(file, "w") as json_file:
        json.dump(data, json_file, indent = 4)

# translate text
def translate(text, lang):
	translator = Translator()
	end_text = translator.translate(src = "ru", dest = lang, text = text)
	return end_text.text

# get user language
def get_lang(chat_id):
	data = load("user_settings.json")
	for users in data:
	    for user_id in users:
	        if user_id == str(chat_id):
	            return users[user_id]["lang"]
	            break