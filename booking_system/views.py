from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_api_key.permissions import HasAPIKey

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
    permission_classes = (AllowAny, HasAPIKey)


class HotelDetail(generics.RetrieveAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = (AllowAny, HasAPIKey)


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny, HasAPIKey)


class FacilitiesAndServicesHotelsList(generics.ListAPIView):
    queryset = FacilitiesAndServicesHotels.objects.all()
    serializer_class = FacilitiesAndServicesHotelsSerializer
    permission_classes = (AllowAny, HasAPIKey)


class FacilitiesAndServicesRoomsList(generics.ListAPIView):
    queryset = FacilitiesAndServicesRooms.objects.all()
    serializer_class = FacilitiesAndServicesRoomsSerializer
    permission_classes = (AllowAny, HasAPIKey)


class FoodCategoryList(generics.ListAPIView):
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer
    permission_classes = (AllowAny, HasAPIKey)


class HotelCategoryStarsList(generics.ListAPIView):
    queryset = HotelCategoryStars.objects.all()
    serializer_class = HotelCategoryStarsSerializer
    permission_classes = (AllowAny, HasAPIKey)


class CharacteristicsList(generics.ListAPIView):
    queryset = Characteristics.objects.all()
    serializer_class = CharacteristicsSerializer
    permission_classes = (AllowAny, HasAPIKey)


class RoomList(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (AllowAny, HasAPIKey)


class BookingListCreate(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (AllowAny, HasAPIKey)

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(guest_id=user.id)

    def perform_create(self, serializer):
        hotel = Hotel.objects.get(pk=self.request.data['hotel'])

        booking = serializer.save(guest_id=self.request.user,
                                  hotel=hotel,
                                  )
        booking.room.set(self.request.data['room'])

        send_booking_to_email.delay(booking_id=booking.id, hotel_id=hotel.id, rooms=self.request.data['room'],
                                    num_of_guests=self.request.data['num_of_guest'],
                                    user_id=self.request.user.id,
                                    room_price=self.request.data['room_price'],
                                    num_of_adults=self.request.data['num_of_adults'],
                                    num_of_childs=self.request.data['num_of_childs'],
                                    child_years=self.request.data['child_years'])


class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated, HasAPIKey)

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(guest_id=user.id)


# @receiver(post_save)
# def update_index(sender, instance, **kwargs):
#     reload_indexes.delay()


