"""
Views do sistema de consultas veterinárias
"""

from .dashboard import DashboardVetView
from .consultas import (
    ConsultaListView,
    ConsultaCreateView,
    ConsultaUpdateView,
    ConsultaDetailView,
    ConsultaCancelarView,
    ConsultaIniciarAtendimentoView,
)
from .prontuarios import (
    ProntuarioCreateView,
    ProntuarioUpdateView,
    ProntuarioDetailView,
)
from .receitas import (
    ReceitaCreateView,
    ReceitaUpdateView,
    ReceitaDeleteView,
)

__all__ = [
    'DashboardVetView',
    'ConsultaListView',
    'ConsultaCreateView',
    'ConsultaUpdateView',
    'ConsultaDetailView',
    'ConsultaCancelarView',
    'ConsultaIniciarAtendimentoView',
    'ProntuarioCreateView',
    'ProntuarioUpdateView',
    'ProntuarioDetailView',
    'ReceitaCreateView',
    'ReceitaUpdateView',
    'ReceitaDeleteView',
]
