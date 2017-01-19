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
        'username': settings.SLACK_BOT_USERNAME,
        'icon_url': settings.SLACK_BOT_ICON_URL,
        **data
    })

    url = url_base + '{}?{}'.format(method, params)
    logger.debug("Sending request to slack with data: %s", json.dumps(data))

    response = requests.post(url)
    content = json.loads(response.content.decode())

    error = content.get('error')
    if error:
        logger.error("Method %s, got response: ok=%s, %s", method, str(content['ok']), 'error='+error)
    else:
        logger.debug("Method %s, got response: ok=%s", method, str(content['ok']))
    return content


def _upload(method, f, channels=None, **data):
    url_base = settings.SLACK_API_URL_BASE
    params = {
        'token': settings.SLACK_API_TOKEN,
        'username': settings.SLACK_BOT_USERNAME,
        'icon_url': settings.SLACK_BOT_ICON_URL,
    }

    if channels:
        params['channels'] = ",".join(channels)

    for k, v in data.items():
        if k is not None and v is not None:
            params[k] = v

    params = urllib.parse.urlencode(params)

    url = url_base + '{}?{}'.format(method, params)
    logger.debug("Uploading file to slack.")

    response = requests.post(url, files={'file': ('current.jpg', f)})
    content = json.loads(response.content.decode())

    error = content.get('error')
    if error:
        logger.error("Method %s, Got response: ok=%s, %s", method, str(content['ok']), 'error='+error)
    else:
        logger.debug("Method %s, Got response: ok=%s", method, str(content['ok']))
    return content


def channels_list():
    return _dispatch('channels.list')


def channels_info(channel):
    return _dispatch('channels.info', channel=channel)


def channels_join(channel):
    return _dispatch('channels.join', channel=channel)


def chat_post_message(channel, text=None, attachments=None):
    data = {
        'channel': channel,
    }

    if text is not None:
        data['text'] = text

    if attachments is not None:
        data['attachments'] = attachments

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


def files_upload(f, filename=None, filetype=None, title=None, initial_comment=None, channels=None):
    return _upload('files.upload', f,
                   filename=filename, filetype=filetype, title=title,
                   initial_comment=initial_comment, channels=channels)

