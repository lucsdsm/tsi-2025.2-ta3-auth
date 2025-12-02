"""
Forms para gerenciamento de usuários
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import User


class FuncionarioCreateForm(forms.ModelForm):
    """
    Formulário para criação de funcionários pelo administrador.
    Usa sistema de matrícula com prefixos e gera senha padrão automaticamente.
    """
    
    matricula = forms.CharField(
        max_length=6,
        min_length=6,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 100001, 150001, 200001, 250001',
            'pattern': '[0-9]{6}',
            'title': 'Digite exatamente 6 dígitos numéricos'
        }),
        help_text='Prefixos: 10-Veterinário, 15-Gerente, 20-Supervisor, 25-Funcionário (seguido de 4 dígitos)'
    )
    
    user_type = forms.ChoiceField(
        choices=[
            (User.VETERINARIO, 'Veterinário'),
            (User.GERENTE, 'Gerente'),
            (User.SUPERVISOR, 'Supervisor'),
            (User.FUNCIONARIO, 'Funcionário'),
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Tipo de Funcionário'
    )
    
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
        label='Nome'
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}),
        label='Sobrenome'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
        label='E-mail'
    )
    
    telefone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
        label='Telefone'
    )
    
    # Campos específicos para veterinários
    crmv = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CRMV'}),
        label='CRMV',
        help_text='Obrigatório apenas para Veterinários'
    )
    
    especialidade = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Especialidade'}),
        label='Especialidade',
        help_text='Obrigatório apenas para Veterinários'
    )
    
    class Meta:
        model = User
        fields = ['matricula', 'user_type', 'first_name', 'last_name', 'email', 'telefone', 'crmv', 'especialidade']
    
    def clean_matricula(self):
        """Valida a matrícula"""
        matricula = self.cleaned_data.get('matricula')
        
        # Verifica se matrícula já existe
        if User.objects.filter(matricula=matricula).exists():
            raise ValidationError('Esta matrícula já está em uso.')
        
        # Valida formato (será validada junto com user_type em clean())
        if not matricula.isdigit():
            raise ValidationError('Matrícula deve conter apenas números.')
        
        if len(matricula) != 6:
            raise ValidationError('Matrícula deve ter exatamente 6 dígitos.')
        
        return matricula
    
    def clean_email(self):
        """Valida se o email já não está cadastrado"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este e-mail já está cadastrado.')
        return email
    
    def clean(self):
        """Validação cruzada de matrícula e tipo de usuário"""
        cleaned_data = super().clean()
        matricula = cleaned_data.get('matricula')
        user_type = cleaned_data.get('user_type')
        crmv = cleaned_data.get('crmv')
        especialidade = cleaned_data.get('especialidade')
        
        # Valida matrícula de acordo com o tipo
        if matricula and user_type:
            is_valid, message = User.validar_matricula(matricula, user_type)
            if not is_valid:
                raise ValidationError({'matricula': message})
        
        # Valida campos obrigatórios para veterinários
        if user_type == User.VETERINARIO:
            if not crmv:
                raise ValidationError({'crmv': 'CRMV é obrigatório para Veterinários.'})
            if not especialidade:
                raise ValidationError({'especialidade': 'Especialidade é obrigatória para Veterinários.'})
        
        return cleaned_data
    
    def save(self, commit=True):
        """
        Salva o funcionário com username baseado na matrícula
        e senha padrão gerada automaticamente
        """
        user = super().save(commit=False)
        
        # Define username como a matrícula
        user.username = self.cleaned_data['matricula']
        
        # Gera e define senha padrão
        senha_padrao = User.gerar_senha_padrao(self.cleaned_data['matricula'])
        user.set_password(senha_padrao)
        
        # Define is_active como True
        user.is_active = True
        
        if commit:
            user.save()
        
        return user


class ClientePublicCreateForm(forms.ModelForm):
    """
    Formulário público para cadastro de clientes.
    Apenas permite criar usuários do tipo CLIENTE.
    """
    
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
        label='Nome de Usuário'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
        label='E-mail'
    )
    
    password = forms.CharField(
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mínimo 8 caracteres'}),
        label='Senha'
    )
    
    password_confirm = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme sua senha'}),
        label='Confirmar Senha'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email']
    
    def clean_username(self):
        """Valida se o username já não está cadastrado"""
        username = self.cleaned_data.get('username')
        
        if len(username) < 3:
            raise ValidationError('Nome de usuário deve ter pelo menos 3 caracteres.')
        
        if User.objects.filter(username=username).exists():
            raise ValidationError('Este nome de usuário já está em uso.')
        
        return username
    
    def clean_email(self):
        """Valida se o email já não está cadastrado"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este e-mail já está cadastrado.')
        return email
    
    def clean(self):
        """Valida se as senhas coincidem"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise ValidationError({'password_confirm': 'As senhas não coincidem.'})
        
        return cleaned_data
    
    def save(self, commit=True):
        """Salva o usuário como CLIENTE com senha criptografada"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.user_type = User.CLIENTE
        user.is_active = True
        
        if commit:
            user.save()
        
        return user
