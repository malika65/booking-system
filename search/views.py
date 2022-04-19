from django_elasticsearch_dsl_drf.constants import SUGGESTER_TERM, SUGGESTER_PHRASE, SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.filter_backends import FilteringFilterBackend, OrderingFilterBackend, \
    CompoundSearchFilterBackend, DefaultOrderingFilterBackend, FunctionalSuggesterFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from booking_system.documents import HotelDocument
from booking_system.serializers import HotelSerializer


class PublisherDocumentView(DocumentViewSet):
    document = HotelDocument
    serializer_class = HotelSerializer
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
        FunctionalSuggesterFilterBackend,
    ]

    search_fields = (
        'hotel_name',
        'hotel_description',
        'city.country_id.country_name',
        'city.city_name',
        'hotel_address',
    )
    multi_match_search_fields = (
        'hotel_name',
        'hotel_address',
    )
    filter_fields = {
        'food_category': 'food_category.id',
        'hotel_category': 'hotel_category.id',
        'categories': 'category_id.id',
        "room_name_id": 'room_id.id',
        "room_category_id": 'room_id.category_id.id',
        "room_characteristic_id": 'room_id.characteristics_id.id'
    }

    ordering_fields = {
        'id': 'id',
    }
