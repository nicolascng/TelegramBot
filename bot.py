#!/usr/bin/python3

import os
from dotenv import load_dotenv
import telebot

load_dotenv()

API_KEY = str(os.getenv('API_KEY'))
PASSWORD = str(os.getenv('PASSWORD'))
SUDO_PASSWORD = str(os.getenv('SUDO_PASSWORD'))
DISPLAY = str(os.getenv('DISPLAY'))
DBUS = str(os.getenv('DBUS_SESSION_BUS_ADDRESS'))
VOICE_ES = str(os.getenv('VOICE_ES', 'es'))
VOICE_EN = str(os.getenv('VOICE_EN', 'en'))
authorized = []

bot = telebot.TeleBot(API_KEY)



@bot.message_handler(commands=['menu','help'])
def menu(message):
    if message.chat.id in authorized:
        help = open("help","r").read()
        bot.reply_to(message, help)
    else:
        bot.reply_to(message, "Just say hi")

# @bot.message_handler(content_types=['audio'])
# def handle_audio(message):
#     bot.reply_to(message, "Nice audio!")




@bot.message_handler()
def process_message(message):

    print("Message: " + str(message))
    print(str(message.content_type))

    this_chat_id = message.chat.id
    try:
        if message.text.lower() == "hi":
            if this_chat_id in authorized:
                username = str(os.popen("whoami 2>&1").read())
                bot.send_message(this_chat_id, "Hi "+username)
            else:
                bot.send_message(this_chat_id, "Hi there")
            return
        elif message.text.lower().startswith("id "):
            if remove_prefix(message.text, "id ") == PASSWORD:
                authorized.append(this_chat_id)
                register_chat_id(str(this_chat_id))
                bot.send_message(this_chat_id, "Authorized")
                return
        elif message.text.lower() in ["exit", "quit", "logout"]:
            authorized.clear()
            register_chat_id(str(0))
            bot.reply_to(message, "Logged out.")

        elif message.text.lower() in ["reset", "restart"]:
            authorized.clear()
            bot.reply_to(message, "Restarting bot.")
            bot.stop_polling()

        elif this_chat_id in authorized:
            if message.text.lower().startswith("sudo "):
                if SUDO_PASSWORD is None:
                    bot.reply_to(message, "SUDO_PASSWORD is not set.")
                    return
                response = str(os.popen("echo "+SUDO_PASSWORD+" | sudo -S -p \"\" "+remove_prefix(message.text, "sudo ")+' 2>&1').read())
                if not response:
                    response = "Done."
                bot.reply_to(message, response)
            elif message.text.lower() in ["reboot"]:
                if SUDO_PASSWORD is None:
                    bot.reply_to(message, "SUDO_PASSWORD is not set.")
                    return
                response = str(os.popen("echo "+SUDO_PASSWORD+" | sudo -S -p '' shutdown -r now 2>&1").read())
                if not response:
                    response = "Done."
                bot.reply_to(message, response)
            elif message.text.lower() in ["shutdown"]:
                if SUDO_PASSWORD is None:
                    bot.reply_to(message, "SUDO_PASSWORD is not set.")
                    return
                response = str(os.popen("echo "+SUDO_PASSWORD+" | sudo -S -p '' shutdown now 2>&1").read())
                if not response:
                    response = "Done."
                bot.reply_to(message, response)
            elif message.text.lower() in ["lock"]:
                if SUDO_PASSWORD is None:
                    bot.reply_to(message, "SUDO_PASSWORD is not set.")
                    return
                response = str(os.popen("echo "+SUDO_PASSWORD+" | sudo -S -p '' loginctl lock-sessions 2>&1").read())
                if not response:
                    response = "Done."
                bot.reply_to(message, response)
            elif message.text.lower() in ["unlock"]:
                if SUDO_PASSWORD is None:
                    bot.reply_to(message, "SUDO_PASSWORD is not set.")
                    return
                response = str(os.popen("echo "+SUDO_PASSWORD+" | sudo -S -p '' loginctl unlock-sessions 2>&1").read())
                if not response:
                    response = "Done."
                bot.reply_to(message, response)
            elif message.text.lower().startswith("sys "):
                response = str(os.popen(remove_prefix(message.text, "sys ")+" 2>&1").read())
                if not response:
                    response = "Done."
                bot.reply_to(message, response)
            elif message.text.lower().startswith("notify "):
                if DBUS == "None":
                    bot.reply_to(message, "DBUS_SESSION_BUS_ADDRESS is not set.")
                else:
                    response = str(os.popen('notify-send "'+remove_prefix(message.text, "notify ")+'" 2>&1').read())
                    if not response:
                        response = "Done."
                    bot.reply_to(message, response)
            elif message.text.lower().startswith("decir "):
                # Needs espeak with mbrola spanish voices
                if not (DBUS == "None"):
                    str(os.popen('notify-send "'+remove_prefix(message.text, "decir ")+'" 2>&1').read())
                if DISPLAY == "None":
                    bot.reply_to(message, "DISPLAY is not set.")
                response = str(os.popen('espeak "'+remove_prefix(message.text, "decir ")+'" -v '+VOICE_ES+' -p 45 -s 160 2>&1').read())
                if not response:
                    response = "Done."
                bot.reply_to(message, response)
            elif message.text.lower().startswith("say "):
                # Needs espeak with mbrola spanish voices
                if not (DBUS == "None"):
                    str(os.popen('notify-send "'+remove_prefix(message.text, "say ")+'" 2>&1').read())
                if DISPLAY is None:
                    bot.reply_to(message, "DISPLAY is not set.")
                response = str(os.popen('espeak "'+remove_prefix(message.text, "say ")+'" -v '+VOICE_EN+' -p 45 -s 160 2>&1').read())
                if not response:
                    response = "Done."
                bot.reply_to(message, response)
            elif message.text.lower() in ["picture","photo","foto"]:
                # Needs espeak with mbrola spanish voices
                try:
                    if DISPLAY is None:
                        bot.reply_to(message, "DISPLAY is not set.")
                    response = str(os.popen('rm foto0*.jpeg').read())
                    response = str(os.popen('streamer -t 4 -r 2 -o foto00.jpeg').read())
                    photo = open("foto03.jpeg", "rb")
                    bot.send_photo(this_chat_id, photo)
                    if not response:
                        response = "Done."
                except Exception as e:
                    bot.reply_to(message, str(e))
            elif message.text.lower() in ["screen", "screenshot", "pantalla", "captura"]:
                # Needs espeak with mbrola spanish voices
                try:
                    if DISPLAY is None:
                        bot.reply_to(message, "DISPLAY is not set.")
                    response = str(os.popen('xhost + 2>&1').read())
                    response = str(os.popen('rm screen.png screen.jpg 2>&1').read())
                    response = str(os.popen('import -window root screen.png && convert screen.png screen.jpg 2>&1').read())
                    screen = open("screen.jpg", "rb")
                    bot.send_photo(this_chat_id, screen)
                    if not response:
                        response = "Done."
                except Exception as e:
                    bot.reply_to(message, str(e))
            else:
                menu(message)
        else:
            menu(message)
    except Exception as e:
        bot.send_message(this_chat_id, "Error: "+str(e))










def remove_prefix(text, prefix):
    if text.lower().startswith(prefix.lower()):
        return text[len(prefix):]
    return text  # or whatever

def last_chat_id():
    with open("last_admin_chat_id","r") as f:
        id = f.readline()
        if not id:
            id = "0"
    f.close()
    return int(id)

def register_chat_id(id):
    with open("last_admin_chat_id","w") as f:
        f.write(id)
    f.close()












last_chat_id_int = last_chat_id()

if last_chat_id_int > 0:
    authorized.append(last_chat_id_int)
    bot.send_message(last_chat_id_int, "Starting bot.")

bot.polling()

last_chat_id_int = last_chat_id()

if last_chat_id_int > 0:
    bot.send_message(last_chat_id_int, "Closing bot.")

