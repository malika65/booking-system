import datetime
import itertools
import json

from django.core.serializers import serialize
from django.db.models import Prefetch
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from rest_framework import serializers
from rest_framework.fields import Field
from rest_framework.response import Response

from authe.models import User
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
from .models.hotel_models import Hotel, Room, HotelImage, PeriodPrice


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


class PeriodPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PeriodPrice
        fields = ('id', 'price', 'currency', 'start_date', 'end_date')


class RoomSerializer(serializers.ModelSerializer):
    category_id = FacilitiesAndServicesRoomsSerializer(read_only=True, many=True)
    characteristics_id = CharacteristicsSerializer(read_only=True, many=True)
    prices = PeriodPriceSerializer(many=True)

    class Meta:
        model = Room
        fields = ('id', 'room_name_ru', 'room_name_en', 'room_description_ru',
                  'room_description_en', 'category_id', 'prices', 'characteristics_id', 'child_capacity')


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
    category_id = CategorySerializer(read_only=True)

    class Meta:
        model = FacilitiesAndServicesHotels
        fields = ('id', 'hotel_category_name_ru', 'hotel_category_name_en', 'category_id')


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
    city = CitySerializer(many=True)
    food_category = FoodCategorySerializer(read_only=True, many=True)
    hotel_category = HotelCategoryStarsSerializer(read_only=True, many=True)
    category_id = FacilitiesAndServicesHotelsSerializer(read_only=True, many=True)
    additional_service_id = AdditionalServiceSerializer(read_only=True, many=True)
    child_service_id = ChildServiceSerializer(read_only=True, many=True)
    room_id = RoomSerializer(read_only=True, many=True)
    images = HotelImageSerializer(many=True)

    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name_ru', 'hotel_name_en', 'hotel_address_ru', 'hotel_address_en',
                  'hotel_description_ru', 'hotel_description_en', 'is_active', 'city',
                  'hotel_category', 'food_category', 'category_id', 'room_id', 'checkin_date', 'checkout_date',
                  'additional_service_id', 'child_service_id', 'images']


class HotelSearchSerializer(serializers.ModelSerializer):
    hotel_name_ru = serializers.CharField(max_length=100)
    hotel_name_en = serializers.CharField(max_length=100)
    hotel_address_ru = serializers.CharField(max_length=100)
    hotel_address_en = serializers.CharField(max_length=100)
    hotel_description_ru = serializers.CharField(max_length=2500)
    hotel_description_en = serializers.CharField(max_length=2500)
    is_active = serializers.BooleanField(default=True)
    city = CitySerializer(many=True)
    food_category = FoodCategorySerializer(read_only=True, many=True)
    hotel_category = HotelCategoryStarsSerializer(read_only=True, many=True)
    category_id = FacilitiesAndServicesHotelsSerializer(read_only=True, many=True)
    additional_service_id = AdditionalServiceSerializer(read_only=True, many=True)
    child_service_id = ChildServiceSerializer(read_only=True, many=True)
    # room_id = RoomSerializer(read_only=True, many=True)
    images = HotelImageSerializer(many=True)
    # child_years = serializers.CharField(required=False)
    # room_amount = serializers.IntegerField(min_value=1, required=False)
    # room_capacity = serializers.IntegerField(min_value=1, required=False)
    # room_capacity_child = serializers.IntegerField(min_value=1, required=False)
    guests = serializers.CharField(required=False)

    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name_ru', 'hotel_name_en', 'hotel_address_ru', 'hotel_address_en',
                  'hotel_description_ru', 'hotel_description_en', 'is_active', 'city',
                  'hotel_category', 'food_category', 'category_id', 'checkin_date', 'checkout_date',
                  'additional_service_id', 'child_service_id', 'images', 'guests']

    @staticmethod
    def get_room_price_depends_on_capacity(representation, capacity):
        for room in representation['room_id']:
            for characteristics_id in room['characteristics_id']:
                if capacity == characteristics_id['capacity']:
                    for date_price in room['prices']:
                        today = datetime.datetime.today()
                        start = datetime.datetime.strptime(date_price['start_date'], '%Y-%m-%d')
                        end = datetime.datetime.strptime(date_price['end_date'], '%Y-%m-%d')
                        if start <= today <= end:
                            return date_price['price']

    @staticmethod
    def get_room_price_depends_on_child_capacity(representation, capacity):
        for room in representation['room_id']:
            if capacity == room['child_capacity']:
                for date_price in room['prices']:
                    today = datetime.datetime.today()
                    start = datetime.datetime.strptime(date_price['start_date'], '%Y-%m-%d')
                    end = datetime.datetime.strptime(date_price['end_date'], '%Y-%m-%d')
                    if start <= today <= end:
                        return date_price['price']

    @staticmethod
    def get_child_service_price(representation, capacity):
        pass

    @staticmethod
    def get_rooms_for_capacity(hotel_id, capacity):
        room = Room.objects.filter(rooms__id=hotel_id, characteristics_id__capacity=capacity)
        # aa = room.last()
        # print(room.values()))
        room = RoomSerializer(room, many=True)
        serialized_data = {'data': room.data}
        return Response(serialized_data)

    def to_representation(self, instance):
        filters_in_request = self.context['request']
        total_rooms_price = []
        representation = super().to_representation(instance)
        guests_room = filters_in_request.GET['guests'].split('-')
        num_of_guests_in_room = []
        child_years = []
        for room in guests_room:
            num_of_guests_in_room.append(int(room.split('and')[0]))
            if len(room.split('and')) > 1:
                child_years.append((room.split('and'))[1].split('.'))
                child_years = list(itertools.chain(*child_years))
        child_years = [int(i) for i in child_years]
        rooms = {}
        for guest in num_of_guests_in_room:
            room = self.get_rooms_for_capacity(representation.get('id'), guest)
            # print(room)
            rooms[f'room{guest.numerator}'] = room.data

        # print(rooms)
        representation['total'] = rooms
        # print(representation['total'])
        # print(representation)
        # print(child_room_capacity)
        # print(child_years)
        # print(list(filter(lambda v: sum(v) == 5, self.powerset([i for i in range(1, 5)]))))
        # print(total_rooms_price)
        # representation['total'] = sum(total_rooms_price)
        return representation


class HotelBookingSerializer(serializers.ModelSerializer):
    hotel_name_ru = serializers.CharField(max_length=100)
    hotel_address_ru = serializers.CharField(max_length=100)
    hotel_description_ru = serializers.CharField(max_length=2500)
    is_active = serializers.BooleanField(default=True)
    city = CitySerializer()
    child_service_id = ChildServiceSerializer(read_only=True, many=True)
    room_id = RoomSerializer(read_only=True, many=True)

    class Meta:
        model = Hotel
        fields = ('hotel_name_ru', 'hotel_name_en', 'hotel_address_ru', 'hotel_description_ru', 'is_active',
                  'city', 'room_id', 'checkin_date', 'checkout_date', 'child_service_id')


class BookingSerializer(serializers.ModelSerializer):
    hotel = serializers.StringRelatedField()
    guest_id = serializers.StringRelatedField()
    room = serializers.StringRelatedField()

    class Meta:
        model = Booking
        fields = ('guest_id', 'checkin_date', 'checkout_date', 'hotel', 'room', 'num_of_guest')

