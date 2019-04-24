from flask import Flask
from flask import request
from flask_sslify import SSLify
import telebot
import time
import random

TOKEN = '<TOKEN>'
bot = telebot.TeleBot(TOKEN, threaded=False)
bot_id = bot.get_me().id

import members as mem
import rw

app = Flask(__name__)
sslify = SSLify(app)


bot.remove_webhook()
time.sleep(1)
bot.set_webhook('https://<NICKNAME>.pythonanywhere.com/'+TOKEN)


@bot.message_handler(content_types=["new_chat_members"])
def handle_new_member(message):
    try:
        if not mem.is_chat_registered(message):
            mem.add_chat(message)

        if mem.allow_add_member(message):
            mem.add_member(message)
            rw.save_stats_in_file(mem.file_of_members, mem.members)
            rw.delete_first__line_in_file(mem.file_of_members)
        mem.send_greetings(message)
    except Exception as e:
        bot.send_message(message.chat.id, e)


@bot.message_handler(content_types=["left_chat_member"])
def handle_left_member(message):
    try:
        if mem.allow_remove_member(message):
            mem.remove_member(message)
            rw.save_stats_in_file(mem.file_of_members, mem.members)
            rw.delete_first__line_in_file(mem.file_of_members)
        mem.send_parting(message)
    except Exception as e:
        bot.send_message(message.chat.id, e)


@bot.message_handler(commands=["remove_participant"])
def handle_remove_participant(message):
    try:
        if not mem.is_group(message):
            mem.send_isnt_group(message)
            return

        if not mem.is_called_by_admin(message):
            mem.send_refuse(message)
        elif mem.check_valid_syntax(message):
            if mem.remove_member_by_command(message):
                rw.save_stats_in_file(mem.file_of_members, mem.members)
                rw.delete_first__line_in_file(mem.file_of_members)
                mem.send_member_removed(message)
            else:
                mem.send_member_not_exists(message)
        else:
            mem.send_invalid_syntax(message)
    except Exception as e:
        bot.send_message(message.chat.id, e)


@bot.message_handler(commands=["add_me_to_participants"])
def handle_add_participant(message):
    try:
        if not mem.is_group(message):
            mem.send_isnt_group(message)
            return

        if not mem.is_chat_registered(message):
            mem.add_chat(message)

        if mem.is_in_participants(message):
            mem.send_add_refuse(message)
        else:
            mem.add_member_by_command(message)
            rw.save_stats_in_file(mem.file_of_members, mem.members)
            rw.delete_first__line_in_file(mem.file_of_members)
            mem.send_participant_added(message)
    except Exception as e:
        bot.send_message(message.chat.id, e)


@bot.message_handler(commands=["show_participants"])
def handle_show_participants(message):
    try:
        chat_id = message.chat.id
        if not mem.is_group(message):
            mem.send_isnt_group(message)
            return

        if mem.is_no_participants(message):
            msg = "ще немає жодного учасника!"
        else:
            msg = "список учасників:"
            for user in mem.members[chat_id]:
                msg = f'{msg}\n@{user[0]}'
        bot.send_message(chat_id, msg)
    except Exception as e:
        bot.send_message(chat_id, e)


@bot.message_handler(commands=["rules", "start", "help"])
def handle_rules(message):
    try:
        mem.send_rules(message)
    except Exception as e:
        bot.send_message(message.chat.id, e)


@bot.message_handler(commands=["rand"])
def handle_rand(message):
    try:
        chat_id = message.chat.id
        if not mem.is_group(message):
            mem.send_isnt_group(message)
            return
        if mem.is_no_participants(message):
            mem.send_no_participants(message)
            return
        user = random.choice(mem.members[chat_id])
        msg = "@{0}, я обираю тебе!".format(user[0])
        bot.send_message(chat_id, msg)
    except Exception as e:
        bot.send_message(chat_id, e)


@app.route('/', methods=["GET"])
def GET():
    return "<h1>I'm working :)</h1>"


@app.route('/'+TOKEN, methods=["POST"])
def POST():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "ok", 200


if __name__ == '__main__':
    app.run()