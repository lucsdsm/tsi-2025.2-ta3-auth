"""
Views para o sistema de gerenciamento de Pets

Funcionalidades:
- CRUD completo para TipoAnimal e Raça (apenas admin/staff)
- Criação e listagem de Animais (apenas proprietário)
- API para buscar raças dinamicamente
"""

from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import TipoAnimal, Raca, Animal


# ====================================
# Views de animal (pet)
# ====================================

class AnimalListView(LoginRequiredMixin, ListView):
    """Lista apenas os animais do usuário logado"""
    model = Animal
    template_name = 'animal_list.html'
    context_object_name = 'animais'
    
    def get_queryset(self):
        # Retorna apenas animais ativos do usuário logado
        return Animal.objects.filter(
            proprietario=self.request.user,
            ativo=True
        ).select_related('tipo_animal', 'raca').order_by('-criado_em')


class AnimalCreateView(LoginRequiredMixin, CreateView):
    """Cadastro de novo animal (somente usuário logado)"""
    model = Animal
    fields = ['nome', 'tipo_animal', 'raca', 'sexo', 'data_nascimento', 'observacoes']
    template_name = 'animal_form.html'
    success_url = reverse_lazy('animal_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_de_animais'] = TipoAnimal.objects.filter(ativo=True)
        context['titulo'] = 'Cadastrar Novo Pet'
        context['botao'] = 'Cadastrar'
        return context
    
    def form_valid(self, form):
        # Associa o animal ao usuário logado automaticamente
        form.instance.proprietario = self.request.user
        messages.success(
            self.request,
            f"✅ O pet '{form.instance.nome}' foi cadastrado com sucesso!"
        )
        return super().form_valid(form)


class AnimalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edição de animal (proprietário ou funcionários)"""
    model = Animal
    fields = ['nome', 'tipo_animal', 'raca', 'sexo', 'data_nascimento', 'observacoes']
    template_name = 'animal_form.html'
    success_url = reverse_lazy('animal_list')
    
    def test_func(self):
        # Verifica se o usuário é o proprietário do animal ou é staff/funcionário
        animal = self.get_object()
        return (animal.proprietario == self.request.user or 
                self.request.user.is_staff or
                self.request.user.is_funcionario() or
                self.request.user.is_supervisor() or
                self.request.user.is_gerente())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_de_animais'] = TipoAnimal.objects.filter(ativo=True)
        context['titulo'] = f'Editar {self.object.nome}'
        context['botao'] = 'Salvar Alterações'
        return context
    
    def form_valid(self, form):
        messages.success(
            self.request,
            f"✅ O pet '{form.instance.nome}' foi atualizado com sucesso!"
        )
        return super().form_valid(form)


class AnimalDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Exclusão de animal (somente proprietário)"""
    model = Animal
    template_name = 'animal_confirm_delete.html'
    success_url = reverse_lazy('animal_list')
    
    def test_func(self):
        animal = self.get_object()
        return animal.proprietario == self.request.user
    
    def delete(self, request, *args, **kwargs):
        animal = self.get_object()
        messages.success(request, f"🗑️ O pet '{animal.nome}' foi removido.")
        return super().delete(request, *args, **kwargs)


# ====================================
# Views de tipo de animal
# ====================================

class TipoAnimalListView(LoginRequiredMixin, ListView):
    """Lista todos os tipos de animais"""
    model = TipoAnimal
    template_name = 'tipoanimal_list.html'
    context_object_name = 'tipos'
    
    def get_queryset(self):
        return TipoAnimal.objects.filter(ativo=True)


class TipoAnimalCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Criação de tipo de animal (somente staff/admin)"""
    model = TipoAnimal
    fields = ['nome', 'icone']
    template_name = 'tipoanimal_form.html'
    success_url = reverse_lazy('tipoanimal_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, f"✅ Tipo '{form.instance.nome}' criado com sucesso!")
        return super().form_valid(form)


# ====================================
# Views de Raça
# ====================================

class RacaListView(LoginRequiredMixin, ListView):
    """Lista todas as raças"""
    model = Raca
    template_name = 'raca_list.html'
    context_object_name = 'racas'
    
    def get_queryset(self):
        return Raca.objects.filter(ativo=True).select_related('tipo_animal')


class RacaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Criação de raça (somente staff/admin)"""
    model = Raca
    fields = ['tipo_animal', 'nome', 'observacoes_manejo']
    template_name = 'raca_form.html'
    success_url = reverse_lazy('raca_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_de_animais'] = TipoAnimal.objects.filter(ativo=True)
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f"✅ Raça '{form.instance.nome}' criada com sucesso!")
        return super().form_valid(form)


# ====================================
# API PARA BUSCAR RAÇAS DINAMICAMENTE
# ====================================

@login_required
def get_racas_by_tipo(request):
    """
    API endpoint para buscar raças de um tipo específico
    Usado no JavaScript do formulário de cadastro de animais
    """
    tipo_animal_id = request.GET.get('tipo_id')
    if not tipo_animal_id:
        return JsonResponse({'error': 'tipo_id não fornecido'}, status=400)
    
    racas = Raca.objects.filter(
        tipo_animal_id=tipo_animal_id,
        ativo=True
    ).order_by('nome').values('id', 'nome')
    
    return JsonResponse(list(racas), safe=False)
