from django.db import models

from datetime import datetime, timedelta


class Hotel(models.Model):
    name     = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    phone    = models.CharField(max_length=20)
    email    = models.CharField(max_length=20)


    def __str__(self) -> str:
        return self.name


class Room(models.Model):
    room_no   = models.IntegerField(default=101)
    price     = models.FloatField(default=1000.0)
    hotel     = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    is_booked = models.BooleanField(default=False) 


    def __str__(self) -> str:
        return str(self.room_no)


    def hotel_name(self) -> str:
        return self.hotel


class Booking(models.Model):
    hotel         = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room          = models.ForeignKey(Room, on_delete=models.CASCADE)
    num_of_guest  = models.IntegerField(default=1)
    checkin_date  = models.DateField(default = datetime.now)
    checkout_date = models.DateField(default = datetime.now)
    is_checkout   = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.guest.name

    def hotel_name(self) -> str:
        return self.hotel.hotel

    # return charge of the room based on how many days did you stay at the hotel and is room is occupied
    def charge(self) -> float:
        return self.is_checkout* \
        (self.checkout_date - self.checkin_date + timedelta(1)).days* \
        self.room.price