"""
Models para o sistema de consultas veterinárias

Hierarquia:
- Consulta (agendamento de consulta)
  └── Prontuario (registro médico da consulta)
      ├── Receita (prescrições médicas)
      └── HistoricoConsulta (histórico de atendimentos)

Relacionamentos:
- Uma Consulta pertence a UM animal e UM veterinário
- Um Prontuario pertence a UMA consulta
- Uma Receita pertence a UM prontuário
- HistoricoConsulta registra todas as ações realizadas
"""

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from pets.models import Animal


class Consulta(models.Model):
    """
    Representa uma consulta veterinária agendada ou realizada
    """
    STATUS_CHOICES = [
        ('AGENDADA', 'Agendada'),
        ('CONFIRMADA', 'Confirmada'),
        ('EM_ATENDIMENTO', 'Em Atendimento'),
        ('REALIZADA', 'Realizada'),
        ('CANCELADA', 'Cancelada'),
        ('FALTOU', 'Paciente Faltou'),
    ]
    
    TIPO_CHOICES = [
        ('CONSULTA', 'Consulta de Rotina'),
        ('RETORNO', 'Retorno'),
        ('EMERGENCIA', 'Emergência'),
        ('CIRURGIA', 'Cirurgia'),
        ('VACINACAO', 'Vacinação'),
        ('EXAME', 'Exame'),
    ]
    
    # Relacionamentos principais
    animal = models.ForeignKey(
        Animal,
        on_delete=models.PROTECT,
        related_name='consultas',
        verbose_name='Animal',
        help_text='Animal que será atendido'
    )
    
    veterinario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='consultas_veterinario',
        limit_choices_to={'user_type': 'VETERINARIO'},
        verbose_name='Veterinário',
        help_text='Veterinário responsável pelo atendimento'
    )
    
    # Dados da consulta
    data_hora = models.DateTimeField(
        verbose_name='Data e Hora',
        help_text='Data e hora da consulta'
    )
    
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='CONSULTA',
        verbose_name='Tipo de Atendimento'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='AGENDADA',
        verbose_name='Status'
    )
    
    motivo = models.TextField(
        verbose_name='Motivo da Consulta',
        help_text='Descrição do motivo do atendimento'
    )
    
    observacoes = models.TextField(
        blank=True,
        verbose_name='Observações',
        help_text='Observações adicionais sobre o agendamento'
    )
    
    # Controle
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='consultas_criadas',
        verbose_name='Criado por'
    )
    
    class Meta:
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'
        ordering = ['-data_hora']
        indexes = [
            models.Index(fields=['data_hora', 'veterinario']),
            models.Index(fields=['animal', 'data_hora']),
        ]
    
    def __str__(self):
        return f"{self.animal.nome} - {self.get_tipo_display()} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"
    
    def clean(self):
        """Validações customizadas"""
        # Verifica veterinario apenas se já foi setado (pode ser None durante criação via form)
        # Usa veterinario_id para evitar query desnecessária e erro quando não setado
        if self.veterinario_id:
            try:
                if not self.veterinario.is_veterinario():
                    raise ValidationError({'veterinario': 'O usuário selecionado não é um veterinário.'})
            except User.DoesNotExist:
                pass
        
        if not self.pk and self.data_hora and self.data_hora < timezone.now():
            raise ValidationError({'data_hora': 'Não é possível agendar consultas no passado.'})
    
    def pode_editar(self):
        return self.status in ['AGENDADA', 'CONFIRMADA']
    
    def pode_cancelar(self):
        return self.status in ['AGENDADA', 'CONFIRMADA']
    
    def pode_iniciar_atendimento(self):
        return self.status in ['AGENDADA', 'CONFIRMADA']
    
    @property
    def tem_prontuario(self):
        return hasattr(self, 'prontuario')


class Prontuario(models.Model):
    consulta = models.OneToOneField(Consulta, on_delete=models.PROTECT, related_name='prontuario', verbose_name='Consulta', help_text='Consulta relacionada a este prontuário')
    peso = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='Peso (kg)', help_text='Peso do animal em quilogramas')
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name='Temperatura (°C)', help_text='Temperatura corporal em graus Celsius')
    frequencia_cardiaca = models.IntegerField(null=True, blank=True, verbose_name='Frequência Cardíaca (bpm)', help_text='Batimentos por minuto')
    frequencia_respiratoria = models.IntegerField(null=True, blank=True, verbose_name='Frequência Respiratória (rpm)', help_text='Respirações por minuto')
    anamnese = models.TextField(verbose_name='Anamnese', help_text='História clínica e queixas do animal')
    exame_fisico = models.TextField(verbose_name='Exame Físico', help_text='Achados do exame físico')
    diagnostico = models.TextField(verbose_name='Diagnóstico', help_text='Diagnóstico médico veterinário')
    tratamento = models.TextField(verbose_name='Tratamento', help_text='Plano de tratamento recomendado')
    observacoes = models.TextField(blank=True, verbose_name='Observações', help_text='Observações adicionais')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Prontuário'
        verbose_name_plural = 'Prontuários'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"Prontuário - {self.consulta}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.consulta.status != 'REALIZADA':
            self.consulta.status = 'REALIZADA'
            self.consulta.save(update_fields=['status', 'atualizado_em'])


class Receita(models.Model):
    prontuario = models.ForeignKey(Prontuario, on_delete=models.PROTECT, related_name='receitas', verbose_name='Prontuário')
    medicamento = models.CharField(max_length=200, verbose_name='Medicamento', help_text='Nome do medicamento prescrito')
    dosagem = models.CharField(max_length=100, verbose_name='Dosagem', help_text='Dosagem do medicamento')
    frequencia = models.CharField(max_length=100, verbose_name='Frequência', help_text='Frequência de administração')
    duracao = models.CharField(max_length=100, verbose_name='Duração', help_text='Duração do tratamento')
    via_administracao = models.CharField(max_length=50, choices=[('ORAL', 'Oral'), ('TOPICA', 'Tópica'), ('INJETAVEL_IM', 'Injetável - Intramuscular'), ('INJETAVEL_IV', 'Injetável - Intravenosa'), ('INJETAVEL_SC', 'Injetável - Subcutânea'), ('OCULAR', 'Ocular'), ('AURICULAR', 'Auricular'), ('OUTRA', 'Outra')], default='ORAL', verbose_name='Via de Administração')
    instrucoes = models.TextField(blank=True, verbose_name='Instruções Especiais', help_text='Instruções adicionais para o uso do medicamento')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Receita'
        verbose_name_plural = 'Receitas'
        ordering = ['medicamento']
    
    def __str__(self):
        return f"{self.medicamento} - {self.dosagem}"


class HistoricoConsulta(models.Model):
    ACAO_CHOICES = [('AGENDAMENTO', 'Agendamento Criado'), ('CONFIRMACAO', 'Consulta Confirmada'), ('INICIO_ATENDIMENTO', 'Atendimento Iniciado'), ('PRONTUARIO_CRIADO', 'Prontuário Criado'), ('PRONTUARIO_ATUALIZADO', 'Prontuário Atualizado'), ('RECEITA_ADICIONADA', 'Receita Adicionada'), ('CANCELAMENTO', 'Consulta Cancelada'), ('OBSERVACAO', 'Observação Adicionada')]
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='historico', verbose_name='Consulta')
    acao = models.CharField(max_length=30, choices=ACAO_CHOICES, verbose_name='Ação')
    descricao = models.TextField(verbose_name='Descrição', help_text='Detalhes da ação realizada')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Usuário', help_text='Usuário que realizou a ação')
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Histórico de Consulta'
        verbose_name_plural = 'Históricos de Consultas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"{self.get_acao_display()} - {self.consulta} - {self.criado_em.strftime('%d/%m/%Y %H:%M')}"
