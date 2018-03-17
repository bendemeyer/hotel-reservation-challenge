from django.contrib import admin
from django.urls import path
from hotel_reservations.views.new_reservation import NewReservation
from hotel_reservations.views.confirmation import Confirmation
from hotel_reservations.views.api.reservations import ReservationAPI
from hotel_reservations.views.api.configuration import HotelConfigurationAPI

urlpatterns = [
    path('', NewReservation.as_view()),
    path('confirmation/', Confirmation.as_view()),
    path('reservations/', ReservationAPI.as_view()),
    path('config/', HotelConfigurationAPI.as_view()),
    path('admin/', admin.site.urls),
]
