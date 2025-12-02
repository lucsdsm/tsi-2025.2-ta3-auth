"""
Views para edição/complemento de dados do cliente
"""

from django.views.generic import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from users.models import User
from pets.models import Animal
from panel.forms_complemento import ClienteComplementoForm, PetCadastroRapidoForm


class ClienteEditarView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View para funcionário complementar/editar dados do cliente
    """
    model = User
    form_class = ClienteComplementoForm
    template_name = 'clientes/editar.html'
    login_url = 'local_login'
    
    def test_func(self):
        """Apenas funcionários e staff podem acessar"""
        user = self.request.user
        return (user.is_staff or 
                user.is_funcionario() or
                user.is_supervisor() or
                user.is_gerente())
    
    def get_success_url(self):
        return reverse_lazy('panel:clientes_list')
    
    def form_valid(self, form):
        """Salva os dados complementares"""
        messages.success(
            self.request,
            f"✅ Dados de {form.instance.get_full_name()} atualizados com sucesso!"
        )
        return super().form_valid(form)


class ClienteAdicionarPetView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    View para funcionário adicionar pet a um cliente existente
    """
    model = Animal
    form_class = PetCadastroRapidoForm
    template_name = 'clientes/adicionar_pet.html'
    login_url = 'local_login'
    
    def test_func(self):
        """Apenas funcionários e staff podem acessar"""
        user = self.request.user
        return (user.is_staff or 
                user.is_funcionario() or
                user.is_supervisor() or
                user.is_gerente())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cliente'] = get_object_or_404(User, pk=self.kwargs['cliente_id'])
        return context
    
    def form_valid(self, form):
        """Associa o pet ao cliente"""
        form.instance.proprietario = get_object_or_404(User, pk=self.kwargs['cliente_id'])
        form.instance.ativo = True
        
        messages.success(
            self.request,
            f"✅ Pet '{form.instance.nome}' cadastrado com sucesso para {form.instance.proprietario.get_full_name()}!"
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('panel:clientes_list')
