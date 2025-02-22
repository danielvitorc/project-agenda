# Módulo que gera api dos registros de reunião no banco para o calendário
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from ..models import Reuniao, Usuario

# View que pega o registro dos pedidos do banco para o JSON
def get_reunioes(request):
    reunioes = Reuniao.objects.all()
    eventos = [
        {
            "title": reuniao.titulo,
            "start": f"{reuniao.data_inicio}T{reuniao.horario_inicio}",
            "end": f"{reuniao.data_fim}T{reuniao.horario_fim}",
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

    '''
    permite filtrar colaboradores disponiveis para a data e horario registrado  
    '''
    if data_inicio and horario_inicio and horario_fim:
        colaboradores_ocupados = Reuniao.objects.filter(
            data_inicio=data_inicio
        ).filter(
            Q(horario_inicio__lt=horario_fim) & Q(horario_fim__gt=horario_inicio)
        ).values_list('colaboradores', flat=True)

        colaboradores_disponiveis = Usuario.objects.filter(role='colaborador').exclude(id__in=colaboradores_ocupados)
        return JsonResponse({"colaboradores": list(colaboradores_disponiveis.values("id", "nome"))})

    return JsonResponse({"colaboradores": []})

# View que carrega dados aos moldais de detalhes de uma reunião
def eventos_json(request):
    reunioes = Reuniao.objects.all()
    eventos = [
        {
            "id": reuniao.id,
            "title": reuniao.titulo,
            "start": f"{reuniao.data_inicio}T{reuniao.horario_inicio}",
            "end": f"{reuniao.data_fim}T{reuniao.horario_fim}",
            "descricao": reuniao.descricao,
            "local": reuniao.local.nome,
            "colaboradores": ", ".join([f"{colab.username} - {colab.nome}" for colab in reuniao.colaboradores.all()]),
            "status": reuniao.status.lower().strip(),
        }
        for reuniao in reunioes
    ]
    return JsonResponse(eventos, safe=False)