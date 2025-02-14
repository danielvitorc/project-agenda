from django.urls import path
from .views import login_view, logout_view, home, colaboradores_disponiveis


urlpatterns = [
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("home/", home, name="home"),
    path("colaboradores-disponiveis/", colaboradores_disponiveis, name="colaboradores_disponiveis"),
]
