from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Reuniao, Usuario
from .forms import ReuniaoForm


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redireciona após login bem-sucedido
        else:
            messages.error(request, "Matrícula ou senha incorretos!")

    return render(request, "agenda/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")  # Redireciona para a página de login

@login_required
def home(request):
    reunioes = Reuniao.objects.all()  # Obtém todas as reuniões cadastradas

    if request.method == 'POST':
        form = ReuniaoForm(request.POST)
        if form.is_valid():
            reuniao = form.save(commit=False)  # Não salva ainda no banco
            reuniao.save()  # Salva a reunião

            # Adiciona os colaboradores selecionados no formulário
            colaboradores_selecionados = form.cleaned_data['colaboradores']
            reuniao.colaboradores.set(colaboradores_selecionados)  

            # Adiciona o usuário logado como colaborador
            reuniao.colaboradores.add(request.user)

            return redirect('home')  # Redireciona para evitar reenvio do formulário
    else:
        form = ReuniaoForm()

    return render(request, "agenda/home.html", {"form": form, "reunioes": reunioes})




def colaboradores_disponiveis(request):
    data_inicio = request.GET.get("data_inicio")
    horario_inicio = request.GET.get("horario_inicio")
    horario_fim = request.GET.get("horario_fim")

    if data_inicio and horario_inicio and horario_fim:
        # Busca colaboradores ocupados nesse intervalo de tempo
        colaboradores_ocupados = Reuniao.objects.filter(
            data_inicio=data_inicio
        ).filter(
            Q(horario_inicio__lt=horario_fim) & Q(horario_fim__gt=horario_inicio)
        ).values_list('colaboradores', flat=True)

        # Retorna os colaboradores disponíveis
        colaboradores_disponiveis = Usuario.objects.filter(role='colaborador').exclude(id__in=colaboradores_ocupados)

        # Retorna os dados em JSON
        colaboradores_json = list(colaboradores_disponiveis.values("id", "nome"))
        return JsonResponse({"colaboradores": colaboradores_json})

    return JsonResponse({"colaboradores": []})


