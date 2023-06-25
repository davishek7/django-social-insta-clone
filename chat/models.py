from django.db import models
from commons.models import TimeStampModel, StatusModel
from django.conf import settings
from post.random_slug import generate_random_slug
from django.db.models import Q

# Create your models here.

User = settings.AUTH_USER_MODEL

class Inbox(TimeStampModel, StatusModel):
    slug = models.SlugField(max_length=255, db_index=True, unique=True, blank=True, null=True)
    users = models.ManyToManyField(User, related_name='user_inboxes', blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = generate_random_slug()
        super(Inbox, self).save(*args, **kwargs)

    @property
    def get_last_message(self):
        return self.message_set.filter(status=True).last()

    class Meta:
        verbose_name_plural = 'Inboxes'

    def __str__(self):
        return f'{self.users.first()} - {self.users.last()}'


class Message(TimeStampModel, StatusModel):

    TEXT = 'TEXT'
    EMOJI = 'EMOJI'

    MESSAGE_TYPE = (
        ('TEXT', TEXT),
        ('EMOJI', EMOJI)
    )

    inbox = models.ForeignKey(Inbox, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_user', blank=True, null=True)
    body = models.TextField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='message_attachments', blank=True, null=True)
    type = models.CharField(max_length=20, choices=MESSAGE_TYPE, blank=True, null=True)
    read_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}'s message:'{self.body}'"