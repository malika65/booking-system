from rest_framework import serializers

from .models import Hotel, Room, Booking, Country, City, FoodCategory, HotelCategoryStars, FacilitiesAndServicesHotels, \
    Characteristics, FacilitiesAndServicesRooms


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
        fields = ('room_category_name', )


class CharacteristicsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Characteristics
        fields = ('name', 'capacity')


class RoomSerializer(serializers.ModelSerializer):
    category_id = FacilitiesAndServicesRoomsSerializer(read_only=True, many=True)
    characteristics_id = CharacteristicsSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        fields = ('room_name', 'room_no', 'room_description', 'price', 'category_id', 'characteristics_id')


class FoodCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodCategory
        fields = "__all__"


class HotelCategoryStarsSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelCategoryStars
        fields = ('hotelcategory_name', 'hotelcategory_stars')


class FacilitiesAndServicesHotelsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FacilitiesAndServicesHotels
        fields = ('hotel_category_name', )


class HotelSerializer(serializers.Serializer):
    hotel_name = serializers.CharField(max_length=100)
    hotel_address = serializers.CharField(max_length=100)
    hotel_description = serializers.CharField(max_length=2500)
    hotel_phone = serializers.CharField(max_length=100)
    is_active = serializers.BooleanField(default=True)
    city = CitySerializer()
    food_category = FoodCategorySerializer(read_only=True, many=True)
    hotel_category = HotelCategoryStarsSerializer(read_only=True, many=True)
    category_id = FacilitiesAndServicesHotelsSerializer(read_only=True, many=True)
    room_id = RoomSerializer(read_only=True, many=True)

    class Meta:
        model = Hotel
        fields = ('hotel_name', 'hotel_address', 'hotel_description', 'hotel_phone', 'is_active', 'city',
                  'hotel_category', 'food_category', 'category_id', 'room_id')


class BookingSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer()
    room = RoomSerializer()

    class Meta:
        model  = Booking
        fields = ('guest_id', 'checkin_date', 'checkout_date', 'hotel', 'room', 'num_of_guest', 'is_checkout')
