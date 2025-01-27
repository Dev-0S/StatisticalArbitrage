from django.urls import path
from . import views

urlpatterns = [
    path('', views.calculate_cointegration, name='calculate_cointegration'),
]