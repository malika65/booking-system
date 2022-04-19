from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
    food_category_abbreviation = models.CharField(max_length=2, default=None, null=True, verbose_name='Аббревиатура питания')

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