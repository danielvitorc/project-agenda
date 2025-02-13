from django.contrib.auth.models import AbstractUser
from django.db import models

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
    
    email = models.EmailField("email", blank=True, null=True, unique=False)  # Agora realmente opcional
    
    contato = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='colaborador')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nome']  # Certifique-se de que 'email' não está aqui

    def __str__(self):
        return f"{self.nome} ({self.get_role_display()})"
