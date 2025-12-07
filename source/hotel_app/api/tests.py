from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Room
from .serializers import RoomSerializer

# Create your tests here.


class APITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    @staticmethod
    def create_rooms():
        rooms = []
        for i in range(1, 11):
            rooms.append(Room(number=f"Room {i}", size=25, price=100))

        Room.objects.bulk_create(rooms)

    def test_api_root(self):

        response = self.client.get(reverse("api-root"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'), "Hello, World!")

    def test_list_rooms(self):

        self.create_rooms()

        response = self.client.get(reverse('list-rooms'))

        rooms = Room.objects.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), RoomSerializer(rooms, many=True).data)