"""
Dashboard principal do painel administrativo
Exibe estatísticas gerais e links para os demais painéis
"""

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.utils import timezone
from users.models import User
from pets.models import Animal, TipoAnimal, Raca


class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Dashboard principal do painel administrativo
    Apenas usuários staff/admin podem acessar
    """
    template_name = 'dashboard.html'
    login_url = 'local_login'
    
    def test_func(self):
        """Verifica se o usuário é staff"""
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        """Redireciona para home se não tiver permissão"""
        from django.shortcuts import redirect
        from django.contrib import messages
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Você não tem permissão para acessar o painel administrativo.')
            return redirect('home')
        return redirect('local_login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estatísticas de usuários
        context['total_usuarios'] = User.objects.count()
        context['usuarios_ativos'] = User.objects.filter(is_active=True).count()
        context['usuarios_staff'] = User.objects.filter(is_staff=True).count()
        
        # Estatísticas de pets
        context['total_pets'] = Animal.objects.filter(ativo=True).count()
        context['total_tipos_animais'] = TipoAnimal.objects.filter(ativo=True).count()
        context['total_racas'] = Raca.objects.filter(ativo=True).count()
        
        # Distribuição de pets por tipo
        context['pets_por_tipo'] = Animal.objects.filter(ativo=True).values(
            'tipo_animal__nome'
        ).annotate(
            total=Count('id')
        ).order_by('-total')
        
        # Últimos usuários cadastrados
        context['ultimos_usuarios'] = User.objects.order_by('-date_joined')[:5]
        
        # Últimos pets cadastrados
        context['ultimos_pets'] = Animal.objects.filter(ativo=True).select_related(
            'proprietario', 'tipo_animal', 'raca'
        ).order_by('-criado_em')[:5]
        
        return context


class DashboardFuncView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Dashboard do painel de funcionário
    Funcionários, supervisores e gerentes podem acessar
    """
    template_name = 'dashboard_funcionario.html'
    login_url = 'local_login'
    
    def test_func(self):
        """Verifica se o usuário é funcionário, supervisor ou gerente"""
        user = self.request.user
        return user.is_funcionario() or user.is_supervisor() or user.is_gerente()
    
    def handle_no_permission(self):
        """Redireciona para home se não tiver permissão"""
        from django.shortcuts import redirect
        from django.contrib import messages
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Você não tem permissão para acessar o painel de funcionário.')
            return redirect('home')
        return redirect('local_login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estatísticas de clientes e pets
        context['total_clientes'] = User.objects.filter(user_type=User.CLIENTE, is_active=True).count()
        context['total_pets'] = Animal.objects.filter(ativo=True).count()
        context['total_tipos_animais'] = TipoAnimal.objects.filter(ativo=True).count()
        context['total_racas'] = Raca.objects.filter(ativo=True).count()
        
        # Produtos disponíveis (importar modelo somente se existir)
        try:
            from produtos.models import Produto
            context['total_produtos'] = Produto.objects.filter(estoque__gt=0).count()
            context['produtos_destaque'] = Produto.objects.filter(
                estoque__gt=0
            ).order_by('-produto_id')[:5]
        except ImportError:
            context['total_produtos'] = 0
            context['produtos_destaque'] = []
        
        # Últimos clientes cadastrados
        context['ultimos_clientes'] = User.objects.filter(
            user_type=User.CLIENTE
        ).order_by('-date_joined')[:5]
        
        # Últimos pets cadastrados
        context['ultimos_pets'] = Animal.objects.filter(ativo=True).select_related(
            'proprietario', 'tipo_animal', 'raca'
        ).order_by('-criado_em')[:5]
        
        return context
