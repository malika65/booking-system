from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

EUR = "EUR"
KGS = "KGS"
KZT = "KZT"
USD = "USD"

CURRENCY_CHOICES = [
    (EUR, 'EUR'),
    (KGS, 'KGS'),
    (KZT, 'KZT'),
    (USD, 'USD'),
]


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Подкатегории')

    def __str__(self) -> str:
        return self.name or ''

    class Meta:
        verbose_name_plural = "Подкатегории услуги удобств отелей"


class FacilitiesAndServicesHotels(models.Model):
    hotel_category_name = models.CharField(max_length=50, verbose_name='Наименование услуги и удобств отеля')
    category_id = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, verbose_name='Подкатегория')

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
    food_category_name = models.CharField(max_length=50, verbose_name='Категория питания')

    def __str__(self) -> str:
        return self.food_category_name or ''

    class Meta:
        verbose_name_plural = "5. Категории питания"


class HotelCategoryStars(models.Model):
    hotel_category_name = models.CharField(max_length=50, verbose_name='Категория звезд отеля')
    hotel_category_stars = models.IntegerField(default=1, validators=[
        MaxValueValidator(7),
        MinValueValidator(1)
    ], verbose_name='Звезды')

    def __str__(self) -> str:
        return self.hotel_category_name or ''

    class Meta:
        verbose_name_plural = "4. Категории отелей(звезды)"


class Characteristics(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    capacity = models.IntegerField(default=1, verbose_name='Вместимость')

    def __str__(self) -> str:
        return self.name or ''

    class Meta:
        verbose_name_plural = "8. Характеристики"


class AdditionalService(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название', null=True)
    price = models.FloatField(default=0, null=True, blank=True, verbose_name='Цена')
    currency = models.CharField(
        max_length=10,
        choices=CURRENCY_CHOICES,
        default=USD,
    )

    def __str__(self) -> str:
        return self.name or ''

    class Meta:
        verbose_name_plural = "Дополнительные услуги"


class ChildService(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название', null=True)
    until_age = models.IntegerField(default=1, validators=[
        MaxValueValidator(17),
        MinValueValidator(1)
    ], verbose_name='До какого возраста', null=True)
    is_discount = models.BooleanField(default=False, verbose_name='Проценты')
    price = models.FloatField(default=0, null=True, blank=True, verbose_name='Цена или проценты')
    currency = models.CharField(
        max_length=10,
        choices=CURRENCY_CHOICES,
        default=USD,
    )

    def __str__(self) -> str:
        return self.name or ''

    class Meta:
        verbose_name_plural = "Услуги проживания с детьми"