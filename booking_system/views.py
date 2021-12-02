from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view


from .models import Guest, Hotel, Room, Booking
from .serializers import GuestSerializer, HotelSerializer, RoomSerializer, BookingSerializer

from collections import namedtuple


nt = namedtuple('object', ['model', 'serializers'])
pattern = {
    "guest"   : nt(Guest, GuestSerializer),
    "hotel"   : nt(Hotel, HotelSerializer),
    "room"    : nt(Room, RoomSerializer),
    "booking" : nt(Booking, BookingSerializer)
}



@api_view(['GET', 'POST'])
def ListView(request, api_name):
    object = pattern.get(api_name, None)
    if object is None:
        return Response(
            data   = 'Invalid URL',
            status = status.HTTP_404_NOT_FOUND,
        )

    if request.method == 'GET':
        object_list = object.model.objects.all()
        serializer  = object.serializers(object_list, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = request.data
        serializers = object.serializers(data=data)

        if not serializers.is_valid():
            return Response(
                data   = serializers.errors,
                status = status.HTTP_404_NOT_FOUND,
            )
        
        serializers.save()
        return Response(
            data = serializers.errors,
            status = status.HTTP_201_CREATED,
        )