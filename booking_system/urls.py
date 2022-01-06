from django.urls import path

from .views import HotelList, HotelDetail

urlpatterns = [
    path('hotel-list/', HotelList.as_view()),
    path('hotel-detail/<int:pk>', HotelDetail.as_view()),
]