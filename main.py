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



@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Here are the available commands:',
                     parse_mode='markdown')
    bot.send_message(message.chat.id, '/start - start the bot')
    bot.send_message(message.chat.id, '/help - get help')
    bot.send_message(message.chat.id, '/searchjop - search for a job online')
    bot.send_message(message.chat.id, '/photo - send a photo')
    bot.send_message(message.chat.id, '/weather - get the weather forecast')
    bot.send_message(message.chat.id, '/sum - calculate the sum of two numbers')



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




@bot.message_handler(commands=['start', 'main', 'hello'])
def welcome(message):
    bot.send_message(message.chat.id, f'Welcome, {message.from_user.first_name}! Type /help to see the available commands.')



@bot.message_handler(commands=['searchjob'])
def search_job(message):
    bot.send_message(message.chat.id, 'Let me help you find a job!')
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Search for a job online', url='https://www.upwork.com')
    btn2 = types.InlineKeyboardButton('Programming lessons', url='https://itproger.com')
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, 'What kind of job are you looking for?', reply_markup=markup)


@bot.message_handler(commands=['sum'])
def sum(message):
    bot.send_message(message.chat.id, 'Enter the first number:', parse_mode='markdown')
    bot.register_next_step_handler(message, get_first_number)

def get_first_number(message):
    try:
        first_number = int(message.text)
        bot.send_message(message.chat.id, 'Enter the second number:', parse_mode='markdown')
        bot.register_next_step_handler(message, calculate_sum, first_number)
    except ValueError:
        bot.send_message(message.chat.id, 'Invalid input. Please enter a valid number.')

def calculate_sum(message, first_number):
    try:
        second_number = int(message.text)
        total = first_number + second_number
        bot.send_message(message.chat.id, f'The sum is {total}')
    except ValueError:
        bot.send_message(message.chat.id, 'Invalid input. Please enter a valid number.')



@bot.message_handler(commands=['weather'])
def weather(message):
    bot.send_message(message.chat.id, 'Привет! Рад тебя видеть. Напиши название города.')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    try:
        city = message.text.strip().lower()
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')

        if res.status_code == 200:
            data = res.json()
            temperature = data['main']['temp']
            bot.reply_to(message, f'Сейчас погода: {temperature}°C')
        else:
            bot.reply_to(message, 'Не удалось получить данные о погоде')
    except Exception as e:
        bot.reply_to(message, 'Произошла ошибка при получении данных о погоде')







@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Welcome!, {message.from_user.first_name} ')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID {message.from_user.id}')





    

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)


bot.polling(none_stop=True)