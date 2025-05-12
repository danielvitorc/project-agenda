from django.urls import path
from .views import auth, api, colaborador, lider


urlpatterns = [
    path("", auth.login_view, name="login"),
    path("logout/", auth.logout_view, name="logout"),
    path("home/", colaborador.home, name="home"),
    path('api/reunioes/', api.get_reunioes, name='api_reunioes'),  # Endpoint da API
    path("colaboradores-disponiveis/", api.colaboradores_disponiveis, name="colaboradores_disponiveis"), 
    path('verificar_conflito/', api.verificar_conflito, name='verificar_conflito'),
    path("pedidos/", lider.gerenciar_pedidos, name="gerenciar_pedidos"),
    path("alterar-status/<int:reuniao_id>/<str:novo_status>/", lider.alterar_status_reuniao, name="alterar_status_reuniao"),
    path("page_pedidos/", colaborador.page_pedidos, name="page_pedidos"),
    path('reuniao/<int:reuniao_id>/cancelar/', colaborador.solicitar_cancelamento_reuniao, name='solicitar_cancelamento_reuniao'),
    path('reuniao/<int:reuniao_id>/aprovar-cancelamento/', lider.aprovar_cancelamento, name='aprovar_cancelamento'),
    path("eventos_json/", api.eventos_json, name="eventos_json"),
    path("home_lider/", lider.home_lider, name="home_lider"),
    
]
