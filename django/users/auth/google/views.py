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
    
    Fluxo:
    1. Recebe o código de autorização
    2. Troca o código por um access_token
    3. Usa o token para obter informações do usuário
    4. Valida e cria/autentica o usuário
    5. Redireciona para a home
    
    Validações customizadas podem ser adicionadas em validate_google_user()
    """
    code = request.GET.get('code')
    
    if not code:
        return render(request, 'account/login.html', {
            'error': 'Erro no login com Google: código não fornecido.'
        })

    # Troca o código por um access token
    token_data = exchange_code_for_token(code)
    
    if not token_data or 'access_token' not in token_data:
        print('Erro ao obter token:', token_data)
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

    print('Google user info:', user_info)

    email = user_info.get('email')
    first_name = user_info.get('given_name', '')
    last_name = user_info.get('family_name', '')

    if not email:
        return render(request, 'account/login.html', {
            'error': 'Não foi possível obter o e-mail do Google.'
        })

    # Validações customizadas (pode-se modificar em utils.py)
    validation_error = validate_google_user(email, user_info)
    if validation_error:
        return render(request, 'account/login.html', {'error': validation_error})

    # Cria ou busca o usuário
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': email.split('@')[0],
            'first_name': first_name,
            'last_name': last_name,
        }
    )
    
    print(f'Usuário {"criado" if created else "encontrado"}: {user.username} ({user.email})')

    # Autentica o usuário
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    
    print(f'Usuário autenticado: {request.user.is_authenticated}')
    
    return redirect('home')
