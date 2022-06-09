from rest_framework import serializers

from booking_system.currency_convert import CurrencyExchangeService
from booking_system.models.characteristic_models import (
    FoodCategory,
    HotelCategoryStars,
    FacilitiesAndServicesHotels,
    Characteristics,
    FacilitiesAndServicesRooms, Category, AdditionalService, ChildService
)
from booking_system.models.country_models import Country, City
from booking_system.models.hotel_models import PeriodPrice

currency_exchange = CurrencyExchangeService()


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
        fields = ('id', 'name_ru', 'name_en', 'until_age', 'price', 'currency', 'is_discount')

    def to_representation(self, instance):
        filters_in_request = self.context['request']
        currency_to = filters_in_request.GET['currency_to_convert']
        child_services = super().to_representation(instance)
        if 'is_discount' in child_services and child_services['is_discount']:
            child_room_price = child_services['price']/100
        else:
            child_room_price = child_services['price']
        currency_from = child_services['currency']
        converted = currency_exchange.get_rates_from_api()
        rates = [d[currency_from] for d in converted if currency_from in d]
        rate = [d[currency_to] for d in rates][0]
        result = child_room_price * rate
        child_services['result_price'] = result
        return child_services


class PeriodPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PeriodPrice
        fields = ('id', 'price', 'currency', 'start_date', 'end_date')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name_ru', 'name_en')


class FoodCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodCategory
        fields = ('id', 'food_category_name_ru', 'food_category_name_en')


class HotelCategoryStarsSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelCategoryStars
        fields = ('id', 'hotel_category_name_ru', 'hotel_category_name_en', 'hotel_category_stars')


class FacilitiesAndServicesHotelsSerializer(serializers.ModelSerializer):
    category_id = CategorySerializer(read_only=True)

    class Meta:
        model = FacilitiesAndServicesHotels
        fields = ('id', 'hotel_category_name_ru', 'hotel_category_name_en', 'category_id')
