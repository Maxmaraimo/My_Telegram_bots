import webbrowser
from telebot import types
import telebot
import requests
import json
from requests import *
from telegram.ext import *
# from forex_python.converter import CurrencyConverter

bot = telebot.TeleBot('6384874766:AAF-hEg_DPpCiF8AKosTu0C94_Bv-l7zUQE')
API = '4ed218357d9c16888596f3b54e587aac'








@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Go to website', url='https://dan.com/buy-domain/4k.photo?redirected=true')
    btn2 = types.InlineKeyboardButton('Delete foto', callback_data='delete')
    markup.row(btn1, btn2)

    bot.reply_to(message, 'What a beautiful photo', reply_markup=markup)



@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://itproger.com')


@bot.message_handler(commands=['start','main','hello'])
def main(message):
    bot.send_message(message.chat.id, f'Hello!, MR. {message.from_user.first_name} write /help')



@bot.message_handler(commands=['searchjop'])
def main(messages):
    bot.send_message(messages.chat.id, '<b>Search</b> <em><u>jop</u></em>', parse_mode='html')
    markup = types.InlineKeyboardMarkup()
    btn11 = types.InlineKeyboardButton('Search for a jop online', url='https://www.upwork.com')
    btn22 = types.InlineKeyboardButton('Programming lessons', url='https://itproger.com')
    # btn33 = types.InlineKeyboardButton('What is happened UPWORK', callback_data='saa')
    markup.row(btn11, btn22)
    bot.reply_to(messages,  '<b>Search</b> <em><u>jop</u></em>', parse_mode='html', reply_markup=markup)



@bot.message_handler(commands=['help'])
def main(messages):
    bot.send_message(messages.chat.id, """
/start   - Start the bot
/help    - Help
/searchjop - he can search jop online
/photo - you send photo he said
/weather - search weather 
/sum - summa
id - your ID 
                     
""")



@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Hello!, {message.from_user.first_name} ')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID {message.from_user.id}')




currency = 1
amount = 0

@bot.message_handler(commands=['sum'])
def sum(message):
    bot.send_message(message.chat.id, 'Привет, введите сумму')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Введите сумму')
        bot.register_next_step_handler(message, summa)
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn99 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
    btn88 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
    btn77 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
    btn66 = types.InlineKeyboardButton('Другое значение', callback_data='else')

    markup.add(btn99, btn88, btn77, btn66)
    bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    values = call.data.upper().split('/')
    res = currency.convert(amount, values[0], values[1])
    bot.send_message(call.message.chat.id, f'Получается: {res}. Можете писать снова.')
    bot.register_next_step_handler(call.message, summa)





@bot.message_handler(commands=['weather'])
def weather(message):
    bot.send_message(message.chat.id, 'Привет! Рад тебя видеть. Напиши название города.')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    data = res.json()
    temperature = data['main']['temp']
    bot.reply_to(message, f'Сейчас погода: {temperature}°C')



bot.polling()
















    

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)









bot.polling(none_stop=True)