from django.utils.timezone import is_naive, get_current_timezone_name, pytz, is_aware, localtime


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
