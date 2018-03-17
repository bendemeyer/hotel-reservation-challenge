from django.contrib import admin
from solo.admin import SingletonModelAdmin
from hotel_reservations.models import HotelConfiguration, Reservation
from hotel_reservations.forms import ReservationAdmin


admin.site.register(HotelConfiguration, SingletonModelAdmin)
admin.site.register(Reservation, ReservationAdmin)