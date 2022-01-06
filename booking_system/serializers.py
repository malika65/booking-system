from django.db import models
from rest_framework import fields, serializers

from .models import Hotel, Room, Booking


class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = ('name', 'location', 'phone', 'email')


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('room_no', 'price', 'hotel', 'is_booked')


class BookingSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer()
    room  = RoomSerializer()

    class Meta:
        model  = Booking
        fields = ('hotel', 'room', 'checkin_date', 'checkout_date', 'is_checkout')
