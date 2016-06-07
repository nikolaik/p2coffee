import json
import logging
import requests
import urllib.parse
from django.conf import settings


logger = logging.getLogger(__name__)


def _dispatch(method, **data):
    url_base = settings.SLACK_API_URL_BASE
    params = urllib.parse.urlencode({
        'token': settings.SLACK_API_TOKEN,
        'username': 'Kaffetrakteren',
        **data
    })

    url = url_base + '{}?{}'.format(method, params)
    logger.debug("Sending request to slack with data: %s", json.dumps(data))

    response = requests.post(url)
    content = json.loads(response.content.decode())

    error = content.get('error', '')
    logger.debug("Got response: ok=%s%s", str(content['ok']), ', error='+error if error else '')
    return content


def channels_list():
    return _dispatch('channels.list')


def channels_info(channel):
    return _dispatch('channels.info', channel=channel)


def chat_post_message(channel, text):
    data = {
        'channel': channel,
        'text': text,
    }

    return _dispatch('chat.postMessage', **data)

def chat_update(channel, timestamp, text):
    data = {
        'channel': channel,
        'ts': timestamp,
        'text': text,
    }

    return _dispatch('chat.update', **data)

def chat_delete(channel, timestamp):
    data = {
        'channel': channel,
        'ts': timestamp,
    }

    return _dispatch('chat.delete', **data)

