from rest_framework import serializers
from rest_framework.fields import Field

from authe.serializers import UserSerializer
from .models.booking_models import Booking
from .models.characteristic_models import (
    FoodCategory,
    HotelCategoryStars,
    FacilitiesAndServicesHotels,
    Characteristics,
    FacilitiesAndServicesRooms, Category, AdditionalService, ChildService
)
from .models.country_models import Country, City
from .models.hotel_models import Hotel, Room, HotelImage


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('country_name_ru', 'country_name_en')


class CitySerializer(serializers.ModelSerializer):
    country_id = CountrySerializer()

    class Meta:
        model = City
        fields = ('city_name_ru', 'city_name_en', 'country_id')


class FacilitiesAndServicesRoomsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FacilitiesAndServicesRooms
        fields = ('id', 'room_category_name_ru', 'room_category_name_en')


class CharacteristicsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Characteristics
        fields = ('id', 'name_ru', 'name_en', 'capacity')


class AdditionalServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdditionalService
        fields = ('id', 'name_ru', 'name_en', 'price', 'currency')


class ChildServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChildService
        fields = ('id', 'name_ru', 'name_en', 'until_age', 'price', 'currency')


class RoomSerializer(serializers.ModelSerializer):
    category_id = FacilitiesAndServicesRoomsSerializer(read_only=True, many=True)
    characteristics_id = CharacteristicsSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        fields = ('id', 'room_name_ru', 'room_name_en', 'room_description_ru',
                  'room_description_en', 'price', 'category_id', 'characteristics_id', 'child_capacity')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name_ru', 'name_en')


class FoodCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodCategory
        fields = ('food_category_name_ru', 'food_category_name_en')


class HotelCategoryStarsSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelCategoryStars
        fields = ('id', 'hotel_category_name_ru', 'hotel_category_name_en', 'hotel_category_stars')


class FacilitiesAndServicesHotelsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FacilitiesAndServicesHotels
        fields = ('id', 'hotel_category_name_ru', 'hotel_category_name_en')


class HotelImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelImage
        fields = ['id', 'image_url']


class HotelSerializer(serializers.ModelSerializer):
    hotel_name_ru = serializers.CharField(max_length=100)
    hotel_name_en = serializers.CharField(max_length=100)
    hotel_address_ru = serializers.CharField(max_length=100)
    hotel_address_en = serializers.CharField(max_length=100)
    hotel_description_ru = serializers.CharField(max_length=2500)
    hotel_description_en = serializers.CharField(max_length=2500)
    is_active = serializers.BooleanField(default=True)
    city = CitySerializer()
    food_category = FoodCategorySerializer(read_only=True, many=True)
    hotel_category = HotelCategoryStarsSerializer(read_only=True, many=True)
    category_id = FacilitiesAndServicesHotelsSerializer(read_only=True, many=True)
    additional_service_id = AdditionalServiceSerializer(read_only=True, many=True)
    child_service_id = ChildServiceSerializer(read_only=True, many=True)
    room_id = RoomSerializer(read_only=True, many=True)
    images = HotelImageSerializer(many=True)

    class Meta:
        model = Hotel
        fields = ['hotel_name_ru', 'hotel_name_en', 'hotel_address_ru', 'hotel_address_en',
                  'hotel_description_ru', 'hotel_description_en', 'is_active', 'city',
                  'hotel_category', 'food_category', 'category_id', 'room_id', 'checkin_date', 'checkout_date',
                  'additional_service_id', 'child_service_id', 'images', 'total']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation


class BookingSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer(read_only=True)
    guest_id = UserSerializer()
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ('guest_id', 'checkin_date', 'checkout_date', 'hotel', 'room', 'num_of_guest')