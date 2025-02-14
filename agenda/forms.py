from django import forms
from datetime import date
from django.db.models import Q  
from .models import Reuniao, Local, Usuario

class ReuniaoForm(forms.ModelForm):
    local = forms.ModelChoiceField(
        queryset=Local.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    colaboradores = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.filter(role='colaborador'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Reuniao
        fields = ['local', 'titulo', 'data_inicio', 'data_fim', 'horario_inicio', 'horario_fim', 'colaboradores', 'descricao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_fim': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'horario_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'horario_fim': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        local = cleaned_data.get("local")
        data_inicio = cleaned_data.get("data_inicio")
        horario_inicio = cleaned_data.get("horario_inicio")
        horario_fim = cleaned_data.get("horario_fim")

        # Só verifica conflitos se houver registros no banco
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_inicio'].initial = date.today()
        self.fields['data_fim'].initial = date.today()
