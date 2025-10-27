"""
URLs para Autenticação Local

Para usar em outro projeto, inclua no seu urls.py principal:
    path('auth/local/', include('users.auth.local.urls')),
"""

from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.create_user, name='local_signup'),
    path('login/', views.user_login, name='local_login'),
    path('logout/', views.user_logout, name='local_logout'),
    path('users/', views.list_users, name='list_users'),
    path('users/update/<int:user_id>/', views.update_user, name='update_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
]
