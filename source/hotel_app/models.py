from django.db import models
from django.contrib.auth import get_user_model
from datetime import date
# Create your models here.

User = get_user_model()


def calculate_price(from_date: date, to_date: date, room_price: int) -> int:
    """
    Calculate the booking price.
    """

    price = (to_date - from_date).days * room_price

    if price < 0:
        raise ValueError("Booking price is negative")

    return price


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


class Booking(models.Model):

    id = models.AutoField(primary_key=True)
    from_date = models.DateField(null=False)
    to_date = models.DateField(null=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    price = models.IntegerField(null=False)

    class Meta:

        constraints = [
            models.CheckConstraint( # booking days must be > 0
                check=models.Q(to_date__gt=models.F("from_date")),
                name='booking_days_check'),
        ]

    def save(self, *args, **kwargs):

        # calculate price of booking before saving
        self.price = calculate_price(self.from_date, self.to_date, self.room.price)

        super().save(*args, **kwargs)


    def __str__(self):
        return self.customer.email