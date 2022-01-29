from django.db import models

from datetime import datetime, timedelta
from authe.models import User

from smart_selects.db_fields import ChainedForeignKey

class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self) -> str:
            return self.category_name or ''
            

    class Meta:
        verbose_name_plural = "6. Категории"


class FoodCategory(models.Model):
    foodcategory_name = models.CharField(max_length=50)

    def __str__(self) -> str:
            return self.foodcategory_name or ''
        
    class Meta:
        verbose_name_plural = "5. Категории питания"


class HotelCategory(models.Model):
    hotelcategory_name = models.CharField(max_length=50)

    def __str__(self) -> str:
            return self.hotelcategory_name or ''

    class Meta:
        verbose_name_plural = "4. Категории отелей(звезды)"


class Country(models.Model):
    contry_name = models.CharField(max_length=50)

    def __str__(self) -> str:
            return self.contry_name or ''

    class Meta:
        verbose_name_plural = "3. Страны и города"


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
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.CASCADE)
    city = ChainedForeignKey(
        City,
        chained_field="country",
        chained_model_field="country_id",
        show_all=False,
        auto_choose=True,
        sort=True, blank=True, null=True)
    food_category = models.ManyToManyField(FoodCategory, blank=True, null=True)
    hotel_category = models.ManyToManyField(HotelCategory, blank=True, null=True)
    category_id = models.ManyToManyField(Category, null=True, blank=True, default="Hotel")
    is_active = models.BooleanField(default=True)


    class Meta:
        verbose_name_plural = "2. Отели"


    def __str__(self) -> str:
        return self.hotel_name or ''


class Room(models.Model):
    room_name = models.CharField(max_length=50, null=True, blank=True)
    room_no = models.IntegerField(default=101, null=True, blank=True)
    room_description = models.TextField(max_length=1500, null=True, blank=True)
    price = models.FloatField(default=1000.0, null=True, blank=True)
    hotel_id = models.ForeignKey(Hotel, null=True, blank=True, on_delete=models.CASCADE)
    is_booked = models.BooleanField(default=False) 


    def __str__(self) -> str:
        return self.room_name or ''


    class Meta:
        verbose_name_plural = "7. Номера"


class RoomType(models.Model):
    type_name = models.CharField(max_length=50, null=True, blank=True)
    room_id = models.ForeignKey(Room, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
            return self.type_name or ''





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

    class Meta:
        verbose_name_plural = "1. Бронирования"