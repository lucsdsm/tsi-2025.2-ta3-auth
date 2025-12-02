"""
Middleware customizado para melhorar a experiência com CSRF
Especialmente após login em ambientes como Codespaces
"""

from django.middleware.csrf import get_token
from django.utils.deprecation import MiddlewareMixin


class CSRFRefreshMiddleware(MiddlewareMixin):
    """
    Middleware que garante que o token CSRF seja sempre válido,
    especialmente útil após login/logout
    """
    
    def process_request(self, request):
        """
        Executado antes da view ser processada.
        Garante que sempre há um token CSRF disponível.
        """
        # Força a geração do token CSRF para todas as requisições
        get_token(request)
        return None
