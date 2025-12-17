from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from ..models import Room, Booking
from .serializers import RoomSerializer, BookingSerializer


# Create your views here.

class RootAPIView(APIView):

    def get(self, request):

        return Response({"message": "Hello, World!"})


class RoomViewSet(viewsets.ModelViewSet):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class BookingViewSet(viewsets.ModelViewSet):

    queryset = Booking.bookings.all()
    serializer_class = BookingSerializer
