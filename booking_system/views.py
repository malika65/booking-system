import asyncio

from django.core.signals import request_finished, request_started
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework import serializers, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core import management

from .models.hotel_models import Hotel, Room, HotelImage, PeriodPrice
from .models.booking_models import Booking
from .models.characteristic_models import (
    FacilitiesAndServicesHotels,
    FacilitiesAndServicesRooms,
    FoodCategory,
    HotelCategoryStars,
    Characteristics,
    Category
)
from .serializers import (
    HotelSerializer,
    BookingSerializer,
    RoomSerializer,
    FacilitiesAndServicesHotelsSerializer,
    FacilitiesAndServicesRoomsSerializer,
    FoodCategorySerializer,
    HotelCategoryStarsSerializer,
    CharacteristicsSerializer,
    CategorySerializer,
    HotelImageSerializer
)


class HotelList(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = (AllowAny,)


class HotelDetail(generics.RetrieveAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = (AllowAny,)


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)


class FacilitiesAndServicesHotelsList(generics.ListAPIView):
    queryset = FacilitiesAndServicesHotels.objects.all()
    serializer_class = FacilitiesAndServicesHotelsSerializer
    permission_classes = (AllowAny,)


class FacilitiesAndServicesRoomsList(generics.ListAPIView):
    queryset = FacilitiesAndServicesRooms.objects.all()
    serializer_class = FacilitiesAndServicesRoomsSerializer
    permission_classes = (AllowAny,)


class FoodCategoryList(generics.ListAPIView):
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer
    permission_classes = (AllowAny,)


class HotelCategoryStarsList(generics.ListAPIView):
    queryset = HotelCategoryStars.objects.all()
    serializer_class = HotelCategoryStarsSerializer
    permission_classes = (AllowAny,)


class CharacteristicsList(generics.ListAPIView):
    queryset = Characteristics.objects.all()
    serializer_class = CharacteristicsSerializer
    permission_classes = (AllowAny,)


class RoomList(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (AllowAny,)


class BookingListCreate(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(guest_id=user.id)

    def perform_create(self, serializer):
        serializer.save(guest_id=self.request.user,)


class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(guest_id=user.id)

    def perform_create(self, serializer):
        serializer.save(guest_id=self.request.user,)
# from main.celery import reload_indexes
# from .tasks import reload_indexes
# @receiver(request_finished)
# def my_callback(sender, **kwargs):
#     management.call_command('search_index', '--rebuild', '-f')

@receiver(post_save)
def update_index(sender, instance, **kwargs):
    management.call_command('search_index', '--rebuild', '-f')
    # reload_indexes.delay()
    # request_started.send(None)
    # request_finished.connect(my_callback)
    # # loop = asyncio.new_event_loop()
    # # asyncio.set_event_loop(loop)
    # # loop.run_until_complete(management.call_command('search_index', '--rebuild', '-f'))
    # # loop.close()



