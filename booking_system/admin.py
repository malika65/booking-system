from django.contrib import admin

from .models import Hotel, Country, City, Room, RoomType, Booking, Category

admin.site.register(Category)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Hotel)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Booking)

