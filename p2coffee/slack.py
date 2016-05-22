import requests
from django.conf import settings


def send_msg(text, channel=None):
    data = {'text': text}
    if channel is not None:
        data['channel'] = channel

    requests.post(settings.SLACK_WEBHOOK_URL, json=data)
