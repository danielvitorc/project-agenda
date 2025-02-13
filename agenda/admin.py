from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Setor, Local

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'nome', 'email', 'setor', 'role', 'is_active', 'is_staff')
    search_fields = ('username', 'nome', 'email')
    list_filter = ('role', 'setor')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('nome', 'email', 'contato', 'setor')}),
        ('Permissões', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

class SetorAdmin(admin.ModelAdmin):
    list_display = ['nome']  # Exibe apenas o nome na listagem principal
    readonly_fields = ['listar_colaboradores']  # Torna o campo somente leitura no admin

    def listar_colaboradores(self, obj):
        colaboradores = obj.usuario_set.filter(role='colaborador')
        return ", ".join([user.nome for user in colaboradores]) if colaboradores else "Nenhum colaborador"

    listar_colaboradores.short_description = "Colaboradores"

admin.site.register(Local)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Setor, SetorAdmin)
