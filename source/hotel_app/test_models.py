from unittest import skip

from django.db import IntegrityError
from django.test import TestCase
from .models import Room, Booking, calculate_price
from django.contrib.auth import get_user_model
from datetime import date, timedelta

User = get_user_model()


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


class BookingTests(TestCase):

    @staticmethod
    def create_user_and_room():

        room = Room.objects.create(number="Room 1", size=25, price=100)
        user = User.objects.create(email="testuser@example.com", password="testpassword")

        return room, user

    def test_booking_str_representation(self):

        room, user =  self.create_user_and_room()
        from_date = date.today()
        to_date = date.today() + timedelta(days=10)

        Booking.objects.create(customer=user, room=room, from_date=from_date, to_date=to_date)

        self.assertEqual(str(Booking.objects.first()), user.email)

    @skip
    def test_to_date_cant_be_less_than_or_equal_to_from_date(self):

        room, user = self.create_user_and_room()

        from_date = date.today()
        wrong_to_date = date.today() - timedelta(days=10) # to_date is less than from_date

        with self.assertRaises(IntegrityError):
            Booking.objects.create(customer=user, room=room, from_date=from_date, to_date=wrong_to_date)

    def test_booking_price(self):

        from_date = date.today()
        to_date = date.today() + timedelta(days=10)
        room_price = 100

        expected_price = 1000

        self.assertEqual(calculate_price(from_date, to_date, room_price), expected_price)

    def test_booking_price_cant_be_less_than_0(self):

        from_date = date.today()
        wrong_to_date = date.today() - timedelta(days=10) # to_date is less than from_date
        room_price = 100

        with self.assertRaises(ValueError):
            calculate_price(from_date, wrong_to_date, room_price)
