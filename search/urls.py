from django.urls import path

from .views import SearchHotels

urlpatterns = [
    path('hotels/<str:query>/', SearchHotels.as_view()),
]