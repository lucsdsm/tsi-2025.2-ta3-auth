"""
Views para cadastro de clientes pelo funcionário
"""

from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from panel.forms import ClienteComPetForm


class ClienteCadastroFuncView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    """
    View para funcionário cadastrar cliente com pet
    """
    template_name = 'clientes/cadastro.html'
    form_class = ClienteComPetForm
    success_url = reverse_lazy('panel:clientes_list')
    login_url = 'local_login'
    
    def test_func(self):
        """Apenas funcionários e staff podem acessar"""
        user = self.request.user
        return (user.is_staff or 
                user.is_funcionario() or
                user.is_supervisor() or
                user.is_gerente())
    
    def form_valid(self, form):
        """Salva o cliente e o pet"""
        user, pet = form.save()
        
        messages.success(
            self.request,
            f"✅ Cliente {user.get_full_name()} cadastrado com sucesso! "
            f"Pet '{pet.nome}' também foi registrado. "
            f"Senha de acesso: Pet@{form.cleaned_data['cpf'][:6]}"
        )
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Exibe erros do formulário"""
        messages.error(
            self.request,
            "❌ Erro ao cadastrar cliente. Verifique os campos e tente novamente."
        )
        return super().form_invalid(form)
