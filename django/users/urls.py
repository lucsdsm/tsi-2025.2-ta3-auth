from django.urls import path, include

urlpatterns = [
    # Rotas de autenticação local (CRUD de usuários)
    path("", include("users.auth.local.urls")),
    
    # Rotas de autenticação Google OAuth
    path("google/", include("users.auth.google.urls")),
]