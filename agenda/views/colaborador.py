# Módulo de açoes dos usuarios do tipo 'colaborador'
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from ..models import Reuniao
from ..forms import ReuniaoForm

#View para carregar funções da tela Home (colaborador)
@login_required
def home(request):
    # Verifica se o tipo de usuario é 'colaborador'. Caso não, é redirecionado para o login
    if request.user.role != 'colaborador':
        return redirect('login')  

    reunioes = Reuniao.objects.filter(Q(status='aprovado') | Q(criado_por=request.user))

    #Carrega e salva formulário para Solicitar Reunião
    if request.method == 'POST':
        form = ReuniaoForm(request.POST)
        if form.is_valid():
            reuniao = form.save(commit=False) 
            # Formulário salvo no nome daquele que solicitou (usuario)
            reuniao.criado_por = request.user 
            ''' Campo 'status' é salvo no banco por padrão como 'pendente' pois ainda não 
            foi autorizado'''
            reuniao.status = 'pendente' 
            reuniao.save()
            # Retorna colaboradores a partir da logica do forms
            reuniao.colaboradores.set(form.cleaned_data['colaboradores'])
            reuniao.colaboradores.add(request.user)

            messages.success(request, "Pedido de reunião enviado para aprovação!")
            return redirect('home')
    else:
        form = ReuniaoForm()

    return render(request, "agenda/home.html", {"form": form, "reunioes": reunioes})

#View para carregar as funções da pagina pedidos (colaborador)
@login_required
def page_pedidos(request):
    # Carrega todos os dados de reuniões pedidas/associadas ao usuario logado
    reunioes = (
        Reuniao.objects.filter(colaboradores=request.user) | 
        # Filtra pedidos/reuniões de datas mais recentes
        Reuniao.objects.filter(criado_por=request.user)
    ).distinct().order_by('-data_inicio', '-horario_inicio')

    return render(request, "agenda/pedidos.html", {"reunioes": reunioes})