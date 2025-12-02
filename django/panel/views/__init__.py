"""
Views do painel administrativo
Organizadas em módulos separados por funcionalidade
"""

from .dashboard import DashboardView, DashboardFuncView
from .usuarios import UsuarioListView, UsuarioCreateView, UsuarioUpdateView, UsuarioToggleStatusView
from .tipos_animais import TipoAnimalAdminListView, TipoAnimalAdminCreateView, TipoAnimalAdminUpdateView, TipoAnimalAdminDeleteView
from .racas import RacaAdminListView, RacaAdminCreateView, RacaAdminUpdateView, RacaAdminDeleteView
from .pets import PetAdminListView
from .clientes import ClienteListView
from .cliente_cadastro import ClienteCadastroFuncView
from .cliente_edicao import ClienteEditarView, ClienteAdicionarPetView

__all__ = [
    'DashboardView',
    'DashboardFuncView',
    'UsuarioListView',
    'UsuarioCreateView', 
    'UsuarioUpdateView',
    'UsuarioToggleStatusView',
    'TipoAnimalAdminListView',
    'TipoAnimalAdminCreateView',
    'TipoAnimalAdminUpdateView',
    'TipoAnimalAdminDeleteView',
    'RacaAdminListView',
    'RacaAdminCreateView',
    'RacaAdminUpdateView',
    'RacaAdminDeleteView',
    'PetAdminListView',
    'ClienteListView',
    'ClienteCadastroFuncView',
    'ClienteEditarView',
    'ClienteAdicionarPetView',
]

