from django.contrib import admin

from .models import Guest, Hotel, Room, Booking

admin.site.register(Guest)
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Booking)
