from django.core.mail import EmailMessage

from authe.models import User
from booking_system.models.hotel_models import Hotel, Room
from main import settings
from main.celery import app


class BookingEmailThread:

    def __init__(self, email, hotel_name, room_names, num_of_guests, price, booking_id,
                 num_of_adults, num_of_childs, child_years):
        self.email = email
        self.hotel_name = hotel_name
        self.num_of_guests = num_of_guests
        self.room_names = room_names
        self.price = price
        self.booking_id = booking_id
        self.num_of_adults = num_of_adults
        self.num_of_childs = num_of_childs
        self.child_years = child_years

    def make_message(self):
        message = f'Пользователь {self.email} оставил заявку на бронирование отеля.\n' + \
            f'Отель {self.hotel_name} \n' + \
            f'Комнаты {self.room_names} на {self.num_of_guests} гостей \n' + \
            f'Взрослых: {self.num_of_adults} \n' + \
            f'Детей: {self.num_of_childs} \n' + \
            f'Возрасты детей: {self.child_years} \n' + \
            f'Общая стоимость: {self.price} \n' + \
            f'Перейти для подтверждения: {settings.ROOT_URL}/admin/booking_system/booking/{self.booking_id}/'
        return message


@app.task
def send_booking_to_email(booking_id, hotel_id, rooms, num_of_guests,
                          user_id, room_price, num_of_adults, num_of_childs, child_years):
    user_data = User.objects.filter(id=user_id).first()
    hotel_data = Hotel.objects.filter(id=hotel_id).first()
    room_names = []
    for room_id in rooms:
        room_data = Room.objects.filter(id=room_id).first()
        room_names.append(room_data.room_name)
    email_body = BookingEmailThread(email=user_data.email, hotel_name=hotel_data.hotel_name,
                                    room_names=room_names, num_of_guests=num_of_guests,
                                    price=room_price, booking_id=booking_id,
                                    num_of_adults=num_of_adults, num_of_childs=num_of_childs,
                                    child_years=child_years)
    email_body = email_body.make_message()
    data = {'email_body': email_body, 'to_email': settings.EMAIL_FROM,
            'email_subject': f'Запрос на бронирование отеля {hotel_data.hotel_name}'}
    email = EmailMessage(
        subject=data['email_subject'], body=data['email_body'], to=[settings.EMAIL_FROM])
    email.send()


