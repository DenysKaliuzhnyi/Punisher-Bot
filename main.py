from flask import Flask
from flask import request
from flask_sslify import SSLify
import telebot
import time

TOKEN = '<TOKEN>'
bot = telebot.TeleBot(TOKEN, threaded=False)
bot_id = bot.get_me().id

app = Flask(__name__)
sslify = SSLify(app)


bot.remove_webhook()
time.sleep(1)
bot.set_webhook('https://<USERNAME>.pythonanywhere.com/'+TOKEN)


import handlers


@app.route('/', methods=["GET"])
def GET():
    return "<h1>I'm working :)</h1>"


@app.route('/'+TOKEN, methods=["POST"])
def POST():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "ok", 200


if __name__ == '__main__':
    app.run()