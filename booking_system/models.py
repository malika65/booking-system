from django.db import models

from datetime import datetime, timedelta
from authe.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from smart_selects.db_fields import ChainedForeignKey


class FacilitiesAndServicesHotels(models.Model):
    hotel_category_name = models.CharField(max_length=50, verbose_name='Наименование услуги и удобств отеля')

    def __str__(self) -> str:
            return self.hotel_category_name or ''
            

    class Meta:
        verbose_name_plural = "6. Удобства и услуги отелей"

class FacilitiesAndServicesRooms(models.Model):
    room_category_name = models.CharField(max_length=50, verbose_name='Наименование услуги и удобств комнаты')

    def __str__(self) -> str:
            return self.room_category_name or ''
            

    class Meta:
        verbose_name_plural = "9. Удобства и услуги комнат"

class FoodCategory(models.Model):
    foodcategory_name = models.CharField(max_length=50, verbose_name='Категория питания')
    foodcategory_abbreviation = models.CharField(max_length=2, default=None, verbose_name='Аббревиатура питания')

    def __str__(self) -> str:
            return self.foodcategory_name or ''
        
    class Meta:
        verbose_name_plural = "5. Категории питания"


class HotelCategoryStars(models.Model):
    hotelcategory_name = models.CharField(max_length=50, verbose_name='Категория звезд отеля')
    hotelcategory_stars = models.IntegerField(default=1, validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ], verbose_name='Звезды')

    def __str__(self) -> str:
            return self.hotelcategory_name or ''

    class Meta:
        verbose_name_plural = "4. Категории отелей(звезды)"


class Country(models.Model):
    contry_name = models.CharField(max_length=50, verbose_name='Страны')

    def __str__(self) -> str:
            return self.contry_name or ''

    class Meta:
        verbose_name_plural = "3. Страны и города"


class City(models.Model):
    city_name = models.CharField(max_length=50, verbose_name='Города')
    postal_code = models.CharField(max_length=50, verbose_name='Почтовый код', null=True, blank=True, default=None)
    country_id = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Страна')
    
    def __str__(self) -> str:
            return self.city_name or ''



class Characteristics(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    capacity = models.IntegerField(default=1, verbose_name='Вместимость')
    # hotel_id = models.ForeignKey(Hotel, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Отель')

    def __str__(self) -> str:
        return self.name or ''


    class Meta:
        verbose_name_plural = "8. Характеристики"


class Room(models.Model):
    room_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Название комнаты')
    room_no = models.IntegerField(default=101, null=True, blank=True, verbose_name='Номер комнаты')
    room_description = models.TextField(max_length=1500, null=True, blank=True, verbose_name='Описание комнаты')
    price = models.FloatField(default=1000.0, null=True, blank=True, verbose_name='Цена')
    category_id = models.ManyToManyField(FacilitiesAndServicesRooms, blank=True, default="Hotel", verbose_name='Удобства и услуги комнаты')
    characteristics_id = models.ManyToManyField(Characteristics, blank=True, verbose_name='Комната')


    def __str__(self) -> str:
        return self.room_name or ''


    class Meta:
        verbose_name_plural = "7. Типы Номеров"


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=20, null=True, blank=True, verbose_name='Название отеля')
    hotel_address = models.CharField(max_length=50, null=True, blank=True, verbose_name='Адрес отеля')
    hotel_description = models.TextField(max_length=1500, null=True, blank=True, verbose_name='Описание отеля')
    hotel_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Номер телефона отеля')
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Страна')
    city = ChainedForeignKey(
        City,
        chained_field="country",
        chained_model_field="country_id",
        show_all=False,
        auto_choose=True,
        sort=True, blank=True, null=True, verbose_name='Город')
    food_category = models.ManyToManyField(FoodCategory, blank=True, verbose_name='Категории питания')
    hotel_category = models.ManyToManyField(HotelCategoryStars, blank=True, verbose_name='Звезды отеля')
    category_id = models.ManyToManyField(FacilitiesAndServicesHotels, blank=True, default="Hotel", verbose_name='Удобства и услуги')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    room_id = models.ManyToManyField(Room, blank=True, verbose_name='Типы комнат')


    class Meta:
        verbose_name_plural = "2. Отели"


    def __str__(self) -> str:
        return self.hotel_name or ''



class Booking(models.Model):
    guest_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='ID гостя')
    checkin_date  = models.DateField(default = datetime.now)
    checkout_date = models.DateField(default = datetime.now)
    created_at = models.DateTimeField(default = datetime.now)
    updated_at = models.DateTimeField(default = datetime.now)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name='Отель')
    room = ChainedForeignKey(
        Room,
        chained_field="hotel",
        chained_model_field="hotel_id",
        show_all=False,
        auto_choose=True,
        sort=True, 
        verbose_name='Комната')
    num_of_guest  = models.IntegerField(default=1, verbose_name='Кол-во гостей')
   
    is_checkout   = models.BooleanField(default=False, verbose_name='Проверено')

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