from django.contrib import admin

from .models import Flight

class FlightAdmin(admin.ModelAdmin):
    list_display = ( 'FlightId', 'companyName', 'sourceLocation', 'destinationLocation', 'departureDate', 'departureTime','classtype', 'price', 'numSeatsRemaining')
    search_fields= ('companyName', 'FlightId', 'sourceLocation', 'destinationLocation', 'departureDate', 'departureTime',)
    
    # filter_horizontal = ()
    # list_filter = ()
    # fieldsets = ()

admin.site.register(Flight, FlightAdmin)