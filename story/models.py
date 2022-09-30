from django.db import models
from commons.models import TimeStampModel, StatusModel

# Create your models here.

class Story(TimeStampModel, StatusModel):
    pass