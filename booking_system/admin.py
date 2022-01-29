from django.contrib import admin

from .models import (
    Hotel, 
    Country, 
    City, 
    Room, 
    RoomType, 
    Booking, 
    Category,
    FoodCategory,
    HotelCategory,
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
    fields = ('country', 'city', 'hotel_name', 'category_id', 'food_category', 'hotel_category', 'hotel_address', 'hotel_description', 'hotel_phone',)


class RoomTypeInline(admin.TabularInline):
    model = RoomType


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = [
        RoomTypeInline,
    ]


admin.site.register(Category)
admin.site.register(Booking)
admin.site.register(FoodCategory)
admin.site.register(HotelCategory)

