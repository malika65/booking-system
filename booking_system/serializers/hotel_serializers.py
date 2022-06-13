import datetime

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers

from booking_system.documents import HotelDocument
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


class HotelSearchSerializer(DocumentSerializer):
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
        document = HotelDocument
        fields = ('id', 'hotel_name_ru', 'hotel_name_en', 'hotel_address_ru', 'hotel_address_en',
                  'hotel_description_ru', 'hotel_description_en', 'is_active', 'city',
                  'hotel_category', 'food_category', 'facilities_hotel_id', 'checkin_date', 'checkout_date',
                  'additional_service_id', 'child_service_id', 'images', 'guests')
        read_only_fields = fields


    @staticmethod
    def check_if_child_service_exist(childs, child_services):
        adults = 0
        rest_childs = []
        for child in childs:
            services_ages = [i.get('until_age') for i in child_services]
            if child == '0':
                rest_childs.append(0)
            elif services_conditions := [i for i in services_ages if int(child)<=i]:
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
        guests_from_request = filters_in_request.GET['guests'].split('-')
        room_category_ids_filter = list(filter(None, filters_in_request.GET['room_category_ids'].strip('][').split(',')))
        rooms_with_guest = []
        result_searched_rooms = {}
        child_services = representation.get('child_service_id')
        try:
            for guest in guests_from_request:
                s = {}
                s[guest.split('and')[0]] = guest.split('and')[1].split('.')
                rooms_with_guest.append(s)

            for index, room_guests in enumerate(rooms_with_guest):
                childs = room_guests.values()
                adults, rest_childs = self.check_if_child_service_exist(*childs, child_services)
                new_key = adults + int(list(room_guests)[0])
                room_guests[new_key] = room_guests.pop(list(room_guests)[0])
                room_guests[new_key] = rest_childs

            child_years = [list(i.values())[0] for i in rooms_with_guest]
            total_num_of_room = len(rooms_with_guest)

            max_num_of_guest = max([max(i, key=i.get) for i in rooms_with_guest])

            room_for_max_num_of_guests = [sub for sub in rooms_with_guest if list(sub.keys())[0] == max_num_of_guest]
            converted_to_dict = {k: v for element in room_for_max_num_of_guests for k,v in element.items()}

            adult = list(converted_to_dict.keys())[0]

            if list(converted_to_dict.values())[0][0] == 0:
                child = 0
            else:
                child = len(list(converted_to_dict.values())[0])
            if room_category_ids_filter:
                rooms = Room.objects.filter(hotel_id=representation.get('id'),
                                            characteristics_id__capacity__gte=adult,
                                            child_capacity__gte=child,
                                            category_id__in=room_category_ids_filter)
            else:
                rooms = Room.objects.filter(hotel_id=representation.get('id'),
                                            characteristics_id__capacity__gte=adult,
                                            child_capacity__gte=child)
            serialized_rooms = RoomSerializer(rooms, many=True, context=self.context).data
            result_searched_rooms['amount_of_room'] = total_num_of_room

            child_years = [item for sublist in child_years for item in sublist]
            for index, child in enumerate(child_years):
                for child_service in child_services:
                    if child_service.get('until_age') == int(child):
                        total_rooms_price += child_service.get('result_price')

            for room in serialized_rooms:
                actual_price = room.get('result_price')
                room['totat_price'] = total_rooms_price + (total_num_of_room*actual_price)
            result_searched_rooms[f'rooms'] = serialized_rooms

            representation['result'] = result_searched_rooms
            return representation
        except TypeError as e:
            representation = {'message': 'Nothing'}
            return representation

    def get_hotel_category(self, obj):
        if obj.hotel_category:
            return list(obj.hotel_category)
        else:
            return []

    def get_food_category(self, obj):
        if obj.food_category:
            return list(obj.food_category)
        else:
            return []

    def get_facilities_hotel_id(self, obj):
        if obj.facilities_hotel_id:
            return list(obj.facilities_hotel_id)
        else:
            return []

    def get_additional_service_id(self, obj):
        if obj.additional_service_id:
            return list(obj.additional_service_id)
        else:
            return []

    # def get_child_service_id(self, obj):
    #     """Get tags."""
    #     if obj.child_service_id:
    #         return list(obj.child_service_id)
    #     else:
    #         return []

    def get_images(self, obj):
        """Get tags."""
        if obj.images:
            return list(obj.images)
        else:
            return []


