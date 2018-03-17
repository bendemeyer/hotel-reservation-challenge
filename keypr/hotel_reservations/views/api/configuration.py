from hotel_reservations.models import HotelConfiguration
from hotel_reservations.serializers import HotelConfigurationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class HotelConfigurationAPI(APIView):

    def post(self, request, format=None):
        hotel_config = HotelConfiguration.get_solo()
        serializer = HotelConfigurationSerializer(hotel_config, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)