from .models import Story
from datetime import datetime
from pytz import timezone


def check_user_active_story(user_id):

    now = datetime.now()

    indian_time = timezone('Asia/Kolkata')

    stories = Story.objects.filter(user = user_id, status=True).all()

    for story in stories:

        local_dt = story.created_at.astimezone(indian_time)

        time_diff = now - local_dt.replace(tzinfo=None)
        time_diff_seconds = time_diff.total_seconds()

        if time_diff_seconds > 86400:
            story.status = False
            story.save()