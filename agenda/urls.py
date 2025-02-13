from django.urls import path
from .views import login_view, logout_view, home


urlpatterns = [
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("home/", home, name="home")
]
