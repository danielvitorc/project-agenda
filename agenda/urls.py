from django.urls import path
from .views import login_view, logout_view, home, colaboradores_disponiveis, gerenciar_pedidos, alterar_status_reuniao


urlpatterns = [
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("home/", home, name="home"),
    path("colaboradores-disponiveis/", colaboradores_disponiveis, name="colaboradores_disponiveis"),
    path("pedidos/", gerenciar_pedidos, name="gerenciar_pedidos"),
    path("alterar-status/<int:reuniao_id>/<str:novo_status>/",alterar_status_reuniao, name="alterar_status_reuniao"),
]
