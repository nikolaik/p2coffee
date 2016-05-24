import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def send_msg(text, channel=None):
    url = settings.SLACK_WEBHOOK_URL
    data = {'text': text}
    if channel is not None:
        data['channel'] = channel

    logger.debug(data)

    if url:
        requests.post(url, json=data)
