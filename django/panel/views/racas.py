"""
Views para gerenciamento de raças
CRUD completo para administradores
"""

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from pets.models import Raca, TipoAnimal, Animal


class RacaAdminListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Lista todas as raças com filtro por tipo"""
    model = Raca
    template_name = 'racas/list.html'
    context_object_name = 'racas'
    paginate_by = 20
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_queryset(self):
        queryset = Raca.objects.select_related('tipo_animal').order_by('tipo_animal__nome', 'nome')
        
        # Filtro por tipo de animal
        tipo_id = self.request.GET.get('tipo', '')
        if tipo_id:
            queryset = queryset.filter(tipo_animal_id=tipo_id)
        
        # Busca por nome
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) | Q(tipo_animal__nome__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_animais'] = TipoAnimal.objects.filter(ativo=True).order_by('nome')
        context['tipo_filter'] = self.request.GET.get('tipo', '')
        context['search'] = self.request.GET.get('search', '')
        return context


class RacaAdminCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Criação de nova raça"""
    model = Raca
    template_name = 'racas/form.html'
    fields = ['tipo_animal', 'nome', 'observacoes_manejo', 'ativo']
    success_url = reverse_lazy('panel:racas_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_animais'] = TipoAnimal.objects.filter(ativo=True).order_by('nome')
        context['titulo'] = 'Cadastrar Raça'
        context['botao'] = 'Cadastrar'
        return context
    
    def form_valid(self, form):
        messages.success(
            self.request,
            f"✅ Raça '{form.instance.nome}' criada com sucesso!"
        )
        return super().form_valid(form)


class RacaAdminUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edição de raça existente"""
    model = Raca
    template_name = 'racas/form.html'
    fields = ['tipo_animal', 'nome', 'observacoes_manejo', 'ativo']
    success_url = reverse_lazy('panel:racas_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_animais'] = TipoAnimal.objects.filter(ativo=True).order_by('nome')
        context['titulo'] = f'Editar {self.object.nome}'
        context['botao'] = 'Salvar Alterações'
        return context
    
    def form_valid(self, form):
        messages.success(
            self.request,
            f"✅ Raça '{form.instance.nome}' atualizada com sucesso!"
        )
        return super().form_valid(form)


class RacaAdminDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Exclusão de raça"""
    model = Raca
    template_name = 'racas/confirm_delete.html'
    success_url = reverse_lazy('panel:racas_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Contar quantos animais estão vinculados a esta raça
        context['animais_count'] = Animal.objects.filter(raca=self.object).count()
        return context
    
    def delete(self, request, *args, **kwargs):
        raca = self.get_object()
        
        # Verificar se existem animais vinculados a esta raça
        animais_count = Animal.objects.filter(raca=raca).count()
        if animais_count > 0:
            messages.error(
                request,
                f"❌ Não é possível excluir a raça '{raca.nome}' pois existem {animais_count} animal(is) cadastrado(s) com esta raça. "
                f"Exclua ou reatribua os animais primeiro."
            )
            return redirect('panel:racas_list')
        
        messages.success(request, f"🗑️ Raça '{raca.nome}' removida com sucesso!")
        return super().delete(request, *args, **kwargs)
