from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

class Setor(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome
    
    def listar_colaboradores(self):
        return self.usuario_set.filter(role='colaborador')
    
class Local(models.Model):
    nome = models.CharField(max_length=65)

    def __str__(self):
        return self.nome
    


class Usuario(AbstractUser):
    ROLE_CHOICES = [
        ('lider', 'Líder'),
        ('colaborador', 'Colaborador'),
        ('admin', 'Administrador'),
    ]

    username = models.CharField(max_length=20, unique=True)  # Matrícula como username
    nome = models.CharField(max_length=150)
    setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, null=True, blank=True)
    
    email = models.EmailField("email", blank=True, null=True, unique=False)  
    
    contato = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='colaborador')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nome'] 

    def __str__(self):
        return f"{self.nome} ({self.get_role_display()})"

class Reuniao(models.Model):
    STATUS_CHOICES = [
        ('pendente','Pendente'),
        ('aprovado','Aprovado'),
        ('rejeitado','Rejeitado'),
    ]
    local = models.ForeignKey('Local', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    data_inicio = models.DateField(default=date.today)
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    colaboradores = models.ManyToManyField('Usuario', blank=True)
    descricao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente') 
    criado_por = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='reunioes_solicitadas')
    motivo_rejeicao = models.TextField(blank=True, null=True)  

    def __str__(self):
        return f"{self.titulo} - {self.local.nome} ({self.get_status_display()})"
