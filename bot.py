import requests
import os
import time
from telegram import Bot

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

bot = Bot(token=TOKEN)

def send_message():
    bot.send_message(chat_id=CHAT_ID, text="🤖 Bot online com sucesso!")

while True:
    send_message()
    time.sleep(300)
