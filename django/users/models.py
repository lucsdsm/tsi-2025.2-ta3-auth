from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    # Tipos de usuário
    ADMIN = 'ADMIN'
    CLIENTE = 'CLIENTE'
    FUNCIONARIO = 'FUNCIONARIO'
    SUPERVISOR = 'SUPERVISOR'
    GERENTE = 'GERENTE'
    VETERINARIO = 'VETERINARIO'
    
    USER_TYPE_CHOICES = [
        (ADMIN, 'Administrador'),
        (CLIENTE, 'Cliente'),
        (FUNCIONARIO, 'Funcionário'),
        (SUPERVISOR, 'Supervisor'),
        (GERENTE, 'Gerente'),
        (VETERINARIO, 'Veterinário'),
    ]
    
    # Prefixos de matrícula por tipo de funcionário
    MATRICULA_PREFIXES = {
        VETERINARIO: '10',
        GERENTE: '15',
        SUPERVISOR: '20',
        FUNCIONARIO: '25',
    }
    
    email = models.EmailField(unique=True)
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default=CLIENTE,
        verbose_name='Tipo de Usuário'
    )
    
    matricula = models.CharField(
        max_length=6,
        unique=True,
        blank=True,
        null=True,
        verbose_name='Matrícula',
        help_text='Matrícula do funcionário (6 dígitos com prefixo: 10-Vet, 15-Gerente, 20-Supervisor, 25-Func)'
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
        if self.matricula:
            return f"{self.get_full_name() or self.username} ({self.matricula})"
        return self.get_full_name() or self.username
    
    def is_veterinario(self):
        """Verifica se o usuário é veterinário"""
        return self.user_type == self.VETERINARIO
    
    def is_funcionario(self):
        """Verifica se o usuário é funcionário"""
        return self.user_type == self.FUNCIONARIO
    
    def is_supervisor(self):
        """Verifica se o usuário é supervisor"""
        return self.user_type == self.SUPERVISOR
    
    def is_gerente(self):
        """Verifica se o usuário é gerente"""
        return self.user_type == self.GERENTE
    
    def is_cliente(self):
        """Verifica se o usuário é cliente"""
        return self.user_type == self.CLIENTE
    
    def is_staff_member(self):
        """Verifica se o usuário é membro da equipe (funcionário, supervisor, gerente ou veterinário)"""
        return self.user_type in [self.FUNCIONARIO, self.SUPERVISOR, self.GERENTE, self.VETERINARIO]
    
    @staticmethod
    def gerar_senha_padrao(matricula):
        """Gera senha padrão baseada na matrícula: Pet@{matricula}"""
        return f"Pet@{matricula}"
    
    @classmethod
    def validar_matricula(cls, matricula, user_type):
        """Valida se a matrícula está no formato correto para o tipo de usuário"""
        if user_type not in cls.MATRICULA_PREFIXES:
            return False, "Tipo de usuário não requer matrícula"
        
        if not matricula or len(matricula) != 6:
            return False, "Matrícula deve ter exatamente 6 dígitos"
        
        if not matricula.isdigit():
            return False, "Matrícula deve conter apenas números"
        
        prefixo_esperado = cls.MATRICULA_PREFIXES[user_type]
        if not matricula.startswith(prefixo_esperado):
            tipo_nome = dict(cls.USER_TYPE_CHOICES)[user_type]
            return False, f"Matrícula de {tipo_nome} deve começar com {prefixo_esperado}"
        
        return True, "Matrícula válida"
    
    def delete(self, *args, **kwargs):
        """Impede exclusão se houver consultas relacionadas"""
        from django.core.exceptions import ValidationError
        
        # Verifica se é veterinário com consultas
        if self.is_veterinario():
            consultas_ativas = self.consultas_veterinario.exclude(status='CANCELADA').count()
            if consultas_ativas > 0:
                raise ValidationError(
                    f"Não é possível excluir este veterinário pois há {consultas_ativas} consulta(s) relacionada(s). "
                    "Cancele as consultas antes de excluir o veterinário."
                )
        
        super().delete(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'