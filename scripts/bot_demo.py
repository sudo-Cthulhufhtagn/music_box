#!/usr/bin/env python
import rospy, os, sys, rospkg, telebot
from sound_play.msg import SoundRequest
bot = telebot.TeleBot('1763023661:AAHtQBxpg0QGWIN-a4G67IhRY9Yx5intVz8')

from sound_play.libsoundplay import SoundClient

def sleep(t):
    try:
        rospy.sleep(t)
    except:
        pass

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Nice to meet you, {message.from_user.first_name}')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'hello':
        bot.send_message(message.from_user.id, 'Hi!')
    else:
        bot.send_message(message.from_user.id, "What's that")

# if __name__ == '__main__':

bot.polling(none_stop=True)
