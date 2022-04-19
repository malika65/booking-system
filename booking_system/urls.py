from django.urls import path

from .views import (
    HotelList,
    HotelDetail,
    BookingList,
    BookingDetail,
    RoomList,
    FacilitiesAndServicesHotelsList,
    FacilitiesAndServicesRoomsList,
    FoodCategoryList,
    HotelCategoryStarsList,
    CharacteristicsList,
    CategoryList
)

urlpatterns = [
    path('hotel_list/', HotelList.as_view()),
    path('room_list/', RoomList.as_view()),
    path('categories/', CategoryList.as_view()),
    path('facilitiels_of_hotels/', FacilitiesAndServicesHotelsList.as_view()),
    path('facilitiels_of_rooms/', FacilitiesAndServicesRoomsList.as_view()),
    path('food_categories/', FoodCategoryList.as_view()),
    path('hotel_stars_categories/', HotelCategoryStarsList.as_view()),
    path('characteristics/', CharacteristicsList.as_view()),
    path('hotel_detail/<int:pk>/', HotelDetail.as_view()),
    path('booking-list/', BookingList.as_view()),
    path('booking-detail/<int:pk>', BookingDetail.as_view()),
]