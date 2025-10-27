"""
URLs para Autenticação Google OAuth2

Para usar em outro projeto, inclua no seu urls.py principal:
    path('auth/google/', include('users.auth.google.urls')),

Certifique-se de registrar a URI de callback no Google Cloud Console:
    https://seu-dominio.com/auth/google/callback/
"""

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.google_login, name='google_login'),
    path('callback/', views.google_callback, name='google_callback'),
]
