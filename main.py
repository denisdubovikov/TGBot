import telebot
from newsapi import NewsApiClient
from itertools import groupby

import constants
import startmessage
import dict
import languages

PROXY = 'socks5://47.52.231.140:8080'
telebot.apihelper.proxy = {'https': 'socks5://198.27.75.152:1080'}

apiKey = constants.apiKey
botToken = constants.botToken

newsapi = NewsApiClient(api_key=apiKey)

bot = telebot.TeleBot(botToken)

categoriesSelected = []
interfaceLanguage = "gb"

ID = ''

certain_request = {'country': '', 'category': ''}
CHAT_ID = None

@bot.message_handler(commands=["start"])
def handle_start(message):
    global CHAT_ID

    CHAT_ID = message.chat.id
    startText = startmessage.text
    bot.send_message(message.chat.id, startText)

    # set_language(message)
    # present_news(None)

    offer_to_set_categories(message)
    # parse_news(q_=None, country_='ru', category_='science')


@bot.message_handler(commands=["help"])
def handle_help(message):
    helpText = "This is help message"
    bot.send_message(message.chat.id, helpText)

@bot.message_handler(commands=["setlang"])
def handle_setlang(message):
    print('21qw')
    set_language(message)


@bot.message_handler(commands=["getnews"])
def handle_getnews(message):
    getnews_keyboard(message)


def getnews_keyboard(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboardButton1 = telebot.types.InlineKeyboardButton(languages.ru_top[interfaceLanguage],
                                                         callback_data='get_Russian top')
    keyboardButton2 = telebot.types.InlineKeyboardButton(languages.fr_top[interfaceLanguage],
                                                         callback_data='get_France top')
    keyboardButton3 = telebot.types.InlineKeyboardButton(languages.us_top[interfaceLanguage],
                                                         callback_data='get_USA top')
    keyboardButton4 = telebot.types.InlineKeyboardButton(languages.apple_news[interfaceLanguage],
                                                         callback_data='get_Apple news')
    keyboardButton5 = telebot.types.InlineKeyboardButton(languages.general[interfaceLanguage],
                                                         callback_data='get_General')
    keyboardButton6 = telebot.types.InlineKeyboardButton(languages.science[interfaceLanguage],
                                                         callback_data='get_Science')
    keyboard.add(keyboardButton1, keyboardButton2, keyboardButton3, keyboardButton4, keyboardButton5, keyboardButton6)

    bot.send_message(message.chat.id, languages.choose[interfaceLanguage], reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data[0:min(4, len(c.data))] == 'get_')
def getnews(c):
    print("HERE!!!")
    bot.answer_callback_query(callback_query_id=c.id)

    parse_news(q_=dict.requests[c.data[4:len(c.data)]]['q'], country_=dict.requests[c.data[4:len(c.data)]]['country'],
               category_=dict.requests[c.data[4:len(c.data)]]['category'])


@bot.message_handler(commands=["getdetailed"])
def handle_getdetailed(message):
    getdetailed_keyboard_countries(message)


def getdetailed_keyboard_countries(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboardButton1 = telebot.types.InlineKeyboardButton(languages.russia[interfaceLanguage], callback_data='getc_ru')
    keyboardButton2 = telebot.types.InlineKeyboardButton(languages.france[interfaceLanguage], callback_data='getc_fr')
    keyboardButton3 = telebot.types.InlineKeyboardButton(languages.usa[interfaceLanguage], callback_data='getc_us')
    keyboard.add(keyboardButton1, keyboardButton2, keyboardButton3)

    bot.send_message(chat_id=message.chat.id, text=languages.choose_country[interfaceLanguage], reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data[0:min(5, len(c.data))] == 'getc_')
def getdetailed(c):
    global certain_request
    bot.answer_callback_query(callback_query_id=c.id)
    country = c.data[5:len(c.data)]
    certain_request['country'] = str(country)

    getdetailed_keyboard_categories(country=country, message=c.message)


def getdetailed_keyboard_categories(country, message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboardButton1 = telebot.types.InlineKeyboardButton(languages.general[interfaceLanguage],
                                                         callback_data='getct_general')
    keyboardButton2 = telebot.types.InlineKeyboardButton(languages.business[interfaceLanguage],
                                                         callback_data='getct_business')
    keyboardButton3 = telebot.types.InlineKeyboardButton(languages.sport[interfaceLanguage],
                                                         callback_data='getct_sports')
    keyboardButton4 = telebot.types.InlineKeyboardButton(languages.science[interfaceLanguage],
                                                         callback_data='getct_science')
    keyboard.add(keyboardButton1, keyboardButton2, keyboardButton3, keyboardButton4)

    bot.send_message(message.chat.id, languages.choose[interfaceLanguage], reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data[0:min(6, len(c.data))] == 'getct_')
def getdetailed(c):
    global certain_request
    bot.answer_callback_query(callback_query_id=c.id)
    category = c.data[6:len(c.data)]
    certain_request['category'] = str(category)

    print(category)

    parse_news(q_=None, country_=certain_request['country'], category_=certain_request['category'])


def parse_news(q_, country_, category_):
    global newsapi

    print(q_, country_, category_)

    headlines = newsapi.get_top_headlines(q=q_, country=country_, category=category_)
    print(headlines)

    present_news(headlines=headlines)


def present_news(headlines):
    global CHAT_ID

    print('HERE!!')

    if headlines['totalResults'] == 0:
        bot.send_message(chat_id=CHAT_ID, text=languages.no_news[interfaceLanguage])
        return

    print('HERE_2')

    for i in range(min(headlines['totalResults'], 5)):
        imageURL = headlines['articles'][i]['urlToImage']
        myMarkup = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton(text=headlines['articles'][i]['title'],
                                                    url=headlines['articles'][i]['url'])
        myMarkup.add(button)

        print('HERE_', i)

        print(imageURL)

        if imageURL != None:
            bot.send_photo(chat_id=CHAT_ID, photo=imageURL)

        messageText = headlines['articles'][i]['description']

        print(messageText)

        if messageText == None:
            messageText = 'No description'
        bot.send_message(chat_id=CHAT_ID, text=messageText, reply_markup=myMarkup)

        print('HERE_', i)


@bot.message_handler(commands=["getfavorites"])
def get_favorites(message):
    global categoriesSelected
    print(categoriesSelected)
    for i in range(len(categoriesSelected)):
        parse_news(dict.requests[categoriesSelected[i]]['q'], dict.requests[categoriesSelected[i]]['country'],
                   dict.requests[categoriesSelected[i]]['category'])


@bot.message_handler(commands=["favorites"])
def show_favorites(message):
    if len(categoriesSelected) == 0:
        bot.send_message(message.chat.id, text=languages.no_favorites[interfaceLanguage] +
                                               languages.use_to_edit_favorites[interfaceLanguage])
        return

    message_text = languages.your_favorites[interfaceLanguage]

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
        bot.send_message(chat_id=message.chat.id, text=languages.list_is_empty[interfaceLanguage])
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
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboardButton1 = telebot.types.InlineKeyboardButton(text='RU 🇷🇺', callback_data='ru')
    keyboardButton2 = telebot.types.InlineKeyboardButton(text='GB 🇬🇧', callback_data='gb')
    keyboard.add(keyboardButton1, keyboardButton2)

    bot.send_message(message.chat.id, languages.choose_lang[interfaceLanguage], reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data == 'ru')
def set_ru_language(c):
    global interfaceLanguage, CHAT_ID

    interfaceLanguage = 'ru'
    bot.answer_callback_query(callback_query_id=c.id, text=languages.saved[interfaceLanguage])
    bot.send_message(chat_id=CHAT_ID, text=languages.lang_set[interfaceLanguage])


@bot.callback_query_handler(func=lambda c: c.data == 'gb')
def set_en_language(c):
    global interfaceLanguage, CHAT_ID

    interfaceLanguage = 'gb'
    bot.answer_callback_query(callback_query_id=c.id, text=languages.saved[interfaceLanguage])
    bot.send_message(chat_id=CHAT_ID, text=languages.lang_set[interfaceLanguage])

def offer_to_set_categories(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboardButton1 = telebot.types.InlineKeyboardButton(languages.now[interfaceLanguage],
                                                         callback_data='setCategoriesNow')
    keyboardButton2 = telebot.types.InlineKeyboardButton(languages.later[interfaceLanguage],
                                                         callback_data='setCategoriesLater')
    keyboard.add(keyboardButton1, keyboardButton2)

    bot.send_message(message.chat.id, languages.want_to_set_favorites[interfaceLanguage], reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data == 'setCategoriesNow')
def set_categories_now(c):
    bot.answer_callback_query(callback_query_id=c.id)
    set_categories(c.message)


@bot.callback_query_handler(func=lambda c: c.data == 'setCategoriesLater')
def set_categories_later(c):
    bot.answer_callback_query(callback_query_id=c.id)
    bot.send_message(chat_id=c.message.chat.id,
                     text=languages.use_to_edit_favorites[interfaceLanguage])


def set_categories(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboardButton1 = telebot.types.InlineKeyboardButton(languages.ru_top[interfaceLanguage], callback_data='ruTop')
    keyboardButton2 = telebot.types.InlineKeyboardButton(languages.fr_top[interfaceLanguage], callback_data='frTop')
    keyboardButton3 = telebot.types.InlineKeyboardButton(languages.us_top[interfaceLanguage], callback_data='usTop')
    keyboardButton4 = telebot.types.InlineKeyboardButton(languages.apple_news[interfaceLanguage], callback_data='apTop')
    keyboardButton5 = telebot.types.InlineKeyboardButton(languages.general[interfaceLanguage], callback_data='general')
    keyboardButton6 = telebot.types.InlineKeyboardButton(languages.science[interfaceLanguage], callback_data='science')
    keyboardButtonContinue = telebot.types.InlineKeyboardButton(languages.continue_[interfaceLanguage],
                                                                callback_data='continue')
    keyboard.add(keyboardButton1, keyboardButton2, keyboardButton3, keyboardButton4, keyboardButton5, keyboardButton6,
                 keyboardButtonContinue)

    bot.send_message(message.chat.id, languages.choose[interfaceLanguage], reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data == 'ruTop')
def set_categories_now(c):
    global categoriesSelected

    bot.answer_callback_query(callback_query_id=c.id, text=languages.added[interfaceLanguage])

    # categoriesSelected.append("https://newsapi.org/v2/top-headlines?country=ru&apiKey=" + apiKey)
    categoriesSelected.append("Russian top")
    print(categoriesSelected[len(categoriesSelected) - 1])

    # bot.send_message(c.message.chat.id, 'Added')


@bot.callback_query_handler(func=lambda c: c.data == 'frTop')
def set_categories_now(c):
    global categoriesSelected

    bot.answer_callback_query(callback_query_id=c.id, text=languages.added[interfaceLanguage])

    # categoriesSelected.append("https://newsapi.org/v2/top-headlines?country=fr&apiKey=" + apiKey)
    categoriesSelected.append("France top")
    print(categoriesSelected[len(categoriesSelected) - 1])

    # bot.send_message(c.message.chat.id, 'Added')


@bot.callback_query_handler(func=lambda c: c.data == 'apTop')
def set_categories_now(c):
    global categoriesSelected

    bot.answer_callback_query(callback_query_id=c.id, text=languages.added[interfaceLanguage])

    # categoriesSelected.append("https://newsapi.org/v2/top-headlines?q=apple&apiKey=" + apiKey)
    categoriesSelected.append("Apple news")
    print(categoriesSelected[len(categoriesSelected) - 1])

    # bot.send_message(c.message.chat.id, 'Added')


@bot.callback_query_handler(func=lambda c: c.data == 'usTop')
def set_categories_now(c):
    global categoriesSelected

    bot.answer_callback_query(callback_query_id=c.id, text=languages.added[interfaceLanguage])
    categoriesSelected.append("USA top")
    print(categoriesSelected[len(categoriesSelected) - 1])


@bot.callback_query_handler(func=lambda c: c.data == 'general')
def set_categories_now(c):
    global categoriesSelected

    bot.answer_callback_query(callback_query_id=c.id, text=languages.added[interfaceLanguage])
    categoriesSelected.append("General")
    print(categoriesSelected[len(categoriesSelected) - 1])


@bot.callback_query_handler(func=lambda c: c.data == 'science')
def set_categories_now(c):
    global categoriesSelected

    bot.answer_callback_query(callback_query_id=c.id, text=languages.added[interfaceLanguage])
    categoriesSelected.append("Science")
    print(categoriesSelected[len(categoriesSelected) - 1])


@bot.callback_query_handler(func=lambda c: c.data == 'continue')
def set_categories_now(c):
    global categoriesSelected

    print('HERE!')

    bot.answer_callback_query(callback_query_id=c.id)

    categoriesSelectedSet = list(set(categoriesSelected))
    categoriesSelected = categoriesSelectedSet
    print(categoriesSelected)

    print(c.message.chat.id)

    bot.send_message(chat_id=c.message.chat.id, text=languages.favorites_saved[interfaceLanguage])

    # bot.edit_message_reply_markup(chat_id=c.message.chat.id, reply_markup=None)


# parse_news()


bot.polling()