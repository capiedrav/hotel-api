from rest_framework import serializers

from ..models import Room, Booking

class RoomSerializer(serializers.ModelSerializer):
    class Meta:

        model = Room

        fields = ["number", "size", "price"]


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for listing bookings (list and retrieve actions).
    """

    class Meta:

        model = Booking

        fields = ["customer", "room", "from_date", "to_date", "price"]


class CreateBookingSerializer(serializers.ModelSerializer):
    """
    Serializer for creating bookings (create action).
    """

    class Meta:
        model = Booking

        # note that price field is not included because it is calculated in the backend
        fields = ["customer", "room", "from_date", "to_date"]


class UpdateBookingSerializer(serializers.ModelSerializer):
    """
    Serializer for updating bookings (update and partial_update actions).
    """

    class Meta:
        model = Booking

        # note that customer field is not included because a booking can't change customers
        # also price field is not included because it is calculated in the backend
        fields = ["room", "from_date", "to_date"]

        extra_kwargs = { # all fields are optional
            "room": {"required": False},
            "from_date": {"required": False},
            "to_date": {"required": False}
        }

