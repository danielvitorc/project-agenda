# Módulo que gera api dos registros de reunião no banco para o calendário
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import json
from ..models import Reuniao, Usuario

# View que pega o registro dos pedidos do banco para o JSON
def get_reunioes(request):
    reunioes = Reuniao.objects.all()
    eventos = [
        {
            "title": reuniao.titulo,
            "start": f"{reuniao.data_inicio}T{reuniao.horario_inicio}",
            "end": f"{reuniao.data_inicio}T{reuniao.horario_fim}",
        }
        for reuniao in reunioes
    ]
    return JsonResponse(eventos, safe=False)

# view que retorna disponibilidade dos colaboradores para registro no formulario
@login_required
def colaboradores_disponiveis(request):
    data_inicio = request.GET.get("data_inicio")
    horario_inicio = request.GET.get("horario_inicio")
    horario_fim = request.GET.get("horario_fim")

    if data_inicio and horario_inicio and horario_fim:
        colaboradores_ocupados = Reuniao.objects.filter(
            data_inicio=data_inicio,
            status__in=['pendente', 'aprovado']
        ).filter(
            Q(horario_inicio__lt=horario_fim) & Q(horario_fim__gt=horario_inicio)
        ).values_list('colaboradores', flat=True)

        colaboradores_disponiveis = Usuario.objects.filter(role='colaborador').exclude(id__in=colaboradores_ocupados)
        # Retorne id, nome, username e setor
        return JsonResponse({"colaboradores": list(colaboradores_disponiveis.values("id", "nome", "username", "setor__nome"))})


# View que carrega dados aos moldais de detalhes de uma reunião
def eventos_json(request):
    reunioes = Reuniao.objects.filter(status__in=["pendente", "aprovado"])
    eventos = [
        {
            "id": reuniao.id,
            "title": reuniao.titulo,
            "start": f"{reuniao.data_inicio}T{reuniao.horario_inicio}",
            "end": f"{reuniao.data_inicio}T{reuniao.horario_fim}",
            "descricao": reuniao.descricao,
            "local": reuniao.local.nome,
            "colaboradores": ", ".join([f"{colab.username} - {colab.nome}" for colab in reuniao.colaboradores.all()]),
            "status": reuniao.status.lower().strip(),
        }
        for reuniao in reunioes
    ]
    return JsonResponse(eventos, safe=False)

# View que nao permite marcar uma reunião para o mesmo local, no mesmo dia e intervalo de horario para uma ja cadastrada

@csrf_exempt
def verificar_conflito(request):
    if request.method == "POST":
        data = json.loads(request.body)
        local = data.get("local")
        data_inicio = data.get("data_inicio")
        horario_inicio = data.get("horario_inicio")
        horario_fim = data.get("horario_fim")

        conflito = Reuniao.objects.filter(
            local_id=local,
            data_inicio=data_inicio,
            status__in=["pendente", "aprovado"]
        ).filter(
            Q(horario_inicio__lt=horario_fim) & Q(horario_fim__gt=horario_inicio)
        ).exists()

        return JsonResponse({"conflito": conflito})