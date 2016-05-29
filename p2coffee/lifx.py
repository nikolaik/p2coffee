from django.conf import settings
import requests

# Ref: http://api.developer.lifx.com/
LIFX_API_URL = 'https://api.lifx.com/v1/'


def _get_auth_headers():
    return {"Authorization": "Bearer %s" % settings.LIFX_TOKEN}


def get_lights(selector='all'):
    url = '{}lights/{}'.format(LIFX_API_URL, selector)

    response = requests.get(url, headers=_get_auth_headers())

    return response.json()


def toggle_power(selector='all'):
    url = '{}lights/{}/toggle'.format(LIFX_API_URL, selector)

    response = requests.post(url, headers=_get_auth_headers())

    return response.json()


def set_state(state, selector='all'):
    """Example:
    state = {
        "power": "on",
        "color": "green",
        "brightness": 1.0,
        "duration": 3.0  # in seconds
    }

    Ref: https://api.developer.lifx.com/docs/set-state
    """
    url = '{}lights/{}/state'.format(LIFX_API_URL, selector)

    response = requests.put(url, json=state, headers=_get_auth_headers())

    return response.json()
