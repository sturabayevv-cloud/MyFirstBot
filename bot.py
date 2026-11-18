
import os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN topilmadi!")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📚 Rus tili", "🧮 Matematika")
    markup.add("⚽ Futbol", "🌍 Tarjimon")
    markup.add("🎮 Test")

    bot.send_message(
        message.chat.id,
        "Salom! MyFirstBot Universal 🤖\nBo‘limni tanla:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: True)
def menu(message):
    text = message.text

    if text == "📚 Rus tili":
        answer = "Привет — Salom!\nСпасибо — Rahmat!"
    elif text == "🧮 Matematika":
        answer = "25 + 15 = 40"
    elif text == "⚽ Futbol":
        answer = "⚽ FUTBOL\nBarcelona 🔵🔴\nReal Madrid ⚪"
    elif text == "🌍 Tarjimon":
        answer = "Salom = Hello = Привет"
    elif text == "🎮 Test":
        answer = "5 × 5 nechchi?\nA) 10\nB) 25\nC) 30"
    else:
        answer = "Menyudagi tugmalardan birini tanla."

    bot.send_message(message.chat.id, answer)

print("MyFirstBot ishga tushdi!")
bot.infinity_polling()

