import os

from django.db import models
from smart_selects.db_fields import ChainedForeignKey

from main import settings
from .characteristic_models import (
    FacilitiesAndServicesRooms,
    Characteristics,
    FoodCategory,
    HotelCategoryStars,
    FacilitiesAndServicesHotels,
    ChildService,
    AdditionalService
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


class PeriodPrice(models.Model):
    price = models.FloatField(default=0, verbose_name="Цена")
    currency = models.CharField(
        max_length=10,
        choices=CURRENCY_CHOICES,
        default=USD,
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self) -> str:
        return f'С {str(self.start_date.strftime("%d-%b-%Y"))} - По {str(self.end_date.strftime("%d-%b-%Y"))}: {self.price}' or ''

    class Meta:
        verbose_name_plural = "Период и цены"


class Room(models.Model):
    room_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Название комнаты')
    room_description = models.TextField(max_length=1500, null=True, blank=True, verbose_name='Описание комнаты')
    price = models.ForeignKey(PeriodPrice, blank=True, verbose_name='Цены', on_delete=models.CASCADE)

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
    category_id = models.ManyToManyField(FacilitiesAndServicesHotels, blank=True, verbose_name='Удобства и услуги')
    additional_service_id = models.ManyToManyField(AdditionalService, blank=True, verbose_name='Дополнительные услуги')
    child_service_id = models.ManyToManyField(ChildService, blank=True, verbose_name='Услуги проживания с детьми')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    room_id = models.ManyToManyField(Room, blank=True, verbose_name='Типы комнат')
    checkin_date = models.CharField(null=True, verbose_name='Регистрация заезда с', max_length=20)
    checkout_date = models.CharField(null=True, verbose_name='Регистрация выезда до', max_length=20)

    class Meta:
        verbose_name_plural = "2. Отели"

    def __str__(self) -> str:
        return self.hotel_name or ''

    @property
    def total(self):
        total_rooms_price = []
        for room in self.room_id.all():
            for price in room.price.all():
                total_rooms_price.append(price.price)
        return sum(total_rooms_price)


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, default=None, on_delete=models.CASCADE, related_name='images')
    image_url = models.TextField(max_length=10000, blank=True, null=True)
    image = models.FileField()

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.hotel.hotel_name

    def save(self, *args, **kwargs):
        try:
            get_text = self.image.url
            self.image_url = get_text
            super(HotelImage, self).save(*args, **kwargs)
        except Exception as exp:
            print("Exception: {exp}".format(exp=exp))
        return super(HotelImage, self).save(*args, **kwargs)