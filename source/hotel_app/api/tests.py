from hmac import new
from http.client import responses

from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Room, Booking
from .serializers import RoomSerializer, BookingSerializer
from .views import RootAPIView, RoomViewSet, BookingViewSet
from datetime import date, timedelta

# Create your tests here.


User = get_user_model()


class RootAPITest(TestCase):

    def setUp(self):

        self.client = APIClient()

    def test_api_root_is_resolved_to_RootAPIView(self):

        view = resolve(reverse("api-root"))

        self.assertEqual(view.func.view_class, RootAPIView)

    def test_api_root(self):

        response = self.client.get(reverse("api-root"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'), "Hello, World!")


class RoomAPITests(TestCase):

    def setUp(self):

        self.client = APIClient()

    @staticmethod
    def create_rooms():
        rooms = []
        for i in range(1, 11):
            rooms.append(Room(number=f"Room {i}", size=25, price=100))

        Room.objects.bulk_create(rooms)

    def test_room_api_is_resolved_to_RoomViewSet(self):

        view = resolve(reverse("room-list")) # this view is used in GET and POST requests

        self.assertEqual(view.func.__name__, RoomViewSet.__name__)

        # this view is used in GET, PUT, PATCH and DELETE requests
        view = resolve(reverse("room-detail", kwargs={"pk": 1}))

        self.assertEqual(view.func.__name__, RoomViewSet.__name__)

    def test_list_rooms(self):

        self.create_rooms()

        response = self.client.get(reverse('room-list'))

        rooms = Room.objects.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), RoomSerializer(rooms, many=True).data)

    def test_get_room_by_id(self):

        Room.objects.create(number="Room 1", size=25, price=100)

        response = self.client.get(reverse("room-detail", kwargs={"pk": 1}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), RoomSerializer(Room.objects.get(pk=1)).data)

    def test_create_room(self):

        response = self.client.post(reverse("room-list"), data={"number": "Room 1", "size": 25, "price": 100})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), RoomSerializer(Room.objects.get(pk=1)).data)

    def test_update_room(self):

        Room.objects.create(number="Room 1", size=25, price=100)

        response = self.client.put(reverse("room-detail", kwargs={"pk": 1}),
                                   data={"number": "Room 1", "size": 30, "price": 110})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), RoomSerializer(Room.objects.get(pk=1)).data)

    def test_patch_room(self):

        Room.objects.create(number="Room 1", size=25, price=100)

        response = self.client.patch(reverse("room-detail", kwargs={"pk": 1}),
                                     data={"size": 30, "price": 110})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), RoomSerializer(Room.objects.get(pk=1)).data)

    def test_delete_room(self):

        Room.objects.create(number="Room 1", size=25, price=100)

        response = self.client.delete(reverse("room-detail", kwargs={"pk": 1}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Room.objects.all().count(), 0)


class BookingAPITests(TestCase):

    def setUp(self):

        self.client = APIClient()

    @staticmethod
    def create_bookings():

        rooms = []
        users = []
        for i in range(1, 11): # create rooms and users
            rooms.append(Room(number=f"Room {i}", size=25, price=100))
            users.append(User(email=f"testuser{i}@example.com", password="testpassword"))

        Room.objects.bulk_create(rooms)
        User.objects.bulk_create(users)

        bookings = []
        for i in range(len(rooms)): # create bookings
            from_date = date.today()
            to_date = date.today() + timedelta(days=10)
            bookings.append(
                Booking.create_booking(
                    customer=users[i],
                    room=rooms[i],
                    from_date=from_date,
                    to_date=to_date,
                ))

        Booking.bookings.bulk_create(bookings)

    @staticmethod
    def create_a_booking():

        room = Room.objects.create(number="Room 1", size=25, price=100)
        user = User.objects.create(email="testuser@example.com", password="testpassword")

        from_date = date.today()
        to_date = date.today() + timedelta(days=10)
        Booking.bookings.create(
            customer=user,
            room=room,
            from_date=from_date,
            to_date=to_date
        )

    def test_booking_api_is_resolved_to_BookingViewSet(self):

        view = resolve(reverse("booking-list")) # endpoint for GET and POST requests

        self.assertEqual(view.func.__name__, BookingViewSet.__name__)

        # endpoint for GET, PUT, PATCH and DELETE requests
        view = resolve(reverse("booking-detail", kwargs={"pk": 1}))

        self.assertEqual(view.func.__name__, BookingViewSet.__name__)

    def test_list_bookings(self):

        self.create_bookings()

        response = self.client.get(reverse('booking-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Booking.bookings.all().count(), 10)

    def test_get_booking_by_id(self):

        self.create_a_booking()

        response = self.client.get(reverse("booking-detail", kwargs={"pk": 1}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), BookingSerializer(Booking.bookings.get(pk=1)).data)

    def test_create_booking(self):

        customer = User.objects.create(email="testuser@example.com", password="testpassword")
        room = Room.objects.create(number="Room 1", size=25, price=100)

        from_date = date.today()
        to_date = date.today() + timedelta(days=10)

        payload = {
            "customer": customer.id,
            "room": room.id,
            "from_date": from_date,
            "to_date": to_date,
        }
        response = self.client.post(reverse("booking-list"), data=payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), BookingSerializer(Booking.bookings.get(pk=1)).data)

        # check booking price is calculated correctly
        expected_price = (to_date - from_date).days * room.price
        self.assertEqual(response.json()["price"], expected_price)

    def test_update_booking(self):

        self.create_a_booking()

        booking = Booking.bookings.first()

        new_to_date = booking.from_date + timedelta(days=5) # new to_date

        payload = {
            "customer": booking.customer.id,
            "room": booking.room.id,
            "from_date": booking.from_date,
            "to_date": new_to_date, # field to update
        }

        response = self.client.put(reverse("booking-detail", kwargs={"pk": 1}), data=payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), BookingSerializer(Booking.bookings.get(pk=1)).data)

        # check booking price is calculated correctly
        expected_price = (new_to_date - booking.from_date).days * booking.room.price
        self.assertEqual(response.json()["price"], expected_price)

    def test_patch_booking(self):

        self.create_a_booking()

        new_to_date = date.today() + timedelta(days=5)
        payload = {"to_date": new_to_date}

        response = self.client.patch(reverse("booking-detail", kwargs={"pk": 1}), data=payload)

        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        booking = Booking.bookings.first()
        self.assertEqual(response.json(), BookingSerializer(booking).data)
        expected_price = (new_to_date - booking.from_date).days * booking.room.price
        self.assertEqual(response.json()["price"], expected_price)

    def test_delete_booking(self):

        self.create_a_booking()

        response = self.client.delete(reverse("booking-detail", kwargs={"pk": 1}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.bookings.all().count(), 0)

