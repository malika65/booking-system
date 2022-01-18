from django.db import models
from rest_framework import fields, serializers

from .models import Hotel, Room, Booking


class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = ('hotel_name', 'hotel_address', 'hotel_description', 'hotel_phone', 'city_id', 'category_id', 'is_active')


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('room_name','room_no', 'room_description', 'price', 'hotel_id', 'room_type_id', 'is_booked')


class BookingSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer()
    room  = RoomSerializer()

    class Meta:
        model  = Booking
        fields = ('guest_id', 'checkin_date', 'checkout_date', 'hotel', 'room', 'num_of_guest', 'is_checkout')
