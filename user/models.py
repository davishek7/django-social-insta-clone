from django.db import models
from commons.models import StatusModel, TimeStampModel
from django.conf import settings
from story.models import Story
from post.random_slug import generate_random_slug

# Create your models here.

User = settings.AUTH_USER_MODEL

class Highlight(StatusModel, TimeStampModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    stories = models.ManyToManyField(Story, related_name='story_highlights', blank=True)

    def __str__(self):
        return f"{self.user}'s highlight - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = generate_random_slug()
        super(Highlight, self).save(*args, **kwargs)

    @property
    def get_first_story(self):
        return self.stories.order_by('created_at').first()