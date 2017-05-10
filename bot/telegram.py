# -*- coding: utf-8 -*-
import os, sys, django

sys.path.append('/var/www/django/project')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

import telebot
import settings
from bot import models

telegram = telebot.TeleBot(settings.TELEGRAM_TOKEN)

@telegram.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if message == '/start': return

    user_id = message.from_user.id
    body = message.text
    
    message_row = models.Message(
            user_id = user_id,
            body = body,
            source = models.Message.SOURCE_TELEGRAM
        )

    message_row.save()
    
    reply_body = "Записал: '{body}'".format(body=body)
    telegram.send_message(message.chat.id, reply_body)

def run():
    telegram.polling(none_stop=True)


if __name__ == "__main__":
    run()
