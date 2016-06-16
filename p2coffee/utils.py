import logging
import io
import requests
from django.conf import settings
from django.utils.timezone import is_naive, get_current_timezone_name, pytz, is_aware, localtime
from requests.exceptions import ConnectionError

logger = logging.getLogger(__name__)


def format_local_timestamp(dt, dt_format='%Y-%m-%d %H:%M'):
    """Returns a formatted localized timestamp according current timezone
    :param dt: A datetime object
    :param dt_format: Format string passed to strftime"""

    if is_naive(dt):
        tz = pytz.timezone(get_current_timezone_name())
        dt = tz.localize(dt)
    elif is_aware(dt):
        dt = localtime(dt)

    return dt.strftime(dt_format)


def coffee_image():
    url = settings.COFFEE_CAMERA_URL
    auth = (settings.COFFEE_CAMERA_USER, settings.COFFEE_CAMERA_PASS)

    try:
        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            logger.debug("Got image with %d bytes", len(response.content))
            return io.BytesIO(response.content)

        logger.error("Couldn't get camera image: %s", str(response.content))
    except ConnectionError as e:
        logger.error("Couldn't get camera image: %s", str(e))

    return None

