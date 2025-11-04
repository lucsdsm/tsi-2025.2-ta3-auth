"""
Views do painel administrativo
Organizadas em módulos separados por funcionalidade
"""

from .dashboard import DashboardView
from .usuarios import UsuarioListView, UsuarioCreateView, UsuarioUpdateView, UsuarioToggleStatusView
from .tipos_animais import TipoAnimalAdminListView, TipoAnimalAdminCreateView, TipoAnimalAdminUpdateView, TipoAnimalAdminDeleteView
from .racas import RacaAdminListView, RacaAdminCreateView, RacaAdminUpdateView, RacaAdminDeleteView
from .pets import PetAdminListView

__all__ = [
    'DashboardView',
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
]
