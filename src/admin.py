"""Game Jam administration."""

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.dashboard, name='gamejam_dashboard'),
    url(r'^guest$', views.add_guest_login, name='add_guest_login'),
]


admin_links = (
    ("Game Jam", "gamejam_dashboard"),
)