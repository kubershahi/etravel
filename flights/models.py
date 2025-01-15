from django.db import models


class Flight(models.Model):
    Logo = models.URLField(default='')
    companyName = models.CharField(max_length=30)
    FlightId = models.CharField(max_length=30, null=True)
    sourceLocation = models.CharField(max_length=30)
    destinationLocation = models.CharField(max_length=30)
    departureDate = models.DateField()
    departureTime = models.TimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    classtype = models.CharField(max_length=30)
    numSeatsRemaining = models.IntegerField(default=50)

    def __str__(self):
        return self.FlightId
