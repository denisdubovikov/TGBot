import telebot
from newsapi import NewsApiClient
from itertools import groupby
import constants
import startmessage

# telebot.apihelper.proxy = {'':''}

apiKey = constants.apiKey
botToken = constants.botToken

newsapi = NewsApiClient(api_key=apiKey)

bot = telebot.TeleBot(botToken)

categoriesSelected = []
userLanguage = "gb"

ID = ''

@bot.message_handler(commands=["start"])
def handle_start(message):
    startText = startmessage.text
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
    print('21qw')
    set_language(message)


@bot.message_handler(commands=["favorites"])
def show_favorites(message):
    if len(categoriesSelected) == 0:
        bot.send_message(message.chat.id, text="You have no favorites")
        return

    message_text = "Your favorites:\n"

    for i in range(len(categoriesSelected)):
        message_text += str(i + 1) + ". " + str(categoriesSelected[i]) + "\n"

    bot.send_message(message.chat.id, text=message_text)


@bot.message_handler(commands=["addfavorites"])
def add_favorites(message):
    set_categories(message)


@bot.message_handler(commands=["cutfavorites"])
def cut_favorites(message):
    global categoriesSelected

    if len(categoriesSelected) == 0:
        bot.send_message(chat_id=message.chat.id, text="The list is empty")
        return

    keyboard = telebot.types.InlineKeyboardMarkup()

    for i in range(len(categoriesSelected)):
        keyboardButton = telebot.types.InlineKeyboardButton(categoriesSelected[i],
                                                            callback_data="cut_" + str(categoriesSelected[i]))
        keyboard.add(keyboardButton)
        print(categoriesSelected[i])

    bot.send_message(message.chat.id, "Choose to cut", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data[0:min(4, len(c.data))] == 'cut_')
def cut_the_category(c):
    print("HERE!!!")
    bot.answer_callback_query(callback_query_id=c.id)

    cut_the_category(c.data[4:len(c.data)])
    # bot.send_message(c.message.chat.id, 'Now pressed')
    # set_categories(c.message)


def cut_the_category(category_name):
    print(category_name)

    # global categoriesSelected

    if categoriesSelected.count(category_name):
        categoriesSelected.remove(category_name)

    print(categoriesSelected)



@bot.message_handler(content_types=["text"])
def handle_text(message):
    global categoriesSelected

    if message.text == "Cancel":
        pass

def set_language(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboardButton1 = telebot.types.KeyboardButton("ru")
    keyboardButton2 = telebot.types.KeyboardButton("us")
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


@bot.callback_query_handler(func=lambda c: c.data == 'setCategoriesLater')
def set_categories_later(c):
    bot.answer_callback_query(callback_query_id=c.id)
    bot.send_message(chat_id=c.message.chat.id,
                     text="Use /addfavorites and /cutfavorites to your list of favorites later")


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
    global categoriesSelected

    bot.answer_callback_query(callback_query_id=c.id, text='Added')

    # categoriesSelected.append("https://newsapi.org/v2/top-headlines?country=ru&apiKey=" + apiKey)
    categoriesSelected.append("Russian top")
    print(categoriesSelected[len(categoriesSelected) - 1])

    # bot.send_message(c.message.chat.id, 'Added')


@bot.callback_query_handler(func=lambda c: c.data == 'frTop')
def set_categories_now(c):
    global categoriesSelected

    bot.answer_callback_query(callback_query_id=c.id, text='Added')

    # categoriesSelected.append("https://newsapi.org/v2/top-headlines?country=fr&apiKey=" + apiKey)
    categoriesSelected.append("France top")
    print(categoriesSelected[len(categoriesSelected) - 1])

    # bot.send_message(c.message.chat.id, 'Added')


@bot.callback_query_handler(func=lambda c: c.data == 'apTop')
def set_categories_now(c):
    global categoriesSelected

    bot.answer_callback_query(callback_query_id=c.id, text='Added')

    # categoriesSelected.append("https://newsapi.org/v2/top-headlines?q=apple&apiKey=" + apiKey)
    categoriesSelected.append("Apple news")
    print(categoriesSelected[len(categoriesSelected) - 1])

    # bot.send_message(c.message.chat.id, 'Added')


@bot.callback_query_handler(func=lambda c: c.data == 'continue')
def set_categories_now(c):
    global categoriesSelected

    print('HERE!')

    bot.answer_callback_query(callback_query_id=c.id)

    categoriesSelectedSet = list(set(categoriesSelected))
    categoriesSelected = categoriesSelectedSet
    print(categoriesSelected)

    print(c.message.chat.id)

    bot.send_message(chat_id=c.message.chat.id, text='Favorites saved')

    # bot.edit_message_reply_markup(chat_id=c.message.chat.id, reply_markup=None)



def parse_news():
    global newsapi
    top_headlines = newsapi.get_top_headlines(language='en', country='us', page=1)

    print(top_headlines['articles'][0])


# parse_news()


bot.polling()