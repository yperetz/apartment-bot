import os
import pickle

import telebot
from threading import Thread
from dotenv import load_dotenv
from secrets import token_urlsafe
import schedule
import time
from Yad2Scraper import get_aps

from telebot.types import MessageEntity

users = []
tokens = []

if load_dotenv():
    API_KEY = os.getenv('TG_BOT_API_KEY')
else:
    exit(1)
bot = telebot.TeleBot(API_KEY)
AP_URL = 'https://www.yad2.co.il/item/'
IMG_NOT_FOUND = 'https://bitsofco.de/content/images/2018/12/broken-1.png'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    token = token_urlsafe(8)
    while token not in tokens:
        token = token_urlsafe(8)
        users.append({'id': message.chat.id, "token": token})
        tokens.append(token)
        # bot.reply_to(message, token)
    bot.reply_to(message, f"The Token is {token, users}")

    # Handle all other messages with content_type 'text' (content_types defaults to ['text'])


@bot.message_handler(commands=['apartments'])
def get_apartments(message):
    msg = bot.reply_to(message, "Started looking for apartments")
    try:
        aps = get_aps()
    except Exception as e:
        bot.reply_to(msg, "Failed")
        print(e)
        return
    pickle.dump(aps, open("aps.p", "wb"))
    for city in aps:
        for nhood in city["nhoods"]:
            for ap in nhood["apartments"]:
                if ap['img_url'] is not None:
                    imgurl = ap['img_url']
                else:
                    imgurl = IMG_NOT_FOUND
                cap = ap["name"] + f' - {nhood["name"]}\n' + ap[
                    "subtitle"] + '\n' + ap[
                          "rooms"] + " " + "חדרים" + "   |" + "   קומה " + ap[
                          "floor"] + "    |    " + ap['area'] + "  מ\"ר"
                try:
                    bot.send_photo(chat_id=message.chat.id, photo=imgurl,
                                   caption=cap, caption_entities=[
                            MessageEntity(length=len(ap["name"]), offset=0,
                                          type='text_link',
                                          url=AP_URL + ap['id'])])
                except:
                    bot.send_photo(chat_id=message.chat.id, photo=IMG_NOT_FOUND,
                                   caption=cap, caption_entities=[
                            MessageEntity(length=len(ap["name"]), offset=0,
                                          type='text_link',
                                          url=AP_URL + ap['id'])])
                time.sleep(2)


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
        time.sleep(1)


def start_polling():
    bot.polling()


schedule.every().day.at('08:00').do(echoAll)
Thread(target=start_polling).start()
time.sleep(2)
Thread(target=schedule_checker).start()
