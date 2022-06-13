from django_elasticsearch_dsl_drf import viewsets
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
)
from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend, IdsFilterBackend
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from booking_system.documents import HotelDocument
# from booking_system.filter import HotelFilter, HotelCategoryFilter
from booking_system.serializers.hotel_serializers import HotelSearchSerializer


class HotelDocumentView(viewsets.ReadOnlyModelViewSet):
    document = HotelDocument
    serializer_class = HotelSearchSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'

    filter_backends = (
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
        # HotelCategoryFilter,
    )

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
        'facilities_hotel_id': 'facilities_hotel_id.id',
    }
    ordering_fields = {
        'id': 'id',
    }
