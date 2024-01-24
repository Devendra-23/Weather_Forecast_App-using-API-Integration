from django.urls import path
from . import views
from weatherapp.views import city_autocomplete
from .views import city_detail

urlpatterns = [
    path("", views.home, name='home'),
    path("city-autocomplete/", city_autocomplete, name='city-autocomplete'),
    path('city-detail/', city_detail, name='city_detail'),
]
