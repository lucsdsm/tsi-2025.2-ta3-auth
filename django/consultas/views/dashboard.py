"""
Dashboard do painel veterinário
Exibe estatísticas e resumo das consultas
"""

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from datetime import timedelta
from consultas.models import Consulta, Prontuario


@method_decorator(ensure_csrf_cookie, name='dispatch')
class DashboardVetView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Dashboard principal do painel veterinário
    Apenas veterinários podem acessar
    """
    template_name = 'consultas/dashboard.html'
    login_url = 'local_login'
    
    def test_func(self):
        """Verifica se o usuário é veterinário"""
        return self.request.user.is_veterinario()
    
    def handle_no_permission(self):
        """Redireciona para home se não tiver permissão"""
        from django.shortcuts import redirect
        from django.contrib import messages
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Você não tem permissão para acessar o painel veterinário.')
            return redirect('home')
        return redirect('local_login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        veterinario = self.request.user
        hoje = timezone.now().date()
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        fim_semana = inicio_semana + timedelta(days=6)
        
        # Consultas do veterinário
        consultas_vet = Consulta.objects.filter(veterinario=veterinario)
        
        # Estatísticas gerais
        context['total_consultas'] = consultas_vet.count()
        context['consultas_hoje'] = consultas_vet.filter(
            data_hora__date=hoje
        ).count()
        context['consultas_semana'] = consultas_vet.filter(
            data_hora__date__gte=inicio_semana,
            data_hora__date__lte=fim_semana
        ).count()
        
        # Consultas por status
        context['consultas_agendadas'] = consultas_vet.filter(
            status='AGENDADA'
        ).count()
        context['consultas_confirmadas'] = consultas_vet.filter(
            status='CONFIRMADA'
        ).count()
        context['consultas_realizadas'] = consultas_vet.filter(
            status='REALIZADA'
        ).count()
        
        # Próximas consultas (próximos 7 dias)
        proximo_periodo = hoje + timedelta(days=7)
        context['proximas_consultas'] = consultas_vet.filter(
            data_hora__date__gte=hoje,
            data_hora__date__lte=proximo_periodo,
            status__in=['AGENDADA', 'CONFIRMADA']
        ).select_related(
            'animal', 'animal__proprietario', 'animal__raca', 'animal__tipo_animal'
        ).order_by('data_hora')[:10]
        
        # Consultas de hoje
        context['consultas_hoje_list'] = consultas_vet.filter(
            data_hora__date=hoje
        ).select_related(
            'animal', 'animal__proprietario', 'animal__raca', 'animal__tipo_animal'
        ).order_by('data_hora')
        
        # Últimas consultas realizadas
        context['ultimas_realizadas'] = consultas_vet.filter(
            status='REALIZADA'
        ).select_related(
            'animal', 'animal__proprietario'
        ).order_by('-data_hora')[:5]
        
        # Estatísticas de atendimento
        context['total_prontuarios'] = Prontuario.objects.filter(
            consulta__veterinario=veterinario
        ).count()
        
        return context
