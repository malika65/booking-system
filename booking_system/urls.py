from django.urls import path

from .views import HotelList, HotelDetail, BookingList, BookingDetail

urlpatterns = [
    path('hotel-list/', HotelList.as_view()),
    path('hotel-detail/<int:pk>', HotelDetail.as_view()),
    path('booking-list/', BookingList.as_view()),
    path('booking-detail/<int:pk>', BookingDetail.as_view()),
]