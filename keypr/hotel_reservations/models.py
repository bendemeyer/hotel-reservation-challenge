from django.db import models
from solo.models import SingletonModel
from django.core.exceptions import ValidationError


def is_positive(num):
    if num <= 0:
        raise ValidationError("Value must be greater than 0")


class HotelConfiguration(SingletonModel):
    room_count = models.IntegerField(validators=[is_positive], default=100)
    overbooking_level = models.FloatField(validators=[is_positive], default=0)
