# from celery import shared_task
# import os
# import io
# from booking_system.models.hotel_models import Hotel, Room, HotelImage, PeriodPrice
# from django.core import management
#
#
# @shared_task
# def reload_indexes():
#     management.call_command('search_index', '--rebuild', '-f')