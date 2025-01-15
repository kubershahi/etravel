from django.db import models

# Create your models here.


class Hotel(models.Model):
    image = models.URLField(default='')
    hotelName = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    roomType = models.CharField(default="", max_length=30)
    roomsLeft = models.IntegerField(default=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.hotelName
