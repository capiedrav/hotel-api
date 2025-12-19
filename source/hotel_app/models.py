from django.db import models
from django.contrib.auth import get_user_model
from datetime import date, datetime

# Create your models here.

User = get_user_model()


class Room(models.Model):

    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=10, null=False)
    size = models.IntegerField(null=False)
    price = models.IntegerField(null=False)

    class Meta:

        constraints = [
            models.CheckConstraint(check=models.Q(size__gt=0), name='room_size_check'), # room size must be > 0
            models.CheckConstraint(check=models.Q(price__gt=0), name='room_price_check'), # room price must be > 0
        ]

    def __str__(self):
        return self.number


def calculate_booking_price(from_date: date, to_date: date, room_price: int) -> int:
    """
    Calculate the booking price.
    """

    price = (to_date - from_date).days * room_price

    return price


class BookingManager(models.Manager):

    def create(self, customer: User, from_date: date, to_date: date, room: Room) -> "Booking":

        booking_price = calculate_booking_price(from_date, to_date, room.price)
        booking = self.model(customer=customer, from_date=from_date, to_date=to_date, room=room, price=booking_price)
        booking.save()

        return booking


class Booking(models.Model):

    id = models.AutoField(primary_key=True)
    from_date = models.DateField(null=False)
    to_date = models.DateField(null=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    price = models.IntegerField(null=False)
    bookings = BookingManager() # default object manager

    class Meta:

        constraints = [
            models.CheckConstraint(  # booking days must be > 0 (to_date > from_date)
                check=models.Q(to_date__gt=models.F("from_date")),
                name='booking_days_check'
            ),
            models.CheckConstraint( # booking price must be > 0
                check=models.Q(price__gt=0),
                name='booking_price_check'
            ),
        ]

    @classmethod
    def create_booking(cls, customer: User, from_date: date, to_date: date, room: Room) -> "Booking":
        """
        Create a new booking (not saved into the database). Used primarily with bulk_create method.
        """

        booking_price = calculate_booking_price(from_date, to_date, room.price)
        booking = Booking(customer=customer, from_date=from_date, to_date=to_date, room=room, price=booking_price)

        return booking

    def update_booking(self, from_date: date=None, to_date: date=None, room: Room=None) -> None:

        fields_to_update = []

        # update fields
        if from_date is not None and self.from_date != from_date:
            self.from_date = from_date
            fields_to_update.append("from_date")
        if to_date is not None and self.to_date != to_date:
            self.to_date = to_date
            fields_to_update.append("to_date")
        if room is not None and self.room != room:
            self.room = room
            fields_to_update.append("room")

        if fields_to_update:
            # recalculate booking price
            self.price = calculate_booking_price(self.from_date, self.to_date, self.room.price)
            fields_to_update.append("price")

            self.save(update_fields=fields_to_update)

    def __str__(self):
        return self.customer.email