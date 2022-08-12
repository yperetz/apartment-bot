import os
import telebot
from threading import Thread
import asyncio
from dotenv import load_dotenv
from secrets import token_urlsafe
import schedule

users = []
tokens = []

if load_dotenv():
    API_KEY = os.getenv('TG_BOT_API_KEY')
else:
    exit(1)
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    token = token_urlsafe(8)
    while token not in tokens:
        token = token_urlsafe(8)
        users.append({'id': message.chat.id, "token": token})
        tokens.append(token)
        # bot.reply_to(message, token)
        bot.reply_to(message, f"""\
    The Token is {token, users}\
""")

        # Handle all other messages with content_type 'text' (content_types defaults to ['text'])


@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)


@bot.message_handler(commands=['Greet'])
def greet(message):
    bot.reply_to(message, "yo")


def echoAll():
    for user in users:
        bot.send_message(chat_id=user["id"],
                         text=f"started +{user['token']}")


def schedule_checker():
    while True:
        schedule.run_pending()
        asyncio.sleep(1)


def start_polling():
    asyncio.run(bot.polling())


schedule.every(15).seconds.do(echoAll)
Thread(target=start_polling).start()
asyncio.sleep(2)
Thread(target=schedule_checker).start()
