from django.contrib import admin
from django.forms import CheckboxSelectMultiple

from .models.booking_models import Booking
from .models.characteristic_models import (
    FacilitiesAndServicesHotels,
    FacilitiesAndServicesRooms,
    FoodCategory,
    HotelCategoryStars,
    Characteristics,
    Category
)
from .models.country_models import Country, City
from .models.hotel_models import Hotel, Room
from django.db import models


class CityInline(admin.TabularInline):
    model = City


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    inlines = [
        CityInline,
    ]


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    fields = ('country', 'city', 'hotel_name', 'category_id',
              'food_category', 'hotel_category', 'hotel_address',
              'hotel_description', 'room_id', 'checkin_date', 'checkout_date')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    field = '__all__'


admin.site.register(Category)
admin.site.register(FacilitiesAndServicesHotels)
admin.site.register(Booking)
admin.site.register(FoodCategory)
admin.site.register(HotelCategoryStars)
admin.site.register(FacilitiesAndServicesRooms)
admin.site.register(Characteristics)


