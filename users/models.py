from django.db import models

from django.contrib.auth.models import User
from flights.models import Flight
from hotels.models import Hotel

class GuestEmail(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

class UserBookings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userflights = models.ManyToManyField(Flight, blank=True, related_name="userflights")
    userhotels = models.ManyToManyField(Hotel, blank=True, related_name="userhotesl")
    
    def __str__(self):
        return self.user.username