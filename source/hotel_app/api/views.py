from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Room, Booking
from .serializers import RoomSerializer, BookingSerializer, CreateBookingSerializer, UpdateBookingSerializer


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
    response_serializer = BookingSerializer # serializer used in all responses

    def get_serializer_class(self):
        """
        Selects appropriate serializer for each action.
        """

        if self.action == "list" or self.action == "retrieve":
            return BookingSerializer
        elif self.action == "create":
            return CreateBookingSerializer
        elif self.action == "update" or self.action == "partial_update":
            return UpdateBookingSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            booking = serializer.create(serializer.validated_data)

            return Response(self.response_serializer(instance=booking).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):

        return self._update_booking(request)

    def partial_update(self, request, *args, **kwargs):

        return self._update_booking(request)

    def _update_booking(self, request):

        booking = self.get_object()  # retrieve the booking to be updated
        serializer = self.get_serializer(data=request.data)  # de-serialize the data send in the request

        if serializer.is_valid():  # if valid, update the booking
            booking.update_booking(**serializer.validated_data)

            return Response(self.response_serializer(instance=booking).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
