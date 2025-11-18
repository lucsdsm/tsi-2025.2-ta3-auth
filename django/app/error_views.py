"""
Views customizadas para tratamento de erros
"""

from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token


@requires_csrf_token
def csrf_failure(request, reason=""):
    """
    View customizada para erro de CSRF
    Fornece informações mais úteis e opções de recuperação
    """
    context = {
        'reason': reason,
        'referer': request.META.get('HTTP_REFERER', '/'),
        'current_url': request.path,
    }
    return render(request, 'csrf_error.html', context, status=403)
