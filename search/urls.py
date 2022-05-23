from django.conf.urls import url
from django.urls import path

from .views import HotelDocumentView

urlpatterns = [
    # path('hotels/<str:query>/', SearchHotels.as_view()),
    # path('', HotelDocumentView.as_view({'get': 'list'})),
]


# urlpatterns =[
#     ('haystack.views',
#     url(r'^search/$', SearchView(
#         searchqueryset=MlSearchQuerySet(),
#         form_class=ModelSearchForm
#     ), name='haystack_search_ml'),
# )]