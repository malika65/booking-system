from django_elasticsearch_dsl_drf.constants import SUGGESTER_TERM, SUGGESTER_PHRASE, SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.filter_backends import FilteringFilterBackend, OrderingFilterBackend, \
    CompoundSearchFilterBackend, DefaultOrderingFilterBackend, FunctionalSuggesterFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from elasticsearch_dsl import RangeFacet

from booking_system.documents import HotelDocument
from booking_system.serializers.hotel_serializers import HotelSearchSerializer
from django_elasticsearch_dsl_drf.constants import ( LOOKUP_FILTER_TERMS,
LOOKUP_FILTER_RANGE,
LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_EXCLUDE,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination


class HotelDocumentView(DocumentViewSet):
    document = HotelDocument
    serializer_class = HotelSearchSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'

    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
        FunctionalSuggesterFilterBackend,
    ]

    search_fields = {
        'hotel_name_ru': {'fuzziness': 2, 'minimum_should_match': "65%"},
        'hotel_name_en': {'fuzziness': 2, 'minimum_should_match': "65%"},
        'city.country_id.country_name_ru': {'fuzziness': 2, 'minimum_should_match': "65%"},
        'city.country_id.country_name_en': {'fuzziness': 2, 'minimum_should_match': "65%"},
        'city.city_name_ru': {'fuzziness': 2, 'minimum_should_match': "65%"},
        'city.city_name_en': {'fuzziness': 2, 'minimum_should_match': "65%"},
    }
    multi_match_search_fields = (
        'hotel_name_ru',
        'hotel_name_en',
        'hotel_address_ru',
        'hotel_address_en',
    )
    filter_fields = {
        'food_category': 'food_category.id',
        'hotel_category': 'hotel_category.id',
        'categories': 'category_id.id',
        'room_name_id': 'room_id.id',
        # 'room_price': {
        #     'field': 'room_id.price',
        #     'lookups': [
        #         LOOKUP_FILTER_RANGE,
        #         LOOKUP_QUERY_IN,
        #     ],
        # },
        # 'room_capacity': {
        #     'field': 'room_id.characteristics_id.capacity',
        # },
        # 'room_capacity_child': {
        #     'field': 'room_id.child_capacity',
        # },
        'room_category_id': 'room_id.category_id.id',
        'room_characteristic_id': 'room_id.characteristics_id.id'
    }

    ordering_fields = {
        'id': 'id',
    }