from rest_framework import serializers

from ..models import Room, Booking

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["number", "size", "price"]