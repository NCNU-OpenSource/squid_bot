import configparser
import logging
import time
import telegram
# from flask import Flask, request
from telegram.ext import Dispatcher, MessageHandler, Filters, Updater, CommandHandler, CallbackContext
from telegram import ReplyKeyboardMarkup, KeyboardButton
from PIL import Image
import json
import urllib.request
from Identify import GoIdentify
from Identify import CNN_Model
import torch.nn as nn
from torchvision import models

# 載入 config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# 從 config 取得 token
token=(config['TELEGRAM']['ACCESS_TOKEN'])
bot = telegram.Bot(token)
updater = Updater(token, use_context = True)

# 允許 logging。當出現error時能知道哪裡出了問題。
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start_handler(update, context: CallbackContext):
    # reply_markup = ReplyKeyboardMarkup([[
    #     KeyboardButton("/about"),
    #     KeyboardButton("/help")],
    #     [KeyboardButton("/start")]])
    # bot.sendMessage(chat_id=-1, text='選項如下:', reply_markup=reply_markup)
    # chatbot在接受用戶輸入/start後的output內容
    bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING) # 會顯示chatbot正在輸入中，增加對話真實感
    time.sleep(0.5) # 在顯示輸入中後停頓1秒，然後顯示下一句code的文字
    update.message.reply_text("Hello! 你好👋，{}！ 我是 Squid🤖".format(update.message.from_user.first_name)) # 給user的output
    bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
    time.sleep(0.5)
    update.message.reply_text("Squid🤖能根據您傳入的圖片辨識是魷魚、章魚、花枝的哪一個。\n\n關於使用方法，請輸入 /help \n") # 給user的output。output可以分開多次使用update.message.reply_text()。
    # reply_markup = ReplyKeyboardMarkup([[KeyboardButton("/about")]
    #     , [KeyboardButton("/record"), KeyboardButton("/end")]
    #     , [KeyboardButton("/get"), KeyboardButton("/help")]])
    # bot.sendMessage(chat_id=update.message.chat_id, text="指令如下", reply_markup=reply_markup)

def img_handler(update, context: CallbackContext):
    """Reply message."""
    photo_id = update.message.photo[0].file_id
    url = "https://api.telegram.org/bot{}/getFile?file_id={}".format(token, photo_id)
    _response = urllib.request.urlopen(url)
    photo_json = json.loads(_response.read())
    file_path = photo_json['result']['file_path']
    print(photo_json['result']['file_path'])
    img_path = "https://api.telegram.org/file/bot{}/{}".format(token, file_path)
    variety = GoIdentify(img_path)
    # img = Image.open(urllib.request.urlopen(img_path))
    # img.show()

    # text = update.message.text
    # if (text != "/start") or (text != "/help") or (text != "/about") or (text != "/suwen"):
    bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
    time.sleep(0.5)
    update.message.reply_text("此圖是：{}".format(variety))

def reply_handler(update, context: CallbackContext):
    """Reply message."""
    text = update.message.text
    if (text != "/start") or (text != "/help"):
        bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
        time.sleep(0.5)
        update.message.reply_text("對不起，Squid🤖不能理解你說啥。🤔\n\n關於使用方法，請輸入 /help")

def help_handler(update, context: CallbackContext):
    # chatbot在接受用戶輸入/start後的output內容
    bot.send_chat_action(chat_id = update.message.chat_id, action = telegram.ChatAction.TYPING)
    time.sleep(0.5)
    update.message.reply_text("《🔍如何使用》\nSquid BOT 會辨識花枝、章魚、魷魚的照片\n請傳送一張照片給 Squid BOT\nSquid BOT 會根據您的照片回答您是哪個物種。") 

def main():
    # 設定使用dispatcher，用來以後設定command和回覆用
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_handler)) # 啟動chatbot
    dp.add_handler(CommandHandler("help", help_handler)) # 顯示幫助的command
    dp.add_handler(MessageHandler(Filters.photo, img_handler)) # 設定接受到圖片會做的事
    dp.add_handler(MessageHandler(Filters.text, reply_handler)) # 設定若非設定command會回覆用戶不知道說啥的訊息
    updater.start_polling()
    # 啟動Bot。bot程式與Telegram連結有兩種方式：polling和webhook。
    # 兩者的差異可以參考這篇reddit的解釋：https://www.reddit.com/r/TelegramBots/comments/525s40/q_polling_vs_webhook/。
    # 在python-telegram-bot裡面本身有built-in的webhook方法，但是在GCE中暫時還沒摸索到如何設定webhook，因此polling是最便捷的方法。
    updater.start_polling()
    # 就是讓程式一直跑。
    # 按照package的說法“start_polling() is non-blocking and will stop the bot gracefully.”。
    # 若要停止按Ctrl-C 就好
    updater.idle()

#運行main()，就會啟動bot。
if __name__ == '__main__':
    main()