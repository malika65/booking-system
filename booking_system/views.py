from rest_framework import serializers, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models.hotel_models import Hotel, Room, HotelImage
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


# class HotelImageList(generics.ListAPIView):
#     queryset = HotelImage.objects.all()
#     serializer_class = HotelImageSerializer
#     permission_classes = (AllowAny,)


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


class BookingList(generics.ListAPIView):
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
