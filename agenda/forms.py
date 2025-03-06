from django import forms
from datetime import date
from django.db.models import Q  
from .models import Reuniao, Local, Usuario

class ReuniaoForm(forms.ModelForm):
    local = forms.ModelChoiceField(
        queryset=Local.objects.all(),
        empty_label="Selecione o Local da Reunião",
        widget=forms.Select(attrs={'class': 'form-control input-cinza'})
    )
    colaboradores = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.filter(Q(role='colaborador') | Q(role='lider')),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'id': 'id_colaboradores',
        }),
        required=False
    )

    class Meta:
        model = Reuniao
        fields = ['local', 'titulo', 'data_inicio', 'horario_inicio', 'horario_fim', 'colaboradores', 'descricao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control input-cinza '}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control input-cinza'}),
            'horario_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control input-cinza'}),
            'horario_fim': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control input-cinza'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control input-cinza', 'rows': 3}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        local = cleaned_data.get("local")
        data_inicio = cleaned_data.get("data_inicio")
        horario_inicio = cleaned_data.get("horario_inicio")
        horario_fim = cleaned_data.get("horario_fim")

        if local and data_inicio and horario_inicio and horario_fim and Reuniao.objects.exists():
            conflito = Reuniao.objects.filter(
                local=local,
                data_inicio=data_inicio
            ).filter(
                Q(horario_inicio__lt=horario_fim) & Q(horario_fim__gt=horario_inicio)
            ).exists()
            if conflito:
                raise forms.ValidationError("Já existe uma reunião agendada para esse local nesse intervalo de tempo.")
        return cleaned_data

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_inicio'].initial = date.today()
        if user and user.is_authenticated:
            self.fields['colaboradores'].queryset = Usuario.objects.filter(Q(role='colaborador') | Q(role='lider')).exclude(id=user.id)
        self.fields['colaboradores'].widget.attrs['id'] = 'id_colaboradores'
        self.fields['colaboradores'].label_from_instance = lambda obj: f"{obj.username} - {obj.nome} - {obj.setor}"

