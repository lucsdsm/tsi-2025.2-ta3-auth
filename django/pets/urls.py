"""
URLs para o app management
"""

from django.urls import path
from . import views

urlpatterns = [
    # URLs de Animal
    path('animais/', views.AnimalListView.as_view(), name='animal_list'),
    path('animais/novo/', views.AnimalCreateView.as_view(), name='animal_create'),
    path('animais/<int:pk>/editar/', views.AnimalUpdateView.as_view(), name='animal_update'),
    path('animais/<int:pk>/excluir/', views.AnimalDeleteView.as_view(), name='animal_delete'),
    
    # URLs de TipoAnimal
    path('tipos/', views.TipoAnimalListView.as_view(), name='tipoanimal_list'),
    path('tipos/novo/', views.TipoAnimalCreateView.as_view(), name='tipoanimal_create'),
    
    # URLs de Raça
    path('racas/', views.RacaListView.as_view(), name='raca_list'),
    path('racas/nova/', views.RacaCreateView.as_view(), name='raca_create'),
    
    # API para buscar raças por tipo
    path('api/racas-por-tipo/', views.get_racas_by_tipo, name='get_racas_by_tipo'),
]
