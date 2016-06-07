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
        'name': 'Kaffetrakteren',
        **data
    })

    url = url_base + '{}?{}'.format(method, params)
    logger.debug("Sending request to slack with data: %s", json.dumps(data))

    response = requests.post(url)
    content = json.loads(response.content.decode())

    error = content.get('error', '')
    logger.debug("Got response: ok=%s%s", str(content['ok']), ', error='+error if error else '')
    return content


def send_msg(text, channel=None):
    url = settings.SLACK_WEBHOOK_URL
    data = {'text': text}
    if channel is not None:
        data['channel'] = channel

    logger.debug("Sending request to slack with data: %s", json.dumps(data))

    if url:
        response = requests.post(url, json=data)
        logger.debug("Got response from slack (%d): %s", response.status_code, response.content)
        return response


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

