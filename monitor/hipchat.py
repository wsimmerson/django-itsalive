from django.conf import settings

import requests
import json


def send(message, color):
    headers = {
        'Authorization': 'Bearer {}'.format(settings.HIPCHAT_TOKEN),
        'Accept-Charset': 'UTF-8',
        'Content-Type': 'application/json'
    }
    url = 'https://api.hipchat.com/v2/room/{}/notification'.format(settings.HIPCHAT_ROOM)

    msg = {
        'message': message,
        'from': "It's Alive",
        'message_format': 'html',
        'json': True,
        'color': color
    }

    r = requests.post(url, data=json.dumps(msg), headers=headers)
