from django.contrib import admin

# Register your models here.
from .models import Hotel


class HotelAdmin(admin.ModelAdmin):
    list_display = ('hotelName', 'location', 'roomType', 'roomsLeft', 'price', )
    search_fields = ('hotelName', 'location', 'roomType', 'roomsLeft',)


admin.site.register(Hotel, HotelAdmin)
