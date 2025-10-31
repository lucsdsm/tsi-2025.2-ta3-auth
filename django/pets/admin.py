"""
Configuração do Django Admin para o app management
"""

from django.contrib import admin
from .models import TipoAnimal, Raca, Animal


@admin.register(TipoAnimal)
class TipoAnimalAdmin(admin.ModelAdmin):
    list_display = ['nome', 'icone', 'ativo', 'criado_em']
    list_filter = ['ativo']
    search_fields = ['nome']
    list_editable = ['ativo']


@admin.register(Raca)
class RacaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo_animal', 'ativo', 'criado_em']
    list_filter = ['tipo_animal', 'ativo']
    search_fields = ['nome', 'tipo_animal__nome']
    list_editable = ['ativo']


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['nome', 'proprietario', 'tipo_animal', 'raca', 'sexo', 'data_nascimento', 'ativo']
    list_filter = ['tipo_animal', 'sexo', 'ativo']
    search_fields = ['nome', 'proprietario__username', 'proprietario__email']
    list_editable = ['ativo']
    readonly_fields = ['criado_em', 'atualizado_em']
    
    fieldsets = (
        ('Informações do Proprietário', {
            'fields': ('proprietario',)
        }),
        ('Dados do Animal', {
            'fields': ('nome', 'tipo_animal', 'raca', 'sexo', 'data_nascimento', 'foto')
        }),
        ('Observações', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        }),
        ('Controle', {
            'fields': ('ativo', 'criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
