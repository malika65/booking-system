from django.db import models

from datetime import datetime, timedelta
from authe.models import User

from smart_selects.db_fields import ChainedForeignKey

class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self) -> str:
            return self.category_name or ''


class Country(models.Model):
    contry_name = models.CharField(max_length=50)

    def __str__(self) -> str:
            return self.contry_name or ''


class City(models.Model):
    city_name = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)
    country_id = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
            return self.city_name or ''




class Hotel(models.Model):
    hotel_name = models.CharField(max_length=20, null=True, blank=True)
    hotel_address = models.CharField(max_length=50, null=True, blank=True)
    hotel_description = models.TextField(max_length=1500, null=True, blank=True)
    hotel_phone = models.CharField(max_length=20, null=True, blank=True)
    city_id = models.ForeignKey(City, null=True, blank=True, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


    def __str__(self) -> str:
        return self.hotel_name or ''


class RoomType(models.Model):
    type_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
            return self.type_name or ''


class Room(models.Model):
    room_name = models.CharField(max_length=50, null=True, blank=True)
    room_no = models.IntegerField(default=101, null=True, blank=True)
    room_description = models.TextField(max_length=1500, null=True, blank=True)
    price = models.FloatField(default=1000.0, null=True, blank=True)
    hotel_id = models.ForeignKey(Hotel, null=True, blank=True, on_delete=models.CASCADE)
    room_type_id = models.ForeignKey(RoomType, null=True, blank=True, on_delete=models.CASCADE)
    is_booked = models.BooleanField(default=False) 


    def __str__(self) -> str:
        return self.room_name or ''


class Booking(models.Model):
    guest_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    checkin_date  = models.DateField(default = datetime.now)
    checkout_date = models.DateField(default = datetime.now)
    created_at = models.DateTimeField(default = datetime.now)
    updated_at = models.DateTimeField(default = datetime.now)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = ChainedForeignKey(
        Room,
        chained_field="hotel",
        chained_model_field="hotel_id",
        show_all=False,
        auto_choose=True,
        sort=True)
    num_of_guest  = models.IntegerField(default=1)
   
    is_checkout   = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.guest_id.email

    def hotel_name(self) -> str:
        return self.hotel.hotel_name

    # return charge of the room based on how many days did you stay at the hotel and is room is occupied
    def charge(self) -> float:
        return self.is_checkout* \
        (self.checkout_date - self.checkin_date + timedelta(1)).days* \
        self.room.price