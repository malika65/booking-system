from datetime import datetime, timedelta

from django.db import models
from smart_selects.db_fields import ChainedForeignKey

from authe.models import User
from .hotel_models import Hotel, Room


class Booking(models.Model):
    guest_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='ID гостя')
    checkin_date = models.DateField(default=datetime.now)
    checkout_date = models.DateField(default=datetime.now)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name='Отель')
    room = ChainedForeignKey(
        Room,
        chained_field="hotel",
        chained_model_field="hotel_id",
        show_all=False,
        auto_choose=True,
        sort=True,
        verbose_name='Комната')
    num_of_guest = models.IntegerField(default=1, verbose_name='Кол-во гостей')

    is_checkout = models.BooleanField(default=False, verbose_name='Проверено')

    def __str__(self) -> str:
        return self.guest_id.email

    def hotel_name(self) -> str:
        return self.hotel.hotel_name

    # return charge of the room based on how many days did you stay at the hotel and is room is occupied
    def charge(self) -> float:
        return self.is_checkout * \
               (self.checkout_date - self.checkin_date + timedelta(1)).days * \
               self.room.price

    class Meta:
        verbose_name_plural = "1. Бронирования"