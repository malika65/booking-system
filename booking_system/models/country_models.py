from django.db import models


class Country(models.Model):
    country_name = models.CharField(max_length=50, verbose_name='Страны')

    def __str__(self) -> str:
        return self.country_name or ''

    class Meta:
        verbose_name_plural = "3. Страны и города"


class City(models.Model):
    city_name = models.CharField(max_length=50, verbose_name='Города')
    country_id = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Страна')

    def __str__(self) -> str:
        return self.city_name or ''
