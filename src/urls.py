"""Game jam urls."""

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^guest_login$', views.guest_login, name='guest_login'),
    url(r'^register_mac_address$', views.register_mac_address, name='register_mac_address'),
]
