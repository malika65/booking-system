from rest_framework import serializers

from authe.serializers import UserSerializer
from .models.booking_models import Booking
from .models.characteristic_models import (
    FoodCategory,
    HotelCategoryStars,
    FacilitiesAndServicesHotels,
    Characteristics,
    FacilitiesAndServicesRooms, Category
)
from .models.country_models import Country, City
from .models.hotel_models import Hotel, Room


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    country_id = CountrySerializer()

    class Meta:
        model = City
        fields = ('city_name', 'postal_code', 'country_id')


class FacilitiesAndServicesRoomsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FacilitiesAndServicesRooms
        fields = ('id', 'room_category_name', )


class CharacteristicsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Characteristics
        fields = ('id', 'name', 'capacity')


class RoomSerializer(serializers.ModelSerializer):
    category_id = FacilitiesAndServicesRoomsSerializer(read_only=True, many=True)
    characteristics_id = CharacteristicsSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        fields = ('id', 'room_name', 'room_no', 'room_description', 'price', 'category_id', 'characteristics_id')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class FoodCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodCategory
        fields = "__all__"


class HotelCategoryStarsSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelCategoryStars
        fields = ('id', 'hotel_category_name', 'hotel_category_stars')


class FacilitiesAndServicesHotelsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FacilitiesAndServicesHotels
        fields = ('id', 'hotel_category_name', )


class HotelSerializer(serializers.Serializer):
    hotel_name = serializers.CharField(max_length=100)
    hotel_address = serializers.CharField(max_length=100)
    hotel_description = serializers.CharField(max_length=2500)
    is_active = serializers.BooleanField(default=True)
    city = CitySerializer()
    food_category = FoodCategorySerializer(read_only=True, many=True)
    hotel_category = HotelCategoryStarsSerializer(read_only=True, many=True)
    category_id = FacilitiesAndServicesHotelsSerializer(read_only=True, many=True)
    room_id = RoomSerializer(read_only=True, many=True)

    class Meta:
        model = Hotel
        fields = ('hotel_name', 'hotel_address', 'hotel_description', 'is_active', 'city',
                  'hotel_category', 'food_category', 'category_id', 'room_id', 'checkin_date', 'checkout_date')


class BookingSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer(read_only=True)
    guest_id = UserSerializer()
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ('guest_id', 'checkin_date', 'checkout_date', 'hotel', 'room', 'num_of_guest')