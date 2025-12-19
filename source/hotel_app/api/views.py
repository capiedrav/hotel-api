from rest_framework.views import APIView
from rest_framework import viewsets, status
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

    def update(self, request, *args, **kwargs):

        booking = self.get_object() # retrieve the booking to be updated

        serializer = self.get_serializer(data=request.data) # de-serialize the data send in the request

        if serializer.is_valid(): # if valid, update the booking
            booking.update_booking(
                from_date=serializer.validated_data["from_date"],
                to_date=serializer.validated_data["to_date"],
                room=serializer.validated_data["room"],
            )

            return Response(self.get_serializer(instance=booking).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):

        booking = self.get_object()

        serializer = self.get_serializer(data=request.data, partial=True) # allows incomplete data

        if serializer.is_valid():
            booking.update_booking(**serializer.validated_data)

            return Response(self.get_serializer(instance=booking).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



