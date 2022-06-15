from rest_framework import serializers

from booking_system.models.booking_models import Booking


class BookingSerializer(serializers.ModelSerializer):
    hotel = serializers.StringRelatedField()
    guest_id = serializers.StringRelatedField()
    room = serializers.ListField(write_only=True)
    room_price = serializers.IntegerField(required=False, read_only=True)
    url = serializers.CharField(required=False, read_only=True)
    num_of_adults = serializers.CharField(required=False, read_only=True)
    num_of_childs = serializers.CharField(required=False, read_only=True)
    child_years = serializers.ListField(required=False, read_only=True)

    class Meta:
        model = Booking
        fields = ('guest_id', 'checkin_date', 'checkout_date',
                  'hotel', 'room', 'num_of_guest', 'room_price', 'url', 'phone_number',
                  'num_of_adults', 'num_of_childs', 'child_years', 'is_checkout')

