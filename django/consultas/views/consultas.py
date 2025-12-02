"""
Views para gerenciamento de consultas
"""

from django.views.generic import ListView, CreateView, UpdateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from consultas.models import Consulta, HistoricoConsulta
from consultas.forms import ConsultaForm, ConsultaUpdateForm
from pets.models import Animal
from users.models import User


class VeterinarioRequiredMixin(UserPassesTestMixin):
    """Mixin para verificar se o usuário é veterinário"""
    
    def test_func(self):
        return self.request.user.is_veterinario()


class ConsultaListView(LoginRequiredMixin, VeterinarioRequiredMixin, ListView):
    """Lista todas as consultas do veterinário"""
    model = Consulta
    template_name = 'consultas/consulta_list.html'
    context_object_name = 'consultas'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Consulta.objects.filter(
            veterinario=self.request.user
        ).select_related(
            'animal', 'animal__proprietario', 'animal__raca', 'animal__tipo_animal'
        ).order_by('-data_hora')
        
        # Filtros
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        tipo = self.request.GET.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        
        busca = self.request.GET.get('busca')
        if busca:
            queryset = queryset.filter(
                Q(animal__nome__icontains=busca) |
                Q(animal__proprietario__username__icontains=busca) |
                Q(motivo__icontains=busca)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Consulta.STATUS_CHOICES
        context['tipo_choices'] = Consulta.TIPO_CHOICES
        context['filtro_status'] = self.request.GET.get('status', '')
        context['filtro_tipo'] = self.request.GET.get('tipo', '')
        context['busca'] = self.request.GET.get('busca', '')
        return context


class ConsultaCreateView(LoginRequiredMixin, VeterinarioRequiredMixin, CreateView):
    """Cria uma nova consulta"""
    model = Consulta
    form_class = ConsultaForm
    template_name = 'consultas/consulta_form.html'
    success_url = reverse_lazy('consultas:consulta_list')
    
    def get_form_kwargs(self):
        """Adiciona o veterinário à instância antes da validação"""
        kwargs = super().get_form_kwargs()
        if kwargs.get('instance') is None:
            kwargs['instance'] = Consulta()
        # Seta veterinário e criado_por na instância antes da validação
        kwargs['instance'].veterinario = self.request.user
        kwargs['instance'].criado_por = self.request.user
        return kwargs
    
    def form_valid(self, form):
        # Garante que veterinário e criado_por estão setados
        form.instance.veterinario = self.request.user
        form.instance.criado_por = self.request.user
        
        # Salva a instância
        response = super().form_valid(form)
        
        # Registra no histórico
        HistoricoConsulta.objects.create(
            consulta=self.object,
            acao='AGENDAMENTO',
            descricao=f'Consulta agendada para {self.object.data_hora.strftime("%d/%m/%Y às %H:%M")}',
            usuario=self.request.user
        )
        
        messages.success(self.request, 'Consulta agendada com sucesso!')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nova Consulta'
        context['botao_submit'] = 'Agendar Consulta'
        return context


class ConsultaUpdateView(LoginRequiredMixin, VeterinarioRequiredMixin, UpdateView):
    """Atualiza uma consulta existente"""
    model = Consulta
    template_name = 'consultas/consulta_form.html'
    fields = ['animal', 'data_hora', 'tipo', 'status', 'motivo', 'observacoes']
    success_url = reverse_lazy('consultas:consulta_list')
    
    def get_queryset(self):
        # Apenas consultas do veterinário logado
        return Consulta.objects.filter(veterinario=self.request.user)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Adiciona classes CSS aos campos
        for field in form.fields:
            form.fields[field].widget.attrs['class'] = 'form-control'
        
        # Configura o campo de data e hora
        form.fields['data_hora'].widget.attrs.update({
            'type': 'datetime-local',
            'class': 'form-control'
        })
        
        # Filtra apenas animais ativos
        form.fields['animal'].queryset = Animal.objects.filter(ativo=True).select_related(
            'proprietario', 'raca', 'tipo_animal'
        )
        
        return form
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Registra no histórico se houve mudança de status
        if 'status' in form.changed_data:
            HistoricoConsulta.objects.create(
                consulta=self.object,
                acao='OBSERVACAO',
                descricao=f'Status alterado para: {self.object.get_status_display()}',
                usuario=self.request.user
            )
        
        messages.success(self.request, 'Consulta atualizada com sucesso!')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Consulta'
        context['botao_submit'] = 'Salvar Alterações'
        return context


class ConsultaDetailView(LoginRequiredMixin, VeterinarioRequiredMixin, DetailView):
    """Exibe detalhes de uma consulta"""
    model = Consulta
    template_name = 'consultas/consulta_detail.html'
    context_object_name = 'consulta'
    
    def get_queryset(self):
        # Apenas consultas do veterinário logado
        return Consulta.objects.filter(
            veterinario=self.request.user
        ).select_related(
            'animal', 'animal__proprietario', 'animal__raca', 'animal__tipo_animal',
            'veterinario', 'criado_por'
        ).prefetch_related('historico')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Busca prontuário se existir
        try:
            context['prontuario'] = self.object.prontuario
            context['receitas'] = self.object.prontuario.receitas.all()
        except:
            context['prontuario'] = None
            context['receitas'] = []
        
        # Histórico da consulta
        context['historico'] = self.object.historico.select_related('usuario').order_by('-criado_em')
        
        return context


class ConsultaCancelarView(LoginRequiredMixin, VeterinarioRequiredMixin, View):
    """Cancela uma consulta"""
    
    def post(self, request, pk):
        consulta = get_object_or_404(Consulta, pk=pk, veterinario=request.user)
        
        if not consulta.pode_cancelar():
            messages.error(request, 'Esta consulta não pode ser cancelada.')
            return redirect('consultas:consulta_detail', pk=pk)
        
        consulta.status = 'CANCELADA'
        consulta.save()
        
        # Registra no histórico
        HistoricoConsulta.objects.create(
            consulta=consulta,
            acao='CANCELAMENTO',
            descricao='Consulta cancelada pelo veterinário',
            usuario=request.user
        )
        
        messages.success(request, 'Consulta cancelada com sucesso!')
        return redirect('consultas:consulta_list')


class ConsultaIniciarAtendimentoView(LoginRequiredMixin, VeterinarioRequiredMixin, View):
    """Inicia o atendimento de uma consulta"""
    
    def post(self, request, pk):
        consulta = get_object_or_404(Consulta, pk=pk, veterinario=request.user)
        
        if not consulta.pode_iniciar_atendimento():
            messages.error(request, 'Esta consulta não pode ser iniciada.')
            return redirect('consultas:consulta_detail', pk=pk)
        
        consulta.status = 'EM_ATENDIMENTO'
        consulta.save()
        
        # Registra no histórico
        HistoricoConsulta.objects.create(
            consulta=consulta,
            acao='INICIO_ATENDIMENTO',
            descricao='Atendimento iniciado',
            usuario=request.user
        )
        
        messages.success(request, 'Atendimento iniciado! Agora você pode criar o prontuário.')
        return redirect('consultas:prontuario_create', consulta_pk=pk)
