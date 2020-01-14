import telebot
from newsapi import NewsApiClient
from itertools import groupby


botToken = '1023706952:AAEzoXtuXn7IYPXzqUyjfytmQzI6CVMPKVA'
botUrl = 'https://api.telegram.org/bot' + botToken + '/'
apiKey = 'fc3c4a1a6478477c950bf27f2500ded9'

newsapi = NewsApiClient(api_key=apiKey)

# https://api.telegram.org/bot1023706952:AAEzoXtuXn7IYPXzqUyjfytmQzI6CVMPKVA/getUpdates

bot = telebot.TeleBot(botToken)

categoriesSelected = []
userLanguage = "gb"

@bot.message_handler(commands=["start"])
def handle_start(message):
    startText = "Hello, I'm your personal news bot!"
    bot.send_message(message.chat.id, startText)
    parse_news()
    # set_language(message)

@bot.message_handler(commands=["help"])
def handle_help(message):
    helpText = "This is help message"
    bot.send_message(message.chat.id, helpText)

@bot.message_handler(commands=["setlang"])
def handle_setlang(message):
    set_language(message)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text == "ru" or message.text == "us" or message.text == "fr" or message.text == "it" or message.text == "de" or message.text == "gb":
        userLanguage = message.text

    bot.send_message(message.chat.id, f"Your language was set to " + message.text + "!\nIf you want to change another - use /setlang")




@bot.message_handler(content_types=["text"])
def handle_text(message):
    global categoriesSelected

    if message.text == "Cancel":
        pass

    if message.text == "Russian top":
        categoriesSelected.append("https://newsapi.org/v2/top-headlines?country=ru&apiKey=" + apiKey)
        print(categoriesSelected[len(categoriesSelected) - 1])

    if message.text == "France top":
        categoriesSelected.append("https://newsapi.org/v2/top-headlines?country=fr&apiKey=" + apiKey)
        print(categoriesSelected[len(categoriesSelected) - 1])

    if message.text == "Apple news":
        categoriesSelected.append("https://newsapi.org/v2/everything?q=apple&&apiKey=" + apiKey)
        print(categoriesSelected[len(categoriesSelected) - 1])

    if message.text == "Continue!":
        categoriesSelectedSet = list(set(categoriesSelected))
        categoriesSelected = categoriesSelectedSet
        print("Here")
        print(categoriesSelected)

def set_language(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboardButton1 = telebot.types.KeyboardButton("ru")
    keyboardButton2 = telebot.types.KeyboardButton("us")
    keyboardButton3 = telebot.types.KeyboardButton("fr")
    keyboardButton4 = telebot.types.KeyboardButton("it")
    keyboardButton5 = telebot.types.KeyboardButton("de")
    keyboardButton6 = telebot.types.KeyboardButton("gb")
    keyboard.add(keyboardButton1, keyboardButton2, keyboardButton3, keyboardButton4, keyboardButton5, keyboardButton6)

    bot.send_message(message.chat.id, "Chose the language you like news will be presented in", reply_markup=keyboard)


def set_categories(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    keyboardButton1 = telebot.types.KeyboardButton("Russian top")
    keyboardButton2 = telebot.types.KeyboardButton("France top")
    keyboardButton3 = telebot.types.KeyboardButton("Apple news")
    keyboardButtonContinue = telebot.types.KeyboardButton("Continue!")
    keyboard.add(keyboardButton1, keyboardButton2, keyboardButton3, keyboardButtonContinue)
    bot.send_message(message.chat.id, "Chose", reply_markup=keyboard)


def parse_news():
    global newsapi
    top_headlines = newsapi.get_top_headlines(language='en', country='us', page=1)

    print(top_headlines['articles'][0])

parse_news()


bot.polling()