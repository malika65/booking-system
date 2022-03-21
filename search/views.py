import abc

from django.http import HttpResponse
from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView

from booking_system.documents import HotelDocument
from booking_system.serializers import HotelSerializer


class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = None
    document_class = None

    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""

    def get(self, request, query):
        try:
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)
            response = search.execute()

            print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return HttpResponse(e, status=500)


class SearchHotels(PaginatedElasticSearchAPIView):
    serializer_class = HotelSerializer
    document_class = HotelDocument

    def generate_q_expression(self, query):
        return Q('multi_match', query=query,
                 fields=[
                    'hotel_name',
                    'hotel_description',
                    'city.city_name',
                    'hotel_address',
                 ], fuzziness="3", minimum_should_match="65%", type="most_fields")

