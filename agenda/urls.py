from django.urls import path
from .views import login_view, logout_view, home, colaboradores_disponiveis, gerenciar_pedidos, alterar_status_reuniao, get_reunioes, page_pedidos, eventos_json


urlpatterns = [
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("home/", home, name="home"),
     path('api/reunioes/', get_reunioes, name='api_reunioes'),  # Endpoint da API
    path("colaboradores-disponiveis/", colaboradores_disponiveis, name="colaboradores_disponiveis"),
    path("pedidos/", gerenciar_pedidos, name="gerenciar_pedidos"),
    path("alterar-status/<int:reuniao_id>/<str:novo_status>/",alterar_status_reuniao, name="alterar_status_reuniao"),
    path("page_pedidos/", page_pedidos, name="page_pedidos"),
     path("eventos_json/", eventos_json, name="eventos_json"),
    
]
