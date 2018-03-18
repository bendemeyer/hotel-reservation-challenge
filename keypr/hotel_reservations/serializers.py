from hotel_reservations.models import Reservation, HotelConfiguration
from rest_framework import serializers
from hotel_reservations.validators import is_valid_date_range, is_available


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
    
    def validate(self, data):
        is_valid_date_range(data["check_in"], data["check_out"])
        is_available(data["check_in"], data["check_out"])
        return data


class HotelConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelConfiguration
        fields = "__all__"
