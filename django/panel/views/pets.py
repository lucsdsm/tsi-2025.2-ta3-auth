"""
Views para visualização de pets cadastrados
Painel administrativo para ver todos os pets do sistema
"""

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from pets.models import Animal, TipoAnimal


class PetAdminListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Lista todos os pets cadastrados no sistema"""
    model = Animal
    template_name = 'pets/list.html'
    context_object_name = 'pets'
    paginate_by = 20
    
    def test_func(self):
        """Permite acesso para staff e funcionários"""
        user = self.request.user
        return (user.is_staff or 
                user.is_funcionario() or
                user.is_supervisor() or
                user.is_gerente())
    
    def get_queryset(self):
        queryset = Animal.objects.select_related(
            'proprietario', 'tipo_animal', 'raca'
        ).order_by('-criado_em')
        
        # Filtro por status
        status = self.request.GET.get('status', '')
        if status == 'ativo':
            queryset = queryset.filter(ativo=True)
        elif status == 'inativo':
            queryset = queryset.filter(ativo=False)
        
        # Filtro por tipo de animal
        tipo_id = self.request.GET.get('tipo', '')
        if tipo_id:
            queryset = queryset.filter(tipo_animal_id=tipo_id)
        
        # Busca por nome do pet ou proprietário
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) |
                Q(proprietario__username__icontains=search) |
                Q(proprietario__email__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_animais'] = TipoAnimal.objects.filter(ativo=True).order_by('nome')
        context['status_filter'] = self.request.GET.get('status', '')
        context['tipo_filter'] = self.request.GET.get('tipo', '')
        context['search'] = self.request.GET.get('search', '')
        return context
