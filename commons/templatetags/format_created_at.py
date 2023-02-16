from django import template
from datetime import datetime
from pytz import timezone

register = template.Library()

@register.filter
def format_created_time(created_at):

    now = datetime.now()

    indian_time = timezone('Asia/Kolkata')
    local_dt = created_at.astimezone(indian_time)

    time_diff = now - local_dt.replace(tzinfo=None)
    time_diff_seconds = time_diff.total_seconds()

    if 1 < time_diff_seconds < 60:
        seconds = int(time_diff_seconds)
        formatted_created_at = f'{seconds}s'

    elif 60 < time_diff_seconds < 3600:
        minutes = int(time_diff_seconds / 60)
        formatted_created_at = f'{minutes}m'

    elif 3600 < time_diff_seconds < 86400:
        hours = int(time_diff_seconds/3600)
        formatted_created_at = f'{hours}h'

    elif 86400 < time_diff_seconds < 604800:
        days = int(time_diff_seconds/86400)
        formatted_created_at = f'{days}d'

    elif time_diff_seconds > 604800:
        weeks = int(time_diff_seconds/604800)
        formatted_created_at = f'{weeks}w'
    
    else:
        formatted_created_at = 'now'

    return formatted_created_at