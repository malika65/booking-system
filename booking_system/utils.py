from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

import threading

from main.celery import app


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class BookingEmailThread:

    def __init__(self, email, hotel_name, num_of_guests, room_name, price):
        self.email = email
        self.hotel_name = hotel_name
        self.num_of_guests = num_of_guests
        self.room_name = room_name
        self.price = price

    def make_message(self):
        message = f'Пользователь {self.email} оставил заявку на бронирование отеля.\n' + \
            f'Отель {self.hotel_name} \n' + \
            f'Комната {self.room_name} на {self.num_of_guests} \n' + \
            f'Общая стоимость: {self.price}'
        return message

@app.task
def send_booking_to_email(hotel_data, room_data, num_of_guests, user_data, price):
    email_body = BookingEmailThread(user_data.email, hotel_data.name, room_data.room_name, num_of_guests, price)
    data = {'email_body': email_body, 'to_email': 'malikasatimbay@gmail.com',
            'email_subject': f'Запрос на бронирование отеля {hotel_data.name}'}
    email = EmailMessage(
        subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
    EmailThread(email).start()


