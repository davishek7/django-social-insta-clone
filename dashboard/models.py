from django.db import models
from commons.models import TimeStampModel, StatusModel

# Create your models here.

class Report(TimeStampModel, StatusModel):
    pass


class Activity(TimeStampModel, StatusModel):
    pass