from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Room
from .serializers import RoomSerializer
from .views import RootAPIView, RoomViewSet


# Create your tests here.


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