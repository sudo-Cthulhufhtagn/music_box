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
    bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # global rospack
    
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
    elif message.text.lower() == 'cl':
        soundhandle.playWave(to_files + "/audio/Clear.ogg")
        sleep(2)
    elif message.text.lower() == 'mv':
        soundhandle.playWave(to_files + "/audio/Moving.ogg")
        sleep(2)
    elif message.text.lower() == 'f':
        soundhandle.playWave(to_files + "/audio/Engaging.ogg")
        sleep(2)
        twist_msg = Twist()
        twist_msg.linerar.x=1
        cmd_vel_pub.publish(twist_msg)
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')
        soundhandle.playWave(to_files + "/audio/Area_denied.ogg")
        sleep(2)

if __name__ == '__main__':
    rospy.init_node('telegram_bot', anonymous = True)
    soundhandle = SoundClient()
    global cmd_vel_pub
	cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    t = rospy.Timer(rospy.Duration(0.1), timer_callback)
    rospy.sleep(1)

    soundhandle.stopAll()
    global rospack
    rospack = rospkg.RosPack()
    to_files=rospack.get_path('music_box')

    rospy.loginfo('Attempt 1')
    soundhandle.playWave(to_files + "/audio/Rolling_out.ogg")
    sleep(2)
    bot.polling()

