from django.db import models
from smart_selects.db_fields import ChainedForeignKey

from .characteristic_models import (
    FacilitiesAndServicesRooms,
    Characteristics,
    FoodCategory,
    HotelCategoryStars,
    FacilitiesAndServicesHotels
)
from .country_models import Country, City

EUR = "EURO"
KGS = "SOM"
KZT = "TENGE"
USD = "DOLLAR"

CURRENCY_CHOICES = [
    (EUR, 'EURO'),
    (KGS, 'SOM'),
    (KZT, 'TENGE'),
    (USD, 'DOLLAR'),
]


class Room(models.Model):
    room_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Название комнаты')
    room_no = models.IntegerField(default=101, null=True, blank=True, verbose_name='Номер комнаты')
    room_description = models.TextField(max_length=1500, null=True, blank=True, verbose_name='Описание комнаты')
    price = models.FloatField(default=1000.0, null=True, blank=True, verbose_name='Цена')
    currency = models.CharField(
        max_length=10,
        choices=CURRENCY_CHOICES,
        default=USD,
    )
    category_id = models.ManyToManyField(FacilitiesAndServicesRooms, blank=True, verbose_name='Удобства и услуги комнаты')
    characteristics_id = models.ManyToManyField(Characteristics, blank=True, verbose_name='Характеристики(вместимости)')
    child_capacity = models.IntegerField(default=0, verbose_name='Сколько детей помещается')

    def __str__(self) -> str:
        return self.room_name or ''

    class Meta:
        verbose_name_plural = "7. Типы Номеров"


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=20, null=True, blank=True, verbose_name='Название отеля')
    hotel_address = models.CharField(max_length=50, null=True, blank=True, verbose_name='Адрес отеля')
    hotel_description = models.TextField(max_length=1500, null=True, blank=True, verbose_name='Описание отеля')
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
    category_id = models.ManyToManyField(FacilitiesAndServicesHotels, blank=True, default="Hotel",
                                         verbose_name='Удобства и услуги')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    room_id = models.ManyToManyField(Room, blank=True, verbose_name='Типы комнат')
    checkin_date = models.DateField(null=True, verbose_name='Регистрация заезда с')
    checkout_date = models.DateField(null=True, verbose_name='Регистрация выезда до')

    class Meta:
        verbose_name_plural = "2. Отели"

    def __str__(self) -> str:
        return self.hotel_name or ''

