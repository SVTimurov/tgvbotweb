import telebot
import requests
import json
import os
from dotenv import load_dotenv  # Подключаем dotenv для работы с .env

# Загружаем переменные окружения из .env (если локально) или из Railway
load_dotenv()

TOKEN = os.getenv("TOKEN")  # Берем токен из переменной окружения
API = os.getenv("API")  # Берем API-ключ из переменной окружения

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Приветствую! Введите название своего города для прогноза погоды.")

@bot.message_handler(commands=['autor'])
def autor(message):
    bot.send_message(message.chat.id, "Автор: Тимур Метелица\nСоздан для демонстрации возможностей на 'Kabanchik'.")

@bot.message_handler(content_types=['text'])
def weather(message):
    # Проверяем, чтобы текст не был командой
    if message.text.startswith("/"):
        return

    City = message.text.strip().lower()
    url = f"https://api.openweathermap.org/data/2.5/weather?q={City}&appid={API}&units=metric"

    try:
        res = requests.get(url)
        data = res.json()

        if res.status_code == 200:
            temp = data["main"]["temp"]
            weather_desc = data["weather"][0]["description"].capitalize()
            bot.reply_to(message, f"🌤 Погода в {City.capitalize()}:\nТемпература: {temp}°C\nОписание: {weather_desc}")
        else:
            bot.reply_to(message, "Ошибка! Введите корректное название города.")

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

# Запускаем бота
bot.polling(none_stop=True)
