from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    # Tipos de usuário
    ADMIN = 'ADMIN'
    CLIENTE = 'CLIENTE'
    FUNCIONARIO = 'FUNCIONARIO'
    VETERINARIO = 'VETERINARIO'
    
    USER_TYPE_CHOICES = [
        (ADMIN, 'Administrador'),
        (CLIENTE, 'Cliente'),
        (FUNCIONARIO, 'Funcionário'),
        (VETERINARIO, 'Veterinário'),
    ]
    
    email = models.EmailField(unique=True)
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default=CLIENTE,
        verbose_name='Tipo de Usuário'
    )
    
    # Campos adicionais para veterinários
    crmv = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='CRMV',
        help_text='Número do Conselho Regional de Medicina Veterinária'
    )
    especialidade = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Especialidade'
    )
    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Telefone'
    )

    def __str__(self):
        return self.username
    
    def is_veterinario(self):
        """Verifica se o usuário é veterinário"""
        return self.user_type == self.VETERINARIO
    
    def is_funcionario(self):
        """Verifica se o usuário é funcionário"""
        return self.user_type == self.FUNCIONARIO
    
    def is_cliente(self):
        """Verifica se o usuário é cliente"""
        return self.user_type == self.CLIENTE
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'