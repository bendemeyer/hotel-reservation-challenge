from django.db import models
from solo.models import SingletonModel
from hotel_reservations.validators import (is_valid_date_range, is_available,
                                           is_positive, is_not_negative,
                                           is_email_address, is_future_date)


class HotelConfiguration(SingletonModel):
    room_count = models.IntegerField(validators=[is_positive], default=100)
    overbooking_level = models.FloatField(validators=[is_not_negative], default=0)


class Reservation(models.Model):
    id = models.AutoField()
    id.primary_key = True
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, validators=[is_email_address])
    check_in = models.DateField(validators=[is_future_date])
    check_out = models.DateField()

    def clean(self):
        super().clean()
        if self.check_in and self.check_out:
            is_valid_date_range(self.check_in, self.check_out)
            is_available(self.check_in, self.check_out)
