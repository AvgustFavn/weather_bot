import telebot
from telebot import types
import requests
import json

bot_token = '6412442605:AAGjt4OYmUZjBISCZkKEzuCJFnloNV3-Nos'
weather_api_token = '57b4d5f33ee7dbb820e4a80b55838f4d'
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Я бот для просмотра погоды в городе ...")
    markup = types.InlineKeyboardMarkup()
    btn_my_site= types.InlineKeyboardButton(text='Посмотреть погоду', callback_data='weather')
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, "Нажмите на кнопку ниже, чтобы узнать погоду.", reply_markup = markup)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'weather':
        send_weather(call.message)

def send_weather(message):
    city = 'Moscow'  # Замените на нужный город
    r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_token}')
    data = json.loads(r.text)
    weather = data['weather'][0]['description']
    wind_speed = data['wind']['speed']
    bot.reply_to(message, f'Погода в {city}: {weather}, скорость ветра: {wind_speed} м/с')

bot.polling()
