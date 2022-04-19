from django.urls import path

from .views import PublisherDocumentView

urlpatterns = [
    # path('hotels/<str:query>/', SearchHotels.as_view()),
    path('', PublisherDocumentView.as_view({'get': 'list'})),
]