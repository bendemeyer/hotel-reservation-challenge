from hotel_reservations.models import Reservation, HotelConfiguration
from rest_framework import serializers


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"


class HotelConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelConfiguration
        fields = "__all__"
