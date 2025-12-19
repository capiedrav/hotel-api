from django.db import IntegrityError
from django.test import TestCase
from .models import Room, Booking, calculate_booking_price
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from unittest.mock import patch


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


    def setUp(self):

        self.from_date = date(2025, 12, 1)
        self.to_date = date(2025, 12, 11)

    @staticmethod
    def create_user_and_room():

        room = Room.objects.create(number="Room 1", size=25, price=100)
        user = User.objects.create(email="testuser@example.com", password="testpassword")

        return room, user

    def test_booking_str_representation(self):

        room, user =  self.create_user_and_room()

        Booking.bookings.create(customer=user, room=room, from_date=self.from_date, to_date=self.to_date)

        self.assertEqual(str(Booking.bookings.first()), user.email)

    def test_to_date_cant_be_less_than_or_equal_to_from_date(self):

        room, user = self.create_user_and_room()
        wrong_to_date =self.from_date - timedelta(days=10) # to_date is less than from_date

        with self.assertRaises(IntegrityError):
            Booking.bookings.create(customer=user, room=room, from_date=self.from_date, to_date=wrong_to_date)

    def test_calculate_booking_price_function(self):

        room_price = 100
        expected_price = 1000

        self.assertEqual(calculate_booking_price(self.from_date, self.to_date, room_price), expected_price)

    @patch("hotel_app.models.calculate_booking_price")
    def test_booking_price_cant_be_less_than_or_equal_to_0(self, mocked_calculate_booking_price):

        room, user = self.create_user_and_room()
        mocked_calculate_booking_price.return_value = 0 # wrong booking price

        with self.assertRaises(IntegrityError):
            Booking.bookings.create(customer=user, from_date=self.from_date, to_date=self.to_date, room=room)

        mocked_calculate_booking_price.assert_called_once()

    def test_update_booking_method(self):

        room, user = self.create_user_and_room()

        booking = Booking.bookings.create(
            customer=user,
            from_date=self.from_date,
            to_date=self.to_date,
            room=room
        )
        new_to_date = date(2025,12,15)
        expected_price = 1400
        booking.update_booking(from_date=self.from_date, to_date=new_to_date, room=room)

        self.assertEqual(booking.to_date, new_to_date)
        self.assertEqual(booking.price, expected_price)

    def test_create_booking_class_method_doesnt_save(self):

        room, user = self.create_user_and_room()

        booking = Booking.create_booking(
            customer=user,
            from_date=self.from_date,
            to_date=self.to_date,
            room=room
        )

        self.assertEqual(Booking.bookings.count(), 0)
