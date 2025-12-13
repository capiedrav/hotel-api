from django.db import IntegrityError
from django.test import TestCase
from .models import Room, Booking


class RoomTests(TestCase):

    def test_room_str_representation(self):

        room_number = "Room 1"
        room = Room.objects.create(number=room_number, size=25, price=100)

        self.assertEqual(str(room), room_number)

    def test_room_size_greater_than_0_is_ok(self):

        room_size = 25
        Room.objects.create(number="Room 1", size=room_size, price=100)

        self.assertEqual(Room.objects.count(), 1)

    def test_room_size_cant_be_less_than_or_equal_to_0(self):

        room_size = 0 # wrong size

        with self.assertRaises(IntegrityError):
            Room.objects.create(number="Room 1", size=room_size, price=100)

    def test_room_price_greater_than_0_is_ok(self):

        room_price = 100
        Room.objects.create(number="Room 1", size=25, price=room_price)

        self.assertEqual(Room.objects.count(), 1)

    def test_room_price_cant_be_less_than_or_equal_to_0(self):

        room_price = 0 # wrong price

        with self.assertRaises(IntegrityError):
            Room.objects.create(number="Room 1", size=25, price=room_price)


