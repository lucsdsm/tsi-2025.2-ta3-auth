"""
Dashboard principal do painel administrativo
Exibe estatísticas gerais e links para os demais painéis
"""

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from users.models import User
from pets.models import Animal, TipoAnimal, Raca


class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Dashboard principal do painel administrativo
    Apenas usuários staff/admin podem acessar
    """
    template_name = 'dashboard.html'
    
    def test_func(self):
        """Verifica se o usuário é staff"""
        return self.request.user.is_staff
    
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
