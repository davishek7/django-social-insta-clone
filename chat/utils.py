from .models import Inbox

def get_inbox(first_user, second_user):
    first_user_inboxes = first_user.user_inboxes.all()
    second_user_inboxes = second_user.user_inboxes.all()
    common_inbox = set(first_user_inboxes).intersection(set(second_user_inboxes))

    if len(common_inbox) > 0:
        return list(common_inbox)[0]
    else:
        inbox = Inbox.objects.create()
        inbox.users.add(first_user, second_user)
        return inbox