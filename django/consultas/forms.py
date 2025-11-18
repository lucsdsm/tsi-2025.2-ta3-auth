"""
Formulários customizados para o app de consultas
"""

from django import forms
from django.utils import timezone
from consultas.models import Consulta
from pets.models import Animal


class ConsultaForm(forms.ModelForm):
    """
    Formulário para criar/editar consultas com widgets customizados
    """
    
    data_hora = forms.DateTimeField(
        label='Data e Hora',
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'DD/MM/YYYY HH:MM'
            }
        ),
        input_formats=[
            '%Y-%m-%dT%H:%M',  # Formato HTML5 datetime-local
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M',
            '%d/%m/%Y %H:%M',  # Formato brasileiro
            '%d/%m/%Y %H:%M:%S',
        ],
        help_text='Formato: DD/MM/YYYY HH:MM (exemplo: 20/11/2025 14:30)'
    )
    
    animal = forms.ModelChoiceField(
        queryset=Animal.objects.none(),  # Será filtrado na view
        label='Animal',
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Selecione o animal que será atendido'
    )
    
    tipo = forms.ChoiceField(
        choices=Consulta.TIPO_CHOICES,
        label='Tipo de Atendimento',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    
    motivo = forms.CharField(
        label='Motivo da Consulta',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Descreva o motivo do atendimento...'
        })
    )
    
    observacoes = forms.CharField(
        label='Observações',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Observações adicionais (opcional)...'
        })
    )
    
    class Meta:
        model = Consulta
        fields = ['animal', 'data_hora', 'tipo', 'motivo', 'observacoes']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra animais ativos
        self.fields['animal'].queryset = Animal.objects.filter(
            ativo=True
        ).select_related('proprietario', 'raca', 'tipo_animal')
    
    def clean_data_hora(self):
        """Valida a data/hora da consulta"""
        data_hora = self.cleaned_data.get('data_hora')
        
        if data_hora:
            # Verifica se não é no passado (apenas para novas consultas)
            if not self.instance.pk:
                # Garante que ambas as datas estejam timezone-aware
                agora = timezone.now()
                
                # Se data_hora for naive, adiciona o timezone atual
                if timezone.is_naive(data_hora):
                    data_hora = timezone.make_aware(data_hora)
                
                # Permite agendamentos no mesmo dia se for no futuro
                # Verifica apenas se a data é anterior a hoje
                if data_hora.date() < agora.date():
                    raise forms.ValidationError(
                        'Não é possível agendar consultas em datas passadas.'
                    )
                
                # Se for hoje, verifica se o horário já passou (com margem de 5 minutos)
                if data_hora.date() == agora.date():
                    # Subtrai 5 minutos do horário agendado para dar margem
                    margem = timezone.timedelta(minutes=5)
                    if (data_hora - margem) < agora:
                        raise forms.ValidationError(
                            f'Para agendamentos no dia de hoje, escolha um horário com pelo menos 5 minutos de antecedência. Horário atual: {agora.strftime("%H:%M")}'
                        )
                
                # Retorna a data com timezone se foi convertida
                return data_hora
        
        return data_hora


class ConsultaUpdateForm(ConsultaForm):
    """
    Formulário para atualizar consultas (inclui campo de status)
    """
    
    status = forms.ChoiceField(
        choices=Consulta.STATUS_CHOICES,
        label='Status',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    
    class Meta:
        model = Consulta
        fields = ['animal', 'data_hora', 'tipo', 'status', 'motivo', 'observacoes']
