from django.contrib import admin
from solo.admin import SingletonModelAdmin
from hotel_reservations.models import HotelConfiguration


admin.site.register(HotelConfiguration, SingletonModelAdmin)
