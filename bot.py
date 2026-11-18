
import os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

questions = [
    ("Salom rus tilida qanday?", ["Привет", "Спасибо", "Пока", "Да"], 0),
    ("Rahmat rus tilida qanday?", ["Нет", "Спасибо", "Дом", "Да"], 1),
    ("Kitob rus tilida qanday?", ["Стол", "Книга", "Вода", "Мама"], 1),
    ("Ona rus tilida qanday?", ["Папа", "Брат", "Мама", "Сестра"], 2),
    ("Ota rus tilida qanday?", ["Мама", "Папа", "Друг", "Дом"], 1),
    ("Suv rus tilida qanday?", ["Вода", "Хлеб", "Книга", "Школа"], 0),
    ("Maktab rus tilida qanday?", ["Дом", "Школа", "Стол", "Окно"], 1),
    ("Do‘st rus tilida qanday?", ["Друг", "Мама", "Папа", "Кот"], 0),
    ("Ha rus tilida qanday?", ["Нет", "Да", "Пока", "Привет"], 1),
    ("Yo‘q rus tilida qanday?", ["Да", "Спасибо", "Нет", "Дом"], 2),
    ("Non rus tilida qanday?", ["Хлеб", "Вода", "Стол", "Мяч"], 0),
    ("Mushuk rus tilida qanday?", ["Собака", "Кот", "Дом", "Друг"], 1),
    ("It rus tilida qanday?", ["Кот", "Мама", "Собака", "Вода"], 2),
    ("Xayr rus tilida qanday?", ["Пока", "Привет", "Да", "Нет"], 0),
    ("Uy rus tilida qanday?", ["Школа", "Дом", "Книга", "Хлеб"], 1),
    ("Opa-singil rus tilida qanday?", ["Брат", "Сестра", "Папа", "Друг"], 1)
]

user_data = {}

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

@bot.message_handler(func=lambda m: m.text == "🎮 Test")
def start_test(message):
    user_data[message.chat.id] = {"q": 0, "score": 0}
    send_question(message.chat.id)

def send_question(chat_id):
    data = user_data[chat_id]
    q = data["q"]

    question, options, correct = questions[q]

    markup = types.InlineKeyboardMarkup()

    for i, option in enumerate(options):
        markup.add(types.InlineKeyboardButton(
            f"{chr(65+i)}) {option}",
            callback_data=str(i)
        ))

    bot.send_message(
        chat_id,
        f"📚 Savol {q+1}/16\n\n{question}",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def check_answer(call):
    chat_id = call.message.chat.id

    if chat_id not in user_data:
        bot.answer_callback_query(call.id, "Avval testni boshlang!")
        return

    data = user_data[chat_id]
    q = data["q"]

    if data.get("answered", False):
        bot.answer_callback_query(call.id, "Bu savolga javob berilgan!")
        return

    correct = questions[q][2]
    selected = int(call.data)

    data["answered"] = True

    if selected == correct:
        data["score"] += 1
        result = "✅ To‘g‘ri!"
    else:
        result = "❌ Noto‘g‘ri!"

    bot.answer_callback_query(call.id, result)
    bot.send_message(chat_id, result)

    data["q"] += 1
    data["answered"] = False

    if data["q"] < len(questions):
        send_question(chat_id)
    else:
        score = data["score"]
        bot.send_message(
            chat_id,
            f"🏆 TEST YAKUNLANDI!\n\n"
            f"Natijang: {score}/16\n"
            f"Foiz: {score/16*100:.0f}%"
        )
        del user_data[chat_id]

@bot.message_handler(func=lambda m: True)
def menu(message):
    if message.text == "📚 Rus tili":
        answer = "Привет — Salom!\nСпасибо — Rahmat!"
    elif message.text == "🧮 Matematika":
        answer = "25 + 15 = 40"
    elif message.text == "⚽ Futbol":
        answer = "⚽ Barcelona 🔵🔴\nReal Madrid ⚪"
    elif message.text == "🌍 Tarjimon":
        answer = "Salom = Hello = Привет"
    else:
        answer = "Menyudagi tugmalardan birini tanla."

    bot.send_message(message.chat.id, answer)

print("MyFirstBot ishga tushdi!")
bot.infinity_polling()
