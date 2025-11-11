from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Campos exibidos na lista de usuários
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active']
    list_filter = ['user_type', 'is_staff', 'is_active', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'crmv']
    
    # Organização dos campos no formulário de edição
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informações de Tipo', {
            'fields': ('user_type',)
        }),
        ('Informações de Contato', {
            'fields': ('telefone',)
        }),
        ('Informações Veterinárias', {
            'fields': ('crmv', 'especialidade'),
            'classes': ('collapse',),
            'description': 'Campos específicos para veterinários'
        }),
    )
    
    # Campos ao adicionar novo usuário
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': ('email', 'first_name', 'last_name', 'user_type', 'telefone', 'crmv', 'especialidade')
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        """Personaliza o formulário baseado no tipo de usuário"""
        form = super().get_form(request, obj, **kwargs)
        return form

