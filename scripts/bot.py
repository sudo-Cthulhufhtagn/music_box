#!/usr/bin/env python3
import rospy, os, sys, rospkg, telebot, signal
from sound_play.msg import SoundRequest
from geometry_msgs.msg import Twist
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
bot = telebot.TeleBot('')

from sound_play.libsoundplay import SoundClient
speed_mult=1
ang_speed_mult=1

def sleep(t):
    try:
        rospy.sleep(t)
    except:
        pass

def gen_markup():
    markup = ReplyKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("↪️"),
    InlineKeyboardButton("↩️"))
    markup.add(InlineKeyboardButton("↖️", callback_data="tl"),
    InlineKeyboardButton("⬆️", callback_data="tt"),
    InlineKeyboardButton("↗️", callback_data="tr"),row_width=3)
    markup.add(InlineKeyboardButton("⬅️", callback_data="cl"),
    InlineKeyboardButton("⏹", callback_data="cc"),
    InlineKeyboardButton("➡️", callback_data="cr"))
    markup.add(InlineKeyboardButton("↙️", callback_data="bl"),
    InlineKeyboardButton("⬇️", callback_data="bb"),
    InlineKeyboardButton("↘️", callback_data="br"))
    return markup

def gen_markup2():
    markup = ReplyKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("speed-10%"),
    InlineKeyboardButton("⏺"),
    InlineKeyboardButton("speed+10%"))
    markup.add(InlineKeyboardButton("ang speed-10%"),
    InlineKeyboardButton("ang speed+10%"))
    return markup

def gen_markup1():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("↖️", callback_data="tl"),
    InlineKeyboardButton("⬆️", callback_data="tt"),
    InlineKeyboardButton("↗️", callback_data="tr"),row_width=3)
    markup.add(InlineKeyboardButton("⬅️", callback_data="cl"),
    InlineKeyboardButton("⏹", callback_data="cc"),
    InlineKeyboardButton("➡️", callback_data="cr"))
    markup.add(InlineKeyboardButton("↙️", callback_data="bl"),
    InlineKeyboardButton("⬇️", callback_data="bb"),
    InlineKeyboardButton("↘️", callback_data="br"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    twist_msg = Twist()
    # global cmd_vel_pub
    if call.data == "tl":
        twist_msg.linear.x=1
        twist_msg.linear.y=1
        cmd_vel_pub.publish(twist_msg)
        # bot.answer_callback_query(call.id, "tl")
    elif call.data == "tt":
        twist_msg.linear.x=1
        twist_msg.linear.y=0
        cmd_vel_pub.publish(twist_msg)
        # bot.answer_callback_query(call.id, "tt")
    elif call.data == "tr":
        twist_msg.linear.x=1
        twist_msg.linear.y=-1
        cmd_vel_pub.publish(twist_msg)
    elif call.data == "cl":
        twist_msg.linear.y=1
        cmd_vel_pub.publish(twist_msg)
    elif call.data == "cc":
        twist_msg.linear.y=0
        twist_msg.linear.x=0
        cmd_vel_pub.publish(twist_msg)
    elif call.data == "cr":
        twist_msg.linear.y=-1
        twist_msg.linear.x=0
        cmd_vel_pub.publish(twist_msg)
    elif call.data == "bl":
        twist_msg.linear.y=1
        twist_msg.linear.x=-1
        cmd_vel_pub.publish(twist_msg)
    elif call.data == "bb":
        twist_msg.linear.y=0
        twist_msg.linear.x=-1
        cmd_vel_pub.publish(twist_msg)
    elif call.data == "br":
        twist_msg.linear.y=-1
        twist_msg.linear.x=-1
        cmd_vel_pub.publish(twist_msg)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'I am remote controller for robotont. Welcome {message.from_user.first_name}!')

def timer_callback(event):
	global last_heartbeat
	if (rospy.get_time() - last_heartbeat) >= 0.5:
		cmd_vel_pub.publish(Twist())

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    twist_msg = Twist()
    global ang_speed_mult, speed_mult, last_heartbeat
    last_heartbeat = rospy.get_time()
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
    elif message.text.lower() == 'cl':
        soundhandle.playWave(to_files + "/audio/Clear.ogg")
        sleep(2)
    elif message.text.lower() == 'mv':
        soundhandle.playWave(to_files + "/audio/Moving.ogg")
        sleep(2)
    elif message.text.lower() == 'rm':
        soundhandle.playWave(to_files + "/audio/Erasing_previous_thirty_seconds_from_memory.ogg")
        sleep(2)
    elif message.text.lower() == 'f':
        soundhandle.playWave(to_files + "/audio/Engaging.ogg")
        twist_msg = Twist()
        twist_msg.linear.x=1
        cmd_vel_pub.publish(twist_msg)
    elif message.text.lower() == '/keyboard' or message.text == '⏺':
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "Robot control", reply_markup=gen_markup())
    elif message.text.lower() == '/keyboard_1':
        bot.send_message(message.chat.id, "Robot control", reply_markup=gen_markup1())
    elif message.text.lower() == 'd':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Привет', 'Пока')
        # bot.send_message(message.chat.id, 'Привет!', reply_markup=keyboard)
    elif message.text.lower() == '↖️':
        bot.delete_message(message.chat.id, message.message_id)
        twist_msg.linear.x=1*speed_mult
        twist_msg.linear.y=1*speed_mult
        cmd_vel_pub.publish(twist_msg)
        # bot.answer_callback_query(call.id, "tl")
    elif message.text.lower() ==  "⬆️":
        bot.delete_message(message.chat.id, message.message_id)
        twist_msg.linear.x=1*speed_mult
        twist_msg.linear.y=0*speed_mult
        cmd_vel_pub.publish(twist_msg)
        # bot.answer_callback_query(call.id, "tt") ↖️
    elif message.text ==  "↗️":
        bot.delete_message(message.chat.id, message.message_id)
        twist_msg.linear.x=1*speed_mult
        twist_msg.linear.y=-1*speed_mult
        cmd_vel_pub.publish(twist_msg)
    elif message.text ==  "⬅️":
        bot.delete_message(message.chat.id, message.message_id)
        twist_msg.linear.y=1*speed_mult
        cmd_vel_pub.publish(twist_msg)
    elif message.text ==  "⏹": 
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "Turn left/right", reply_markup=gen_markup2())
        twist_msg.linear.y=0*speed_mult
        twist_msg.linear.x=0*speed_mult
        cmd_vel_pub.publish(twist_msg)
    elif message.text ==  "➡️":
        bot.delete_message(message.chat.id, message.message_id)
        twist_msg.linear.y=-1*speed_mult
        twist_msg.linear.x=0*speed_mult
        cmd_vel_pub.publish(twist_msg)
    elif message.text ==  "↙️":
        bot.delete_message(message.chat.id, message.message_id)
        twist_msg.linear.y=1*speed_mult
        twist_msg.linear.x=-1*speed_mult
        cmd_vel_pub.publish(twist_msg)
    elif message.text == "⬇️":
        bot.delete_message(message.chat.id, message.message_id)
        twist_msg.linear.y=0*speed_mult
        twist_msg.linear.x=-1*speed_mult
        cmd_vel_pub.publish(twist_msg)
    elif message.text == "↘️":
        bot.delete_message(message.chat.id, message.message_id)
        twist_msg.linear.y=-1*speed_mult
        twist_msg.linear.x=-1*speed_mult
        cmd_vel_pub.publish(twist_msg)
    elif message.text == "↪️":
        bot.delete_message(message.chat.id, message.message_id)
        twist_msg.angular.z=1*ang_speed_mult
        cmd_vel_pub.publish(twist_msg)
    elif message.text == "↩️":
        bot.delete_message(message.chat.id, message.message_id)
        twist_msg.angular.z=-1*ang_speed_mult
        cmd_vel_pub.publish(twist_msg)
    elif message.text == "ang speed+10%":
        bot.delete_message(message.chat.id, message.message_id)
        ang_speed_mult= ang_speed_mult*1.1 if ang_speed_mult*1.1<1.57 else 1.57
        bot.send_message(message.chat.id, f"Ang speed: {ang_speed_mult}")
    elif message.text == "ang speed-10%":
        bot.delete_message(message.chat.id, message.message_id)
        ang_speed_mult*=0.9
    elif message.text == "speed+10%":
        bot.delete_message(message.chat.id, message.message_id)
        speed_mult= speed_mult*1.1 if speed_mult*1.1<3 else 3
        bot.send_message(message.chat.id, f"Speed: {speed_mult}")
    elif message.text == "speed-10%":
        bot.delete_message(message.chat.id, message.message_id)
        speed_mult*=0.9
    elif message.text == "kys":
        signal_handler()
    else:
        bot.send_message(message.from_user.id, 'Command not recognized')
        soundhandle.playWave(to_files + "/audio/Area_denied.ogg")
        sleep(2)

def signal_handler():
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    rospy.init_node('telegram_bot', anonymous = True)
    soundhandle = SoundClient()
    global cmd_vel_pub
    cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    global last_heartbeat
    last_heartbeat = rospy.get_time()
    t = rospy.Timer(rospy.Duration(0.5), timer_callback)
    rospy.sleep(1)

    soundhandle.stopAll()
    global rospack
    rospack = rospkg.RosPack()
    to_files=rospack.get_path('music_box')


    # rospy.loginfo('Attempt 1')
    # soundhandle.playWave(to_files + "/audio/Rolling_out.ogg")
    # sleep(2)
    bot.polling()

