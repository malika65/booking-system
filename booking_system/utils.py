from django.core.mail import EmailMessage

from authe.models import User
from booking_system.models.hotel_models import Hotel, Room
from main import settings
from main.celery import app


class BookingEmailThread:

    def __init__(self, email, hotel_name, num_of_guests, room_name, price, booking_id):
        self.email = email
        self.hotel_name = hotel_name
        self.num_of_guests = num_of_guests
        self.room_name = room_name
        self.price = price,
        self.booking_id = booking_id

    def make_message(self):
        message = f'Пользователь {self.email} оставил заявку на бронирование отеля.\n' + \
            f'Отель {self.hotel_name} \n' + \
            f'Комната {self.room_name} на {self.num_of_guests} \n' + \
            f'Общая стоимость: {self.price} \n' + \
            f'Перейти для подтверждения: http://127.0.0.1:8000/admin/booking_system/booking/{self.booking_id}/'
        return message


@app.task
def send_booking_to_email(booking_id, hotel_id, room_id, num_of_guests, user_id, room_price):
    user_data = User.objects.filter(id=user_id).first()
    hotel_data = Hotel.objects.filter(id=hotel_id).first()
    room_data = Room.objects.filter(id=room_id).first()
    email_body = BookingEmailThread(user_data.email, hotel_data.hotel_name,
                                    room_data.room_name, num_of_guests,
                                    room_price, booking_id)
    email_body = email_body.make_message()
    data = {'email_body': email_body, 'to_email': settings.EMAIL_FROM,
            'email_subject': f'Запрос на бронирование отеля {hotel_data.hotel_name}'}
    email = EmailMessage(
        subject=data['email_subject'], body=data['email_body'], to=[settings.EMAIL_FROM])
    email.send()


