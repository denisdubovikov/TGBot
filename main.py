import telebot
from newsapi import NewsApiClient
from itertools import groupby
import constants

apiKey = constants.apiKey
botToken = constants.botToken

newsapi = NewsApiClient(api_key=apiKey)

bot = telebot.TeleBot(botToken)

categoriesSelected = []
userLanguage = "gb"

ID = ''

@bot.message_handler(commands=["start"])
def handle_start(message):
    startText = "Hello, I'm your personal news bot!"
    bot.send_message(message.chat.id, startText)

    offer_to_set_categories(message)
    # parse_news()
    # set_language(message)


@bot.message_handler(commands=["help"])
def handle_help(message):
    helpText = "This is help message"
    bot.send_message(message.chat.id, helpText)

@bot.message_handler(commands=["setlang"])
def handle_setlang(message):
    set_language(message)


# @bot.message_handler(content_types=["text"])
# def handle_text(message):
#     if message.text == "ru" or message.text == "us" or message.text == "fr" or message.text == "it" or message.text == "de" or message.text == "gb":
#         userLanguage = message.text
#
#     bot.send_message(message.chat.id, f"Your language was set to " + message.text + "!\nIf you want to change another - use /setlang")




@bot.message_handler(content_types=["text"])
def handle_text(message):
    global categoriesSelected

    if message.text == "Cancel":
        pass

    # if message.text == "Russian top":
    #     categoriesSelected.append("https://newsapi.org/v2/top-headlines?country=ru&apiKey=" + apiKey)
    #     print(categoriesSelected[len(categoriesSelected) - 1])
    #
    # if message.text == "France top":
    #     categoriesSelected.append("https://newsapi.org/v2/top-headlines?country=fr&apiKey=" + apiKey)
    #     print(categoriesSelected[len(categoriesSelected) - 1])
    #
    # if message.text == "Apple news":
    #     categoriesSelected.append("https://newsapi.org/v2/everything?q=apple&&apiKey=" + apiKey)
    #     print(categoriesSelected[len(categoriesSelected) - 1])
    #
    # if message.text == "Continue!":
    #     categoriesSelectedSet = list(set(categoriesSelected))
    #     categoriesSelected = categoriesSelectedSet
    #     print("Here")
    #     print(categoriesSelected)

def set_language(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboardButton1 = telebot.types.KeyboardButton("ru")
    keyboardButton2 = telebot.types.KeyboardButton("us")
    # keyboardButton3 = telebot.types.KeyboardButton("fr")
    # keyboardButton4 = telebot.types.KeyboardButton("it")
    # keyboardButton5 = telebot.types.KeyboardButton("de")
    # keyboardButton6 = telebot.types.KeyboardButton("gb")
    keyboard.add(keyboardButton1, keyboardButton2)

    bot.send_message(message.chat.id, "Chose the language of the interface", reply_markup=keyboard)


def offer_to_set_categories(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboardButton1 = telebot.types.InlineKeyboardButton("Now", callback_data='setCategoriesNow')
    keyboardButton2 = telebot.types.InlineKeyboardButton("Later", callback_data='setCategoriesLater')
    keyboard.add(keyboardButton1, keyboardButton2)

    bot.send_message(message.chat.id, "Do you want to set favorite categories?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data == 'setCategoriesNow')
def set_categories_now(c):
    bot.answer_callback_query(callback_query_id=c.id)
    # bot.send_message(c.message.chat.id, 'Now pressed')
    set_categories(c.message)


def set_categories(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboardButton1 = telebot.types.InlineKeyboardButton("Russian top", callback_data='ruTop')
    keyboardButton2 = telebot.types.InlineKeyboardButton("France top", callback_data='frTop')
    keyboardButton3 = telebot.types.InlineKeyboardButton("Apple news", callback_data='apTop')
    keyboardButtonContinue = telebot.types.InlineKeyboardButton("Continue!", callback_data='continue')
    keyboard.add(keyboardButton1, keyboardButton2, keyboardButton3, keyboardButtonContinue)
    bot.send_message(message.chat.id, "Chose", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data == 'ruTop')
def set_categories_now(c):
    bot.answer_callback_query(callback_query_id=c.id)

    categoriesSelected.append("https://newsapi.org/v2/top-headlines?country=ru&apiKey=" + apiKey)
    print(categoriesSelected[len(categoriesSelected) - 1])

    bot.send_message(c.message.chat.id, 'Added')


@bot.callback_query_handler(func=lambda c: c.data == 'frTop')
def set_categories_now(c):
    bot.answer_callback_query(callback_query_id=c.id)

    categoriesSelected.append("https://newsapi.org/v2/top-headlines?country=fr&apiKey=" + apiKey)
    print(categoriesSelected[len(categoriesSelected) - 1])

    bot.send_message(c.message.chat.id, 'Added')


@bot.callback_query_handler(func=lambda c: c.data == 'apTop')
def set_categories_now(c):
    bot.answer_callback_query(callback_query_id=c.id)

    categoriesSelected.append("https://newsapi.org/v2/top-headlines?q=apple&apiKey=" + apiKey)
    print(categoriesSelected[len(categoriesSelected) - 1])

    bot.send_message(c.message.chat.id, 'Added')


def parse_news():
    global newsapi
    top_headlines = newsapi.get_top_headlines(language='en', country='us', page=1)

    print(top_headlines['articles'][0])


# parse_news()


bot.polling()