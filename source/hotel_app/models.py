from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Room(models.Model):

    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=10, null=False)
    size = models.IntegerField(null=False)
    price = models.IntegerField(null=False)

    def __str__(self):
        return self.number


class Booking(models.Model):

    id = models.AutoField(primary_key=True)
    from_date = models.DateField(null=False)
    to_date = models.DateField(null=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    price = models.IntegerField(null=False)

    def save(self, *args, **kwargs):

        # calculate the price of the booking
        self.price = (self.to_date - self.from_date).days * self.room.price

        super().save(*args, **kwargs)

    def __str__(self):
        return self.customer.username