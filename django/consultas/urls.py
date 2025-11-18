"""
URLs do app de consultas veterinárias
"""

from django.urls import path
from .views import (
    DashboardVetView,
    ConsultaListView,
    ConsultaCreateView,
    ConsultaUpdateView,
    ConsultaDetailView,
    ConsultaCancelarView,
    ConsultaIniciarAtendimentoView,
    ProntuarioCreateView,
    ProntuarioUpdateView,
    ProntuarioDetailView,
    ReceitaCreateView,
    ReceitaUpdateView,
    ReceitaDeleteView,
)

app_name = 'consultas'

urlpatterns = [
    # Dashboard
    path('', DashboardVetView.as_view(), name='dashboard'),
    
    # Consultas
    path('consultas/', ConsultaListView.as_view(), name='consulta_list'),
    path('consultas/nova/', ConsultaCreateView.as_view(), name='consulta_create'),
    path('consultas/<int:pk>/', ConsultaDetailView.as_view(), name='consulta_detail'),
    path('consultas/<int:pk>/editar/', ConsultaUpdateView.as_view(), name='consulta_update'),
    path('consultas/<int:pk>/cancelar/', ConsultaCancelarView.as_view(), name='consulta_cancelar'),
    path('consultas/<int:pk>/iniciar/', ConsultaIniciarAtendimentoView.as_view(), name='consulta_iniciar'),
    
    # Prontuários
    path('consultas/<int:consulta_pk>/prontuario/criar/', ProntuarioCreateView.as_view(), name='prontuario_create'),
    path('prontuarios/<int:pk>/editar/', ProntuarioUpdateView.as_view(), name='prontuario_update'),
    path('prontuarios/<int:pk>/', ProntuarioDetailView.as_view(), name='prontuario_detail'),
    
    # Receitas
    path('prontuarios/<int:prontuario_pk>/receitas/nova/', ReceitaCreateView.as_view(), name='receita_create'),
    path('receitas/<int:pk>/editar/', ReceitaUpdateView.as_view(), name='receita_update'),
    path('receitas/<int:pk>/excluir/', ReceitaDeleteView.as_view(), name='receita_delete'),
]
