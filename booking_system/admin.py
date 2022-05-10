from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

from .models.booking_models import Booking
from .models.characteristic_models import (
    FacilitiesAndServicesHotels,
    FacilitiesAndServicesRooms,
    FoodCategory,
    HotelCategoryStars,
    Characteristics,
    Category, AdditionalService, ChildService
)
from .models.country_models import Country, City
from .models.hotel_models import Hotel, Room, HotelImage
from django.db import models


class CityInline(TranslationTabularInline):
    model = City


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    inlines = [
        CityInline,
    ]


class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 3


@admin.register(Hotel)
class HotelAdmin(TranslationAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    field = '__all__'
    inlines = [HotelImageInline, ]


@admin.register(Room)
class RoomAdmin(TranslationAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    field = '__all__'


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    field = '__all__'


@admin.register(FacilitiesAndServicesHotels)
class FacilitiesAndServicesHotelsAdmin(TranslationAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    field = '__all__'


@admin.register(FoodCategory)
class FoodCategoryAdmin(TranslationAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    field = '__all__'


@admin.register(HotelCategoryStars)
class HotelCategoryStarsAdmin(TranslationAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    field = '__all__'


@admin.register(FacilitiesAndServicesRooms)
class FacilitiesAndServicesRoomsAdmin(TranslationAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    field = '__all__'


@admin.register(Characteristics)
class CharacteristicsAdmin(TranslationAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    field = '__all__'


@admin.register(AdditionalService)
class AdditionalServiceAdmin(TranslationAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    field = '__all__'


@admin.register(ChildService)
class ChildServiceAdmin(TranslationAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    field = '__all__'


admin.site.register(Booking)