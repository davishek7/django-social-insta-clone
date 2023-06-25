from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile, LoggedUser
from django.contrib.auth.signals import user_logged_in, user_logged_out


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def login_user(sender, request, user, **kwargs):
    logged_in_user = LoggedUser.objects.filter(user=user, status=False).first()
    if logged_in_user:
        logged_in_user.status = True
        logged_in_user.save()
    else:
        LoggedUser.objects.create(user=user)

def logout_user(sender, request, user, **kwargs):
    logged_in_user = LoggedUser.objects.filter(user=user, status=True).first()
    if logged_in_user:
        logged_in_user.status = False
        logged_in_user.save()

user_logged_in.connect(login_user)
user_logged_out.connect(logout_user)