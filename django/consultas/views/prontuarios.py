"""
Views para gerenciamento de prontuários
"""

from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from consultas.models import Consulta, Prontuario, HistoricoConsulta
from .consultas import VeterinarioRequiredMixin


class ProntuarioCreateView(LoginRequiredMixin, VeterinarioRequiredMixin, CreateView):
    """Cria um prontuário para uma consulta"""
    model = Prontuario
    template_name = 'consultas/prontuario_form.html'
    fields = [
        'peso', 'temperatura', 'frequencia_cardiaca', 'frequencia_respiratoria',
        'anamnese', 'exame_fisico', 'diagnostico', 'tratamento', 'observacoes'
    ]
    
    def dispatch(self, request, *args, **kwargs):
        self.consulta = get_object_or_404(
            Consulta, 
            pk=self.kwargs['consulta_pk'],
            veterinario=request.user
        )
        
        # Verifica se já existe prontuário
        if hasattr(self.consulta, 'prontuario'):
            messages.warning(request, 'Esta consulta já possui prontuário. Você pode editá-lo.')
            return redirect('consultas:prontuario_update', pk=self.consulta.prontuario.pk)
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Adiciona classes CSS aos campos
        for field in form.fields:
            if field in ['peso', 'temperatura', 'frequencia_cardiaca', 'frequencia_respiratoria']:
                form.fields[field].widget.attrs['class'] = 'form-control'
                form.fields[field].widget.attrs['type'] = 'number'
                form.fields[field].widget.attrs['step'] = '0.1' if field in ['peso', 'temperatura'] else '1'
            else:
                form.fields[field].widget.attrs['class'] = 'form-control'
                form.fields[field].widget.attrs['rows'] = '4'
        
        return form
    
    def form_valid(self, form):
        form.instance.consulta = self.consulta
        response = super().form_valid(form)
        
        # Registra no histórico
        HistoricoConsulta.objects.create(
            consulta=self.consulta,
            acao='PRONTUARIO_CRIADO',
            descricao='Prontuário criado',
            usuario=self.request.user
        )
        
        messages.success(self.request, 'Prontuário criado com sucesso!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('consultas:consulta_detail', kwargs={'pk': self.consulta.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['consulta'] = self.consulta
        context['titulo'] = 'Criar Prontuário'
        context['botao_submit'] = 'Salvar Prontuário'
        return context


class ProntuarioUpdateView(LoginRequiredMixin, VeterinarioRequiredMixin, UpdateView):
    """Atualiza um prontuário existente"""
    model = Prontuario
    template_name = 'consultas/prontuario_form.html'
    fields = [
        'peso', 'temperatura', 'frequencia_cardiaca', 'frequencia_respiratoria',
        'anamnese', 'exame_fisico', 'diagnostico', 'tratamento', 'observacoes'
    ]
    
    def get_queryset(self):
        # Apenas prontuários de consultas do veterinário logado
        return Prontuario.objects.filter(consulta__veterinario=self.request.user)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Adiciona classes CSS aos campos
        for field in form.fields:
            if field in ['peso', 'temperatura', 'frequencia_cardiaca', 'frequencia_respiratoria']:
                form.fields[field].widget.attrs['class'] = 'form-control'
                form.fields[field].widget.attrs['type'] = 'number'
                form.fields[field].widget.attrs['step'] = '0.1' if field in ['peso', 'temperatura'] else '1'
            else:
                form.fields[field].widget.attrs['class'] = 'form-control'
                form.fields[field].widget.attrs['rows'] = '4'
        
        return form
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Registra no histórico
        HistoricoConsulta.objects.create(
            consulta=self.object.consulta,
            acao='PRONTUARIO_ATUALIZADO',
            descricao='Prontuário atualizado',
            usuario=self.request.user
        )
        
        messages.success(self.request, 'Prontuário atualizado com sucesso!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('consultas:consulta_detail', kwargs={'pk': self.object.consulta.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['consulta'] = self.object.consulta
        context['titulo'] = 'Editar Prontuário'
        context['botao_submit'] = 'Salvar Alterações'
        return context


class ProntuarioDetailView(LoginRequiredMixin, VeterinarioRequiredMixin, DetailView):
    """Exibe detalhes de um prontuário"""
    model = Prontuario
    template_name = 'consultas/prontuario_detail.html'
    context_object_name = 'prontuario'
    
    def get_queryset(self):
        # Apenas prontuários de consultas do veterinário logado
        return Prontuario.objects.filter(
            consulta__veterinario=self.request.user
        ).select_related(
            'consulta', 'consulta__animal', 'consulta__animal__proprietario',
            'consulta__animal__raca', 'consulta__animal__tipo_animal'
        ).prefetch_related('receitas')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['consulta'] = self.object.consulta
        context['receitas'] = self.object.receitas.all()
        return context
