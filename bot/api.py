import requests
from . import settings

def message_send(message, user_id):
    uri = settings.VK_API_METHOD_MESSAGE_SEND

    params = {
        'message': message,
        'user_id': user_id,
        'access_token': settings.VK_ACCESS_TOKEN,
        'v': settings.VK_API_VERSION
    }

    response = requests.get(uri, params=params)

    return response
