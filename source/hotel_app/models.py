from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Room(models.Model):

    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=10)
    size = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.number


class Booking(models.Model):

    id = models.AutoField(primary_key=True)
    from_date = models.DateField()
    to_date = models.DateField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return self.customer.username