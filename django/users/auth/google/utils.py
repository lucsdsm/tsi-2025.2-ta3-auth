"""
Funções auxiliares para autenticação Google OAuth2
==================================================

Contém toda a lógica de comunicação com a API do Google.
"""

import os
import requests
from secrets import token_urlsafe


# ============================================
# CONFIGURAÇÕES 
# ============================================

def get_redirect_uri():
    """
    Retorna a URI de redirecionamento configurada.
    
    IMPORTANTE: Atualize esta URL para corresponder ao domínio.
    Esta mesma URL deve estar registrada no Google Cloud Console.
    """
    # Para desenvolvimento local:
    # return 'http://localhost:8000/auth/google/callback/'
    
    # Para produção/Codespaces:
    return 'https://zany-goggles-94w6qq9v55g2w55-8000.app.github.dev/users/google/callback/'


def get_google_credentials():
    """
    Retorna as credenciais do Google OAuth.
    
    Lê do ambiente (.env) as variáveis:
    - GOOGLE_CLIENT_ID
    - GOOGLE_CLIENT_SECRET
    """
    return {
        'client_id': os.getenv('GOOGLE_CLIENT_ID'),
        'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
    }

# ============================================
# FUNÇÕES PRINCIPAIS
# ============================================

def get_google_auth_url():
    """
    Gera a URL de autenticação do Google OAuth2.
    
    Returns:
        str: URL completa para redirecionar o usuário
    """
    credentials = get_google_credentials()
    redirect_uri = get_redirect_uri()
    
    # Gera um state aleatório para proteção CSRF
    state = token_urlsafe(16)
    
    params = {
        'client_id': credentials['client_id'],
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'openid email profile',
        'state': state,
    }
    
    # Constrói a URL
    base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
    
    return f'{base_url}?{query_string}'


def exchange_code_for_token(code):
    """
    Troca o código de autorização por um access token.
    
    Args:
        code (str): Código recebido do Google
        
    Returns:
        dict: Dados do token (access_token, id_token, etc.) ou None se falhar
    """
    credentials = get_google_credentials()
    redirect_uri = get_redirect_uri()
    
    token_url = 'https://oauth2.googleapis.com/token'
    data = {
        'code': code,
        'client_id': credentials['client_id'],
        'client_secret': credentials['client_secret'],
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
    }
    
    try:
        response = requests.post(token_url, data=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f'Erro ao trocar código por token: {e}')
        return None


def get_user_info_from_google(access_token):
    """
    Busca informações do usuário usando o access token.
    
    Args:
        access_token (str): Token de acesso obtido do Google
        
    Returns:
        dict: Dados do usuário (email, name, etc.) ou None se falhar
    """
    user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        response = requests.get(user_info_url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f'Erro ao buscar informações do usuário: {e}')
        return None


# ============================================
# VALIDAÇÕES CUSTOMIZADAS
# ============================================

def validate_google_user(email, user_info):
    """
    Valida o usuário antes de criar/autenticar.

    Aqui pode-se adicionar suas próprias regras de negócio:
    - Bloquear domínios específicos
    - Exigir domínio corporativo
    - Verificar lista negra
    - Validar informações adicionais
    
    Args:
        email (str): Email do usuário
        user_info (dict): Informações completas retornadas pelo Google
        
    Returns:
        str: Mensagem de erro se inválido, None se válido
    """
    # Exemplo: Bloquear emails de determinados domínios
    # blocked_domains = ['example.com', 'spam.com']
    # domain = email.split('@')[1]
    # if domain in blocked_domains:
    #     return f'Emails do domínio {domain} não são permitidos.'
    
    # Exemplo: Aceitar apenas emails corporativos
    # allowed_domain = 'suaempresa.com'
    # if not email.endswith(f'@{allowed_domain}'):
    #     return 'Apenas emails corporativos são permitidos.'
    
    # Exemplo: Verificar se email já existe (comentado pois get_or_create já trata)
    # from django.contrib.auth import get_user_model
    # User = get_user_model()
    # if User.objects.filter(email=email).exists():
    #     return 'Email já cadastrado no sistema.'
    
    # Se passar todas as validações, retorna None (sem erro)
    return None
