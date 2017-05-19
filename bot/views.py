from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from telegrambot.bot_views.generic import TemplateCommandView

from . import settings, api
from bot.models import Message
import json

import redis

redis_connection = redis.StrictRedis(host='localhost', port=6379, db=0) # подключиться к redis

@csrf_exempt
@require_http_methods(["POST"])
def callbackapi(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if body['type'] == 'confirmation':

        return HttpResponse(settings.VK_CONFIRMATION_KEY) # подтверждение запроса от вк

    elif body['type'] == 'message_new':
        user_id = body['object']['user_id'] # получить id пользователя
        body = body['object']['body'] # получить тело сообщения
        reply_body =  '' # возвращаемое сообщение
        reply_delimeters = '' # возвращаемый разделитель

        user_context = redis_connection.get( 'vk:{user_id}'.format(user_id=user_id) ) # получить предыдущий контекст сохраненный в redis
        if user_context is not None:
            context = json.loads( user_context.decode("utf-8") ) # если контекст существует в бд, то десериализовать его в объект
        else:
            context = {'status': 'clear', 'messages': []} # иначе создать новый объект контекста

        if body.lower().strip() == 'привет' and context['status'] != 'record': # если введена команда привет и до это не было команды начать запись
            context['status'] = 'new' # установить статус
            context['messages'] = [] # установить пустой массив сообщений
            reply_delimeters = 'Запись началась.' # вернуть ответ о начале записи

        elif body.lower().strip() == 'пока': # если введена команда пока
            context['status'] = 'closed' # установить статус закрыто
            reply_delimeters = 'Запись завершена.' # вернуть запись завершена

        if context['status'] == 'record': # если статус record
            context['messages'].append(body) # добавить сообщение в массив messages в контексте
            message = Message(
                user_id = user_id,
                body = body,
                source = Message.SOURCE_VK
            )
            message.save() # сохранить запись в вк
        elif context['status'] == 'new': # если статус new
            if context.get('count'): # если в контексте есть кол-во слов
                reply_body = 'В прошлом диалоге было {count} слов.'.format(count=context['count']) # вернуть кол-во слов
                del context['count'] # удалить кол-во слов из контекста
            context['status'] = 'record' # установить статус запись
        elif context['status'] == 'closed': # если статус closed
            messages = context['messages']
            count = 0
            for message in messages: # посчитать кол-во слов
                count += len(message.strip().split(' '))
            context['count'] = count
            context['status'] = 'unknown' # установить статус unknown
        elif context['status'] == 'clear': # если статус clear
            reply_body = 'Для начала диалога напишите мне Привет, а для окончания Пока' # вернуть сообщение
        elif context['status'] == 'unknown': # если статус unknown
            reply_body = 'Для начала диалога напишите мне Привет' # вернуть сообщение

        redis_connection.set( 'vk:{user_id}'.format(user_id=user_id), json.dumps( context ) ) # сохранить контекст в redis

        api.message_send(reply_delimeters + "\n" + reply_body, user_id) # написать пользователю сформированный ответ

        return HttpResponse('ok') # вернуть ответ вк, чтобы он не повторял запросы
