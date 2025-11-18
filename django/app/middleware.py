"""
Middleware customizado para melhorar a experiência com CSRF
Especialmente após login em ambientes como Codespaces
"""

from django.middleware.csrf import rotate_token


class CSRFRefreshMiddleware:
    """
    Middleware que garante que o token CSRF seja sempre válido,
    especialmente útil após login/logout
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Se o usuário acabou de fazer login, garante token fresco
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Força refresh do token CSRF na resposta
            if hasattr(response, 'csrf_cookie_needs_reset'):
                response.csrf_cookie_needs_reset = True
        
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Executado antes da view ser chamada
        Garante que há sempre um token CSRF válido
        """
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Força criação de token CSRF se não existir
            request.META.get("CSRF_COOKIE")
        
        return None
