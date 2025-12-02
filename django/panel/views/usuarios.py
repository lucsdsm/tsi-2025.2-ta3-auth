"""
Views para gerenciamento de usuários
CRUD completo para administradores
"""

from django.views.generic import ListView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db.models import Q
from users.models import User
from users.forms import FuncionarioCreateForm


class UsuarioListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Lista todos os usuários do sistema com busca"""
    model = User
    template_name = 'usuarios/list.html'
    context_object_name = 'usuarios'
    paginate_by = 20
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_queryset(self):
        queryset = User.objects.all().order_by('-date_joined')
        
        # Busca por nome, email ou username
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(crmv__icontains=search)
            )
        
        # Filtro por status
        status = self.request.GET.get('status', '')
        if status == 'ativo':
            queryset = queryset.filter(is_active=True)
        elif status == 'inativo':
            queryset = queryset.filter(is_active=False)
        
        # Filtro por tipo de usuário
        user_type = self.request.GET.get('user_type', '')
        if user_type:
            queryset = queryset.filter(user_type=user_type)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        context['user_type_filter'] = self.request.GET.get('user_type', '')
        context['user_type_choices'] = User.USER_TYPE_CHOICES
        return context


class UsuarioCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Criação de novo funcionário pelo admin com sistema de matrícula"""
    model = User
    form_class = FuncionarioCreateForm
    template_name = 'usuarios/form.html'
    success_url = reverse_lazy('panel:usuarios_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        user = form.save()
        
        # Gera senha padrão
        senha_padrao = User.gerar_senha_padrao(user.matricula)
        
        messages.success(
            self.request,
            f"✅ Funcionário '{user.get_full_name()}' criado com sucesso!<br>"
            f"<strong>Matrícula:</strong> {user.matricula}<br>"
            f"<strong>Senha padrão:</strong> {senha_padrao}<br>"
            f"<em>Informe estes dados ao funcionário para o primeiro acesso.</em>"
        )
        return redirect(self.success_url)


class UsuarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edição de usuário existente"""
    model = User
    template_name = 'usuarios/form.html'
    fields = ['first_name', 'last_name', 'email', 'user_type', 'matricula', 'telefone', 'crmv', 'especialidade', 'is_active']
    success_url = reverse_lazy('panel:usuarios_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Adicionar classes CSS para melhorar apresentação
        for field_name, field in form.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        # Tornar matrícula readonly se já estiver definida
        if self.object.matricula:
            form.fields['matricula'].widget.attrs['readonly'] = True
            form.fields['matricula'].help_text = 'Matrícula não pode ser alterada após criação'
        
        return form
    
    def form_valid(self, form):
        # Validar matrícula se foi alterada
        if self.object.matricula and form.cleaned_data.get('matricula') != self.object.matricula:
            messages.error(self.request, "❌ Matrícula não pode ser alterada!")
            return self.form_invalid(form)
        
        messages.success(
            self.request,
            f"✅ Usuário '{form.instance.get_full_name() or form.instance.username}' atualizado com sucesso!"
        )
        return super().form_valid(form)


class UsuarioToggleStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Ativa/desativa usuário"""
    
    def test_func(self):
        return self.request.user.is_staff
    
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        
        # Não permitir desativar o próprio usuário
        if user == request.user:
            messages.error(request, "❌ Você não pode desativar sua própria conta!")
            return redirect('panel:usuarios_list')
        
        user.is_active = not user.is_active
        user.save()
        
        status = "ativado" if user.is_active else "desativado"
        messages.success(request, f"✅ Usuário '{user.username}' {status} com sucesso!")
        
        return redirect('panel:usuarios_list')
