from rest_framework import serializers

from booking_system.models.booking_models import Booking


class BookingSerializer(serializers.ModelSerializer):
    hotel = serializers.StringRelatedField()
    guest_id = serializers.StringRelatedField()
    room = serializers.StringRelatedField()
    room_price = serializers.IntegerField(required=False, read_only=True)
    url = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = Booking
        fields = ('guest_id', 'checkin_date', 'checkout_date',
                  'hotel', 'room', 'num_of_guest', 'room_price', 'url')

