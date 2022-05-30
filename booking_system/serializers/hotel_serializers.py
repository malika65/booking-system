import datetime

from rest_framework import serializers

from booking_system.models.hotel_models import PeriodPrice, HotelImage, Hotel, Room
from booking_system.serializers.characteristics_serializers import CitySerializer, FoodCategorySerializer, \
    HotelCategoryStarsSerializer, FacilitiesAndServicesHotelsSerializer, AdditionalServiceSerializer, \
    ChildServiceSerializer, FacilitiesAndServicesRoomsSerializer, CharacteristicsSerializer, PeriodPriceSerializer, \
    currency_exchange


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
    images = HotelImageSerializer(many=True)

    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name_ru', 'hotel_name_en', 'hotel_address_ru', 'hotel_address_en',
                  'hotel_description_ru', 'hotel_description_en', 'is_active', 'city',
                  'hotel_category', 'food_category', 'category_id', 'checkin_date', 'checkout_date',
                  'additional_service_id', 'child_service_id', 'images']


class RoomSerializer(serializers.ModelSerializer):
    category_id = FacilitiesAndServicesRoomsSerializer(read_only=True, many=True)
    characteristics_id = CharacteristicsSerializer(read_only=True, many=True)
    prices = PeriodPriceSerializer(many=True)
    currency_to_convert = serializers.CharField(required=False)
    hotel_id = HotelSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ('id', 'room_name_ru', 'room_name_en', 'room_description_ru',
                  'room_description_en', 'category_id', 'prices', 'characteristics_id',
                  'child_capacity', 'currency_to_convert', 'hotel_id')

    @staticmethod
    def get_room_price_depends_on_datetime(representation):
        for date_price in representation['prices']:
            today = datetime.datetime.today()
            start = datetime.datetime.strptime(date_price['start_date'], '%Y-%m-%d')
            end = datetime.datetime.strptime(date_price['end_date'], '%Y-%m-%d')
            if start <= today <= end:
                return date_price

    def to_representation(self, instance):
        filters_in_request = self.context['request']
        currency_to = filters_in_request.GET['currency_to_convert']
        rooms = super().to_representation(instance)
        actual_room_price = self.get_room_price_depends_on_datetime(rooms)
        currency_from = actual_room_price['currency']
        amount = actual_room_price['price']
        converted = currency_exchange.get_rates_from_api()
        rates = [d[currency_from] for d in converted if currency_from in d]
        rate = [d[currency_to] for d in rates][0]
        result = amount * rate
        rooms['result_price'] = result
        return rooms


class HotelSearchSerializer(serializers.ModelSerializer):
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
    images = HotelImageSerializer(many=True)
    guests = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name_ru', 'hotel_name_en', 'hotel_address_ru', 'hotel_address_en',
                  'hotel_description_ru', 'hotel_description_en', 'is_active', 'city',
                  'hotel_category', 'food_category', 'category_id', 'checkin_date', 'checkout_date',
                  'additional_service_id', 'child_service_id', 'images', 'guests']

    @staticmethod
    def get_room_price_depends_on_datetime(prices):
        for price in prices:
            today = datetime.datetime.today()
            start = datetime.datetime.strptime(str(price.start_date), '%Y-%m-%d')
            end = datetime.datetime.strptime(str(price.end_date), '%Y-%m-%d')
            if start <= today <= end:
                return price.price

    @staticmethod
    def check_if_child_service_exist(childs, child_services):
        adults = 0
        rest_childs = []
        for child in childs:
            services_ages = [i.get('until_age') for i in child_services]
            if services_conditions := [i for i in services_ages if int(child)<=i]:
                rest_childs.append(min(services_conditions))
            else:
                adults += 1
        return adults, rest_childs

    @staticmethod
    def get_child_service_prices(child_years, child_services):
        result = 0
        years = [i.get('until_age') for i in child_services]
        prices = [i.get('result_price') for i in child_services]
        zip_iterator = zip(years, prices)
        prices_dictionary = dict(zip_iterator)
        for index, child_year in enumerate(child_years):
            if child_year in prices_dictionary:
                result += prices_dictionary[child_year]
        return result

    def to_representation(self, instance):
        filters_in_request = self.context['request']
        total_rooms_price = 0
        representation = super().to_representation(instance)
        guests_in_room = filters_in_request.GET['guests'].split('-')
        rooms_with_guest = []
        for guest in guests_in_room:
            s = {}
            s[guest.split('and')[0]] = guest.split('and')[1].split('.')
            rooms_with_guest.append(s)
        rooms = {}
        child_service = representation.get('child_service_id')
        for index, room_guests in enumerate(rooms_with_guest):
            childs = room_guests.values()
            adults, rest_childs = self.check_if_child_service_exist(*childs, child_service)
            new_key = adults + int(list(room_guests)[0])
            room_guests[new_key] = room_guests.pop(list(room_guests)[0])
            room_guests[new_key] = rest_childs
        try:
            for room_index, adult_and_child in enumerate(rooms_with_guest, start=1):
                adult = list(adult_and_child.keys())[0]
                child = len(list(adult_and_child.values())[0])
                room = Room.objects.select_related('hotel_id').filter(hotel_id=representation.get('id'),
                                                                      characteristics_id__capacity=adult,
                                                                      child_capacity=child)
                prices = PeriodPrice.objects.filter(room_id__id=room.values('id').last()['id'])
                actual_price = self.get_room_price_depends_on_datetime(prices)
                total_rooms_price += actual_price
                child_years = list(adult_and_child.values())[0]
                for index, child in enumerate(child_years):

                    if child_service[index].get('until_age') == int(child):
                        total_rooms_price += child_service[index].get('result_price')
                room = RoomSerializer(room, many=True, context=self.context)
                rooms[f'room{room_index}'] = room.data[0]

                total_rooms_price += self.get_child_service_prices(child_years, child_service)

            representation['result'] = rooms
            representation['total_price'] = total_rooms_price
            return representation
        except TypeError as e:
            representation['result'] = {'message': 'Nothing'}
            return representation
