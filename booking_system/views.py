from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from booking_system.serializers.booking_serializers import BookingSerializer
from booking_system.serializers.characteristics_serializers import (
    FacilitiesAndServicesHotelsSerializer,
    FacilitiesAndServicesRoomsSerializer,
    FoodCategorySerializer,
    HotelCategoryStarsSerializer,
    CharacteristicsSerializer,
    CategorySerializer
)
from booking_system.serializers.hotel_serializers import (
    HotelSerializer,
    RoomSerializer,
)
from main.celery import reload_indexes
from .models.booking_models import Booking
from .models.characteristic_models import (
    FacilitiesAndServicesHotels,
    FacilitiesAndServicesRooms,
    FoodCategory,
    HotelCategoryStars,
    Characteristics,
    Category
)
from .models.hotel_models import Hotel, Room
from .utils import send_booking_to_email


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
    permission_classes = (AllowAny,)

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(guest_id=user.id)

    def perform_create(self, serializer):
        hotel = Hotel.objects.get(pk=self.request.data['hotel'])
        room = Room.objects.get(pk=self.request.data['room'])
        booking = serializer.save(guest_id=self.request.user,
                                  hotel=hotel,
                                  room=room)

        # print(serializer.num_of_guest)
        # print(serializer)
        # print(self.request.user)
        # hotel_data, room_data, num_of_guests, user_data, price
        send_booking_to_email(booking.id, hotel, room, self.request.data['num_of_guest'],
                              self.request.user, self.request.data['room_price'])


class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(guest_id=user.id)


# @receiver(post_save)
# def update_index(sender, instance, **kwargs):
#     reload_indexes.delay()


