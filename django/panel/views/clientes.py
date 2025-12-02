"""
Views para gerenciamento de clientes no painel do funcionário
"""

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from users.models import User
from pets.models import Animal


class ClienteListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Lista todos os clientes com seus pets"""
    model = User
    template_name = 'clientes/list.html'
    context_object_name = 'clientes'
    paginate_by = 20
    login_url = 'local_login'
    
    def test_func(self):
        """Verifica se o usuário é funcionário ou staff"""
        user = self.request.user
        return (user.is_funcionario() or 
                user.is_supervisor() or 
                user.is_gerente() or 
                user.is_staff)
    
    def get_queryset(self):
        """Retorna todos os clientes (incluindo os que se cadastraram por conta própria)"""
        queryset = User.objects.filter(
            user_type=User.CLIENTE
        ).annotate(
            total_pets=Count('animais')
        ).order_by('-date_joined')
        
        # Filtro de busca
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(username__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Adiciona os pets de cada cliente
        for cliente in context['clientes']:
            cliente.pets = Animal.objects.filter(
                proprietario=cliente,
                ativo=True
            ).select_related('tipo_animal', 'raca')[:5]  # Limita a 5 pets por cliente
        
        context['total_clientes'] = User.objects.filter(
            user_type=User.CLIENTE
        ).count()
        
        return context
