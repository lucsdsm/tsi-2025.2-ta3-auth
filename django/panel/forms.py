"""
Formulários do painel administrativo
"""

from django import forms
from users.models import User
from pets.models import Animal, TipoAnimal, Raca


class ClienteComPetForm(forms.Form):
    """
    Formulário para cadastro de cliente com pet pelo funcionário
    """
    # Dados do Cliente
    first_name = forms.CharField(
        max_length=150,
        label="Nome",
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome do cliente',
            'class': 'form-control'
        })
    )
    
    last_name = forms.CharField(
        max_length=150,
        label="Sobrenome",
        widget=forms.TextInput(attrs={
            'placeholder': 'Sobrenome do cliente',
            'class': 'form-control'
        })
    )
    
    cpf = forms.CharField(
        max_length=14,
        label="CPF",
        widget=forms.TextInput(attrs={
            'placeholder': '000.000.000-00',
            'class': 'form-control'
        }),
        help_text="Formato: 000.000.000-00"
    )
    
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={
            'placeholder': 'email@exemplo.com',
            'class': 'form-control'
        })
    )
    
    telefone = forms.CharField(
        max_length=20,
        required=False,
        label="Telefone",
        widget=forms.TextInput(attrs={
            'placeholder': '(00) 00000-0000',
            'class': 'form-control'
        })
    )
    
    # Dados do Pet
    pet_nome = forms.CharField(
        max_length=100,
        label="Nome do Pet",
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome do animal',
            'class': 'form-control'
        })
    )
    
    pet_tipo = forms.ModelChoiceField(
        queryset=TipoAnimal.objects.filter(ativo=True),
        label="Tipo de Animal",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    pet_raca = forms.ModelChoiceField(
        queryset=Raca.objects.filter(ativo=True),
        label="Raça",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    pet_sexo = forms.ChoiceField(
        choices=[('M', 'Macho'), ('F', 'Fêmea')],
        label="Sexo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    pet_peso = forms.DecimalField(
        max_digits=6,
        decimal_places=2,
        required=False,
        label="Peso (kg)",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Ex: 5.50',
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    pet_tamanho = forms.ChoiceField(
        choices=[
            ('P', 'Pequeno'),
            ('M', 'Médio'),
            ('G', 'Grande'),
            ('GG', 'Muito Grande')
        ],
        required=False,
        label="Porte",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    pet_data_nascimento = forms.DateField(
        required=False,
        label="Data de Nascimento",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    pet_observacoes = forms.CharField(
        required=False,
        label="Observações",
        widget=forms.Textarea(attrs={
            'placeholder': 'Informações adicionais sobre o pet...',
            'class': 'form-control',
            'rows': 3
        })
    )
    
    def clean_cpf(self):
        """Valida CPF"""
        cpf = self.cleaned_data.get('cpf')
        # Remove caracteres não numéricos
        cpf_numeros = ''.join(filter(str.isdigit, cpf))
        
        if len(cpf_numeros) != 11:
            raise forms.ValidationError("CPF deve conter 11 dígitos")
        
        # Verifica se já existe
        if User.objects.filter(username=cpf_numeros).exists():
            raise forms.ValidationError("Já existe um cliente cadastrado com este CPF")
        
        return cpf_numeros
    
    def clean_email(self):
        """Valida email único"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado")
        return email
    
    def save(self):
        """Cria o cliente e o pet"""
        # Cria o usuário/cliente
        user = User.objects.create_user(
            username=self.cleaned_data['cpf'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            password=f"Pet@{self.cleaned_data['cpf'][:6]}",  # Senha padrão com os 6 primeiros dígitos do CPF
            user_type=User.CLIENTE,
            telefone=self.cleaned_data.get('telefone', ''),
            is_active=True
        )
        
        # Cria o pet
        pet = Animal.objects.create(
            proprietario=user,
            nome=self.cleaned_data['pet_nome'],
            tipo_animal=self.cleaned_data['pet_tipo'],
            raca=self.cleaned_data['pet_raca'],
            sexo=self.cleaned_data['pet_sexo'],
            data_nascimento=self.cleaned_data.get('pet_data_nascimento'),
            observacoes=self.cleaned_data.get('pet_observacoes', ''),
            ativo=True
        )
        
        return user, pet
