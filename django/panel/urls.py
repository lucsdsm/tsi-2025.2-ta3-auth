"""
URLs do painel administrativo
Rotas organizadas por funcionalidade
"""

from django.urls import path
from .views import (
    DashboardView,
    UsuarioListView, UsuarioCreateView, UsuarioUpdateView, UsuarioToggleStatusView,
    TipoAnimalAdminListView, TipoAnimalAdminCreateView, TipoAnimalAdminUpdateView, TipoAnimalAdminDeleteView,
    RacaAdminListView, RacaAdminCreateView, RacaAdminUpdateView, RacaAdminDeleteView,
    PetAdminListView,
    ClienteListView,
    ClienteCadastroFuncView,
    ClienteEditarView,
    ClienteAdicionarPetView,
)

app_name = 'panel'

urlpatterns = [
    # Dashboard principal
    path('', DashboardView.as_view(), name='dashboard'),
    
    # Gerenciamento de usuários
    path('usuarios/', UsuarioListView.as_view(), name='usuarios_list'),
    path('usuarios/novo/', UsuarioCreateView.as_view(), name='usuarios_create'),
    path('usuarios/<int:pk>/editar/', UsuarioUpdateView.as_view(), name='usuarios_update'),
    path('usuarios/<int:pk>/toggle-status/', UsuarioToggleStatusView.as_view(), name='usuarios_toggle_status'),
    
    # Gerenciamento de clientes (funcionários)
    path('clientes/', ClienteListView.as_view(), name='clientes_list'),
    path('clientes/cadastrar/', ClienteCadastroFuncView.as_view(), name='clientes_cadastrar'),
    path('clientes/<int:pk>/editar/', ClienteEditarView.as_view(), name='clientes_editar'),
    path('clientes/<int:cliente_id>/adicionar-pet/', ClienteAdicionarPetView.as_view(), name='clientes_adicionar_pet'),
    
    # Gerenciamento de tipos de animais
    path('tipos-animais/', TipoAnimalAdminListView.as_view(), name='tipos_animais_list'),
    path('tipos-animais/novo/', TipoAnimalAdminCreateView.as_view(), name='tipos_animais_create'),
    path('tipos-animais/<int:pk>/editar/', TipoAnimalAdminUpdateView.as_view(), name='tipos_animais_update'),
    path('tipos-animais/<int:pk>/deletar/', TipoAnimalAdminDeleteView.as_view(), name='tipos_animais_delete'),
    
    # Gerenciamento de raças
    path('racas/', RacaAdminListView.as_view(), name='racas_list'),
    path('racas/novo/', RacaAdminCreateView.as_view(), name='racas_create'),
    path('racas/<int:pk>/editar/', RacaAdminUpdateView.as_view(), name='racas_update'),
    path('racas/<int:pk>/deletar/', RacaAdminDeleteView.as_view(), name='racas_delete'),
    
    # Visualização de pets
    path('pets/', PetAdminListView.as_view(), name='pets_list'),
]

