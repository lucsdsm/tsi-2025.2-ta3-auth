"""
Formulário para complementar dados do cliente
"""

from django import forms
from users.models import User
from pets.models import Animal, TipoAnimal, Raca


class ClienteComplementoForm(forms.ModelForm):
    """
    Formulário para complementar dados de cliente já cadastrado
    """
    cpf = forms.CharField(
        max_length=14,
        required=False,
        label="CPF",
        widget=forms.TextInput(attrs={
            'placeholder': '000.000.000-00',
            'class': 'form-control'
        }),
        help_text="Formato: 000.000.000-00"
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'telefone']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Nome do cliente',
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Sobrenome do cliente',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'email@exemplo.com',
                'class': 'form-control'
            }),
            'telefone': forms.TextInput(attrs={
                'placeholder': '(00) 00000-0000',
                'class': 'form-control'
            }),
        }
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'telefone': 'Telefone',
        }
    
    def clean_cpf(self):
        """Valida CPF se informado"""
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            # Remove caracteres não numéricos
            cpf_numeros = ''.join(filter(str.isdigit, cpf))
            
            if len(cpf_numeros) != 11:
                raise forms.ValidationError("CPF deve conter 11 dígitos")
            
            # Verifica se já existe em outro usuário
            existing = User.objects.filter(username=cpf_numeros).exclude(pk=self.instance.pk).exists()
            if existing:
                raise forms.ValidationError("Já existe um cliente cadastrado com este CPF")
            
            return cpf_numeros
        return cpf
    
    def save(self, commit=True):
        """Atualiza o username com o CPF se informado"""
        user = super().save(commit=False)
        cpf = self.cleaned_data.get('cpf')
        
        # Se CPF foi informado e o username ainda não é um CPF, atualiza
        if cpf and not user.username.isdigit():
            user.username = cpf
        
        if commit:
            user.save()
        return user


class PetCadastroRapidoForm(forms.ModelForm):
    """
    Formulário rápido para cadastrar pet de um cliente existente
    """
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
            ('', 'Selecione...'),
            ('P', 'Pequeno'),
            ('M', 'Médio'),
            ('G', 'Grande'),
            ('GG', 'Muito Grande')
        ],
        required=False,
        label="Porte",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Animal
        fields = ['nome', 'tipo_animal', 'raca', 'sexo', 'data_nascimento', 'observacoes']
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Nome do pet',
                'class': 'form-control'
            }),
            'tipo_animal': forms.Select(attrs={'class': 'form-control'}),
            'raca': forms.Select(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'observacoes': forms.Textarea(attrs={
                'placeholder': 'Informações adicionais sobre o pet...',
                'class': 'form-control',
                'rows': 3
            }),
        }
        labels = {
            'nome': 'Nome do Pet',
            'tipo_animal': 'Tipo de Animal',
            'raca': 'Raça',
            'sexo': 'Sexo',
            'data_nascimento': 'Data de Nascimento',
            'observacoes': 'Observações',
        }
