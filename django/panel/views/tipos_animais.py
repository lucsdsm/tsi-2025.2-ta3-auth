"""
Views para gerenciamento de tipos de animais
CRUD completo para administradores
"""

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from pets.models import TipoAnimal, Raca, Animal


class TipoAnimalAdminListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Lista todos os tipos de animais"""
    model = TipoAnimal
    template_name = 'tipos_animais/list.html'
    context_object_name = 'tipos'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_queryset(self):
        return TipoAnimal.objects.all().order_by('nome')


class TipoAnimalAdminCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Criação de novo tipo de animal"""
    model = TipoAnimal
    template_name = 'tipos_animais/form.html'
    fields = ['nome', 'icone', 'ativo']
    success_url = reverse_lazy('panel:tipos_animais_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Cadastrar Tipo de Animal'
        context['botao'] = 'Cadastrar'
        return context
    
    def form_valid(self, form):
        messages.success(
            self.request,
            f"✅ Tipo de animal '{form.instance.nome}' criado com sucesso!"
        )
        return super().form_valid(form)


class TipoAnimalAdminUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edição de tipo de animal existente"""
    model = TipoAnimal
    template_name = 'tipos_animais/form.html'
    fields = ['nome', 'icone', 'ativo']
    success_url = reverse_lazy('panel:tipos_animais_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar {self.object.nome}'
        context['botao'] = 'Salvar Alterações'
        return context
    
    def form_valid(self, form):
        messages.success(
            self.request,
            f"✅ Tipo de animal '{form.instance.nome}' atualizado com sucesso!"
        )
        return super().form_valid(form)


class TipoAnimalAdminDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Exclusão de tipo de animal"""
    model = TipoAnimal
    template_name = 'tipos_animais/confirm_delete.html'
    success_url = reverse_lazy('panel:tipos_animais_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Contar quantas raças estão vinculadas a este tipo
        context['racas_count'] = Raca.objects.filter(tipo_animal=self.object).count()
        # Contar quantos animais estão vinculados a este tipo
        context['animais_count'] = Animal.objects.filter(tipo_animal=self.object).count()
        return context
    
    def delete(self, request, *args, **kwargs):
        tipo = self.get_object()
        
        # Verificar se existem raças vinculadas
        racas_count = Raca.objects.filter(tipo_animal=tipo).count()
        if racas_count > 0:
            messages.error(
                request,
                f"❌ Não é possível excluir o tipo '{tipo.nome}' pois existem {racas_count} raça(s) vinculada(s) a ele. "
                f"Exclua ou reatribua as raças primeiro."
            )
            return redirect('panel:tipos_animais_list')
        
        # Verificar se existem animais vinculados
        animais_count = Animal.objects.filter(tipo_animal=tipo).count()
        if animais_count > 0:
            messages.error(
                request,
                f"❌ Não é possível excluir o tipo '{tipo.nome}' pois existem {animais_count} animal(is) cadastrado(s) com este tipo. "
                f"Exclua ou reatribua os animais primeiro."
            )
            return redirect('panel:tipos_animais_list')
        
        messages.success(request, f"🗑️ Tipo de animal '{tipo.nome}' removido com sucesso!")
        return super().delete(request, *args, **kwargs)
