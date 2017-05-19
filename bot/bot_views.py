from telegrambot.bot_views.generic import TemplateCommandView
import json
import redis
from bot.models import Message

redis_connection = redis.StrictRedis(host='localhost', port=6379, db=0) # подключиться к redis

class StartCommandView(TemplateCommandView):
    template_text = "bot/messages/command_write_message_text.txt" # шаблон вьюхи
    context_object_name = "response" # название контекстной переменной

    def get_context(self, bot, update, **kwargs): # переопределение контекстной переменной
        user_id = update.message.chat.id  # id пользователя
        reply_delimeter = ''

        user_context = redis_connection.get( 'telegram:{user_id}'.format(user_id=user_id) ) # получить предыдущий контекст сохраненный в redis
        if user_context is not None:
            context = json.loads( user_context.decode("utf-8") ) # если контекст существует в бд, то десериализовать его в объект
        else:
            context = {'status': 'clear', 'messages': []} # иначе создать новый объект контекста

        if context['status'] == 'closed': # если статус closed
            messages = context['messages']
            count = 0
            for message in messages: # посчитать кол-во слов
                count += len(message.strip().split(' '))
            reply_delimeter = ' В прошлом диалоге было {count} слов.'.format(count=count) # вернуть в ответе кол-во слов
            context['status'] = 'record' # установить статус record для начала записи
            context['messages'] = [] # обнулить массив сообщений

        redis_connection.set( 'telegram:{user_id}'.format(user_id=user_id), json.dumps( context ) ) # сохранить контекст в redis

        reply_body = 'Запись началась.' # сообщение о начале записи

        response = {self.context_object_name: reply_body + reply_delimeter} # переопределение контекста шаблона

        return response

class CloseCommandView(TemplateCommandView):
    template_text = "bot/messages/command_write_message_text.txt" # шаблон вьюхи
    context_object_name = "response" # название контекстной переменной

    def get_context(self, bot, update, **kwargs):
        user_id = update.message.chat.id # id пользователя
        user_context = redis_connection.get( 'telegram:{user_id}'.format(user_id=user_id) ) # получить предыдущий контекст сохраненный в redis
        if user_context is not None:
            context = json.loads( user_context.decode("utf-8") ) # если контекст существует в бд, то десериализовать его в объект
        else:
            context = {'status': 'clear', 'messages': []} # иначе создать новый объект контекста

        context['status'] = 'closed' # установить статус closed
        redis_connection.set( 'telegram:{user_id}'.format(user_id=user_id), json.dumps( context ) ) # сохранить контекст в redis

        reply_body = 'Запись завершена.' # сообщение о начале записи

        response = {self.context_object_name: reply_body} # переопределение контекста шаблона

        return response

class MessageCommandView(TemplateCommandView):
    template_text = "bot/messages/command_write_message_text.txt" # шаблон вьюхи
    context_object_name = "response" # название контекстной переменной

    def get_context(self, bot, update, **kwargs):
        user_id = update.message.chat.id # id пользователя
        body = update.message.text # тело сообщения
        reply_body =  ''

        user_context = redis_connection.get( 'telegram:{user_id}'.format(user_id=user_id) ) # получить предыдущий контекст сохраненный в redis
        if user_context is not None:
            context = json.loads( user_context.decode("utf-8") ) # если контекст существует в бд, то десериализовать его в объект
        else:
            context = {'status': 'clear', 'messages': []} # иначе создать новый объект контекста

        if context['status'] == 'record': # если статус record
            context['messages'].append(body) # добавить сообщение в messages в объекте контекст
            message = Message(
                user_id = user_id,
                body = body,
                source = Message.SOURCE_TELEGRAM
            )
            message.save() # сохранить в базу данных сообщение
            reply_body = 'Записал: {body}'.format(body=body) # ответное сообщение после сохранения
        elif context['status'] == 'clear': # если статус clear
            reply_body = 'Для начала диалога напишите мне /hello, а для окончания /bye' # ответное сообщение с уведомлением

        redis_connection.set( 'telegram:{user_id}'.format(user_id=user_id), json.dumps( context ) ) # сохранить контекст в redis

        response = {self.context_object_name: reply_body} # переопределение контекста шаблона

        return response