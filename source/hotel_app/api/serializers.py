from rest_framework import serializers

from ..models import Room, Booking

class RoomSerializer(serializers.ModelSerializer):
    class Meta:

        model = Room

        fields = ["number", "size", "price"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:

        model = Booking

        fields = ["customer", "room", "from_date", "to_date", "price"]
        extra_kwargs = {"price": {"required": False}}