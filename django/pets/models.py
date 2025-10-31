"""
Models para o sistema de gerenciamento de Pets

Hierarquia:
- TipoAnimal (Ex: Cachorro, Gato, Pássaro)
  └── Raca (Ex: Labrador, Persa, Canário)
      └── Animal (Pet individual com proprietário)

Relacionamentos:
- Um Animal pertence a UM proprietário (User) - ForeignKey
- Um User pode ter VÁRIOS animais - reverse relationship
- Uma Raça pertence a UM TipoAnimal
- Um Animal pertence a UMA Raça
"""

from django.db import models
from django.conf import settings


class TipoAnimal(models.Model):
    """
    Tipo/Espécie de animal (Cachorro, Gato, etc)
    """
    nome = models.CharField(
        max_length=50,
        unique=True,
        help_text="Nome do tipo de animal (ex: Cachorro, Gato, Pássaro)"
    )
    icone = models.CharField(
        max_length=50,
        blank=True,
        help_text="Emoji ou ícone representando o tipo (ex: 🐶, 🐱, 🐦)"
    )
    ativo = models.BooleanField(
        default=True,
        help_text="Define se este tipo está ativo no sistema"
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tipo de Animal"
        verbose_name_plural = "Tipos de Animais"
        ordering = ['nome']

    def __str__(self):
        return f"{self.icone} {self.nome}" if self.icone else self.nome


class Raca(models.Model):
    """
    Raça de um tipo específico de animal
    """
    tipo_animal = models.ForeignKey(
        TipoAnimal,
        on_delete=models.PROTECT,
        related_name='racas',
        help_text="Tipo de animal ao qual esta raça pertence"
    )
    nome = models.CharField(
        max_length=100,
        help_text="Nome da raça (ex: Labrador, Persa, Canário)"
    )
    observacoes_manejo = models.TextField(
        blank=True,
        help_text="Observações sobre cuidados e manejo específicos desta raça"
    )
    ativo = models.BooleanField(
        default=True,
        help_text="Define se esta raça está ativa no sistema"
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Raça"
        verbose_name_plural = "Raças"
        ordering = ['tipo_animal', 'nome']
        unique_together = ['tipo_animal', 'nome']  # Evita raça duplicada para mesmo tipo

    def __str__(self):
        return f"{self.nome} ({self.tipo_animal.nome})"


class Animal(models.Model):
    """
    Animal (Pet) individual com proprietário
    
    Relacionamento: Cada animal pertence a UM usuário
    """
    SEXO_CHOICES = [
        ('M', 'Macho'),
        ('F', 'Fêmea'),
        ('I', 'Indefinido'),
    ]

    # Relacionamento com o usuário proprietário
    proprietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='animais',
        help_text="Usuário proprietário do animal"
    )
    
    # Dados do animal
    nome = models.CharField(
        max_length=100,
        help_text="Nome do pet"
    )
    tipo_animal = models.ForeignKey(
        TipoAnimal,
        on_delete=models.PROTECT,
        related_name='animais',
        help_text="Tipo do animal"
    )
    raca = models.ForeignKey(
        Raca,
        on_delete=models.PROTECT,
        related_name='animais',
        help_text="Raça do animal"
    )
    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        default='I',
        help_text="Sexo do animal"
    )
    data_nascimento = models.DateField(
        null=True,
        blank=True,
        help_text="Data de nascimento do animal"
    )
    
    # Campos de controle
    ativo = models.BooleanField(
        default=True,
        help_text="Define se este animal está ativo no sistema"
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    # Campos opcionais adicionais
    observacoes = models.TextField(
        blank=True,
        help_text="Observações gerais sobre o animal"
    )
    # foto = models.ImageField(
    #     upload_to='animais/',
    #     blank=True,
    #     null=True,
    #     help_text="Foto do animal"
    # )

    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animais"
        ordering = ['-criado_em']  # Mais recentes primeiro
        # Um usuário não pode ter dois animais com o mesmo nome
        unique_together = ['proprietario', 'nome']

    def __str__(self):
        return f"{self.nome} ({self.raca.nome}) - {self.proprietario.username}"
    
    @property
    def idade_anos(self):
        from datetime import date

        if self.data_nascimento:
            hoje = date.today()
            return (
                hoje.year
                - self.data_nascimento.year
                - (
                    (hoje.month, hoje.day)
                    < (self.data_nascimento.month, self.data_nascimento.day)
                )
            )
        return None

    def get_sexo_display_icon(self):
        """Retorna o ícone do sexo do animal"""
        if self.sexo == "M":
            return "♂️"
        elif self.sexo == "F":
            return "♀️"
        return ""
    
    def get_sexo_display_icon(self):
        """Retorna ícone para o sexo"""
        icons = {
            'M': '♂️',
            'F': '♀️',
            'I': '⚪',
        }
        return icons.get(self.sexo, '')
