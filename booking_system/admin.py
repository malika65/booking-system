from re import A
from django.contrib import admin

from .models import (
    Hotel, 
    Country, 
    City, 
    Room, 
    # RoomType, 
    Booking, 
    FacilitiesAndServicesHotels,
    FacilitiesAndServicesRooms,
    FoodCategory,
    HotelCategoryStars,
    Characteristics,
)


class CityInline(admin.TabularInline):
    model = City


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    inlines = [
        CityInline,
    ]



@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    fields = ('country', 'city', 'hotel_name', 'category_id', 'food_category', 'hotel_category', 'hotel_address', 'hotel_description', 'hotel_phone', 'room_id')



admin.site.register(FacilitiesAndServicesHotels)
admin.site.register(Booking)
admin.site.register(FoodCategory)
admin.site.register(HotelCategoryStars)
admin.site.register(FacilitiesAndServicesRooms)
admin.site.register(Room)
admin.site.register(Characteristics)


