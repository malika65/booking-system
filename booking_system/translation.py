from modeltranslation.translator import translator, TranslationOptions
from booking_system.models.hotel_models import Hotel, Room
from booking_system.models.country_models import Country, City
from booking_system.models.characteristic_models import (
    FoodCategory,
    FacilitiesAndServicesHotels,
    FacilitiesAndServicesRooms,
    Category,
    Characteristics,
    HotelCategoryStars, AdditionalService, ChildService,
)


class HotelTranslationOptions(TranslationOptions):
    fields = ('hotel_name', 'hotel_address', 'hotel_description',)


class RoomTranslationOptions(TranslationOptions):
    fields = ('room_name', 'room_description')


class CountryTranslationOptions(TranslationOptions):
    fields = ('country_name',)


class CityTranslationOptions(TranslationOptions):
    fields = ('city_name',)


class FoodCategoryTranslationOptions(TranslationOptions):
    fields = ('food_category_name',)


class FacilitiesAndServicesHotelsTranslationOptions(TranslationOptions):
    fields = ('hotel_category_name',)


class FacilitiesAndServicesRoomsTranslationOptions(TranslationOptions):
    fields = ('room_category_name',)


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


class CharacteristicsTranslationOptions(TranslationOptions):
    fields = ('name',)


class HotelCategoryStarsTranslationOptions(TranslationOptions):
    fields = ('hotel_category_name',)


class AdditionalServiceTranslationOptions(TranslationOptions):
    fields = ('name',)


class ChildServiceTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Hotel, HotelTranslationOptions)
translator.register(Room, RoomTranslationOptions)
translator.register(Country, CountryTranslationOptions)
translator.register(City, CityTranslationOptions)
translator.register(AdditionalService, AdditionalServiceTranslationOptions)
translator.register(ChildService, ChildServiceTranslationOptions)
translator.register(FoodCategory, FoodCategoryTranslationOptions)
translator.register(FacilitiesAndServicesRooms, FacilitiesAndServicesRoomsTranslationOptions)
translator.register(FacilitiesAndServicesHotels, FacilitiesAndServicesHotelsTranslationOptions)
translator.register(Characteristics, CharacteristicsTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
translator.register(HotelCategoryStars, HotelCategoryStarsTranslationOptions)

