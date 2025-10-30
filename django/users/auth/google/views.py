"""
Módulo de Autenticação Google OAuth2
====================================

Este módulo fornece autenticação via Google OAuth2.
É totalmente independente e pode ser usado em qualquer projeto Django.

Funcionalidades:
- Login com Google
- Criação automática de usuário na primeira autenticação
- Validação de email duplicado
- Suporte a customização de validações

Requisitos:
- requests (pip install requests)
- Variáveis de ambiente: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

Para usar em outro projeto:
1. Copie esta pasta 'google' para seu projeto
2. Configure as credenciais do Google no .env
3. Configure as URLs no seu urls.py principal
4. Atualize REDIRECT_URI no utils.py com sua URL
5. Registre a URI de redirecionamento no Google Cloud Console

Configuração no Google Cloud Console:
1. Crie um projeto em https://console.cloud.google.com
2. Ative a API Google+ ou Google People API
3. Crie credenciais OAuth 2.0
4. Adicione a URI de redirecionamento: https://seu-dominio.com/auth/google/callback/
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie
from .utils import (
    get_google_auth_url,
    exchange_code_for_token,
    get_user_info_from_google,
    validate_google_user,
)

User = get_user_model()


def google_login(request):
    """
    Redireciona o usuário para a tela de consentimento do Google.
    
    Gera uma URL de autenticação OAuth2 e redireciona o usuário.
    Após autorização, o Google redirecionará para google_callback.
    """
    auth_url = get_google_auth_url()
    return redirect(auth_url)

def google_callback(request):
    """
    Recebe o callback do Google após autenticação.
    
    Fluxo inteligente:
    1. Recebe o código de autorização
    2. Troca o código por um access_token
    3. Usa o token para obter informações do usuário
    4. Verifica se já existe usuário com este email:
       - Se existe: conecta nele (mesmo criado localmente)
       - Se não existe: cria novo e redireciona para definir senha
    5. Autentica e redireciona
    
    Validações:
    - Email verificado no Google
    - Conflitos de username
    - Validações customizadas em validate_google_user()
    """
    
    code = request.GET.get('code')
    
    if not code:
        error_msg = request.GET.get('error', 'Código não fornecido')
        return render(request, 'account/login.html', {
            'error': f'Erro no login com Google: {error_msg}'
        })

    # Troca o código por um access token
    token_data = exchange_code_for_token(code)
    
    if not token_data or 'access_token' not in token_data:
        return render(request, 'account/login.html', {
            'error': 'Erro ao obter token do Google.'
        })

    access_token = token_data['access_token']
    
    # Busca informações do usuário
    user_info = get_user_info_from_google(access_token)
    
    if not user_info:
        return render(request, 'account/login.html', {
            'error': 'Erro ao obter informações do usuário.'
        })

    email = user_info.get('email')
    email_verified = user_info.get('verified_email', False)
    first_name = user_info.get('given_name', '')
    last_name = user_info.get('family_name', '')

    if not email:
        return render(request, 'account/login.html', {
            'error': 'Não foi possível obter o e-mail do Google.'
        })

    # VALIDAÇÃO: Email deve estar verificado no Google
    if not email_verified:
        return render(request, 'account/login.html', {
            'error': 'Seu e-mail não está verificado no Google. Por favor, verifique seu e-mail antes de continuar.'
        })

    # Validações customizadas (pode-se modificar em utils.py)
    validation_error = validate_google_user(email, user_info)
    if validation_error:
        return render(request, 'account/login.html', {'error': validation_error})

    # Verifica se já existe usuário com este email
    try:
        user = User.objects.get(email=email)
        created = False
        
        # Atualiza informações do Google se estiverem vazias
        if not user.first_name and first_name:
            user.first_name = first_name
        if not user.last_name and last_name:
            user.last_name = last_name
        user.save()
        
    except User.DoesNotExist:
        # Usuário não existe, vamos criar
        created = True
        
        # Gera username único baseado no email
        base_username = email.split('@')[0]
        username = base_username
        counter = 1
        
        # Garante username único
        while User.objects.filter(username=username).exists():
            username = f'{base_username}{counter}'
            counter += 1
        
        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        # Marca explicitamente que o usuário não tem senha
        user.set_unusable_password()
        user.save()

    # Autentica o usuário
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    
    # Se for um novo usuário OU usuário sem senha, redireciona para criar senha
    if created or not user.has_usable_password():
        return redirect('google_setup_password')
    
    # Usuário existente com senha, vai direto para home
    return redirect('home')


@ensure_csrf_cookie
def google_setup_password(request):
    """
    Página para novos usuários do Google criarem uma senha.
    
    Após login inicial com Google, usuários sem senha são redirecionados
    aqui para definir uma senha local, permitindo login tradicional futuro.
    
    Validações:
    - Usuário deve estar autenticado
    - Senha mínima de 8 caracteres
    - Confirmação de senha
    - Senhas devem bater
    """
    # Verifica se usuário está logado
    if not request.user.is_authenticated:
        return redirect('local_login')
    
    # Se usuário já tem senha, redireciona para home
    if request.user.has_usable_password():
        return redirect('home')
    
    print(f'[INFO] Mostrando formulário de setup de senha')
    
    print(f'[INFO] Mostrando formulário de setup de senha')
    
    error_message = None
    
    if request.method == 'POST':
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()
        
        # Validações
        if not password or not password_confirm:
            error_message = '❌ Todos os campos são obrigatórios.'
        
        elif len(password) < 8:
            error_message = '❌ A senha deve ter pelo menos 8 caracteres.'
        
        elif len(password) > 128:
            error_message = '❌ A senha não pode ter mais de 128 caracteres.'
        
        elif password != password_confirm:
            error_message = '❌ As senhas não coincidem. Verifique os valores.'
        
        elif password == request.user.email:
            error_message = '❌ A senha não pode ser igual ao seu email.'
        
        if error_message is None:
            # Define a senha do usuário
            request.user.set_password(password)
            request.user.save()
            
            # Re-autentica o usuário (necessário após mudar senha)
            user = request.user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            
            return redirect('home')
    
    return render(request, 'account/setup_password.html', {
        'error': error_message,
        'user': request.user
    })
