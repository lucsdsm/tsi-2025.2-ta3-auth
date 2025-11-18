"""
Views para gerenciamento de receitas
"""

from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from consultas.models import Prontuario, Receita, HistoricoConsulta
from .consultas import VeterinarioRequiredMixin


class ReceitaCreateView(LoginRequiredMixin, VeterinarioRequiredMixin, CreateView):
    """Cria uma receita para um prontuário"""
    model = Receita
    template_name = 'consultas/receita_form.html'
    fields = ['medicamento', 'dosagem', 'frequencia', 'duracao', 'via_administracao', 'instrucoes']
    
    def dispatch(self, request, *args, **kwargs):
        self.prontuario = get_object_or_404(
            Prontuario, 
            pk=self.kwargs['prontuario_pk'],
            consulta__veterinario=request.user
        )
        return super().dispatch(request, *args, **kwargs)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Adiciona classes CSS aos campos
        for field in form.fields:
            if field == 'instrucoes':
                form.fields[field].widget.attrs['class'] = 'form-control'
                form.fields[field].widget.attrs['rows'] = '3'
            else:
                form.fields[field].widget.attrs['class'] = 'form-control'
        
        return form
    
    def form_valid(self, form):
        form.instance.prontuario = self.prontuario
        response = super().form_valid(form)
        
        # Registra no histórico
        HistoricoConsulta.objects.create(
            consulta=self.prontuario.consulta,
            acao='RECEITA_ADICIONADA',
            descricao=f'Receita adicionada: {self.object.medicamento}',
            usuario=self.request.user
        )
        
        messages.success(self.request, 'Receita adicionada com sucesso!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('consultas:consulta_detail', kwargs={'pk': self.prontuario.consulta.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prontuario'] = self.prontuario
        context['consulta'] = self.prontuario.consulta
        context['titulo'] = 'Nova Receita'
        context['botao_submit'] = 'Adicionar Receita'
        return context


class ReceitaUpdateView(LoginRequiredMixin, VeterinarioRequiredMixin, UpdateView):
    """Atualiza uma receita existente"""
    model = Receita
    template_name = 'consultas/receita_form.html'
    fields = ['medicamento', 'dosagem', 'frequencia', 'duracao', 'via_administracao', 'instrucoes']
    
    def get_queryset(self):
        # Apenas receitas de prontuários do veterinário logado
        return Receita.objects.filter(prontuario__consulta__veterinario=self.request.user)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Adiciona classes CSS aos campos
        for field in form.fields:
            if field == 'instrucoes':
                form.fields[field].widget.attrs['class'] = 'form-control'
                form.fields[field].widget.attrs['rows'] = '3'
            else:
                form.fields[field].widget.attrs['class'] = 'form-control'
        
        return form
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Registra no histórico
        HistoricoConsulta.objects.create(
            consulta=self.object.prontuario.consulta,
            acao='OBSERVACAO',
            descricao=f'Receita atualizada: {self.object.medicamento}',
            usuario=self.request.user
        )
        
        messages.success(self.request, 'Receita atualizada com sucesso!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('consultas:consulta_detail', kwargs={'pk': self.object.prontuario.consulta.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prontuario'] = self.object.prontuario
        context['consulta'] = self.object.prontuario.consulta
        context['titulo'] = 'Editar Receita'
        context['botao_submit'] = 'Salvar Alterações'
        return context


class ReceitaDeleteView(LoginRequiredMixin, VeterinarioRequiredMixin, DeleteView):
    """Exclui uma receita"""
    model = Receita
    template_name = 'consultas/receita_confirm_delete.html'
    
    def get_queryset(self):
        # Apenas receitas de prontuários do veterinário logado
        return Receita.objects.filter(prontuario__consulta__veterinario=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('consultas:consulta_detail', kwargs={'pk': self.object.prontuario.consulta.pk})
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        consulta = self.object.prontuario.consulta
        medicamento = self.object.medicamento
        
        response = super().delete(request, *args, **kwargs)
        
        # Registra no histórico
        HistoricoConsulta.objects.create(
            consulta=consulta,
            acao='OBSERVACAO',
            descricao=f'Receita removida: {medicamento}',
            usuario=request.user
        )
        
        messages.success(request, 'Receita removida com sucesso!')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['consulta'] = self.object.prontuario.consulta
        return context
