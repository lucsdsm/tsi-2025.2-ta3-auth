from django.urls import path, include
from . import views 

urlpatterns =[
    path("", views.list_users, name="list_users"),
    path("signup/", views.create_user, name="create_user"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("update/<int:user_id>/", views.update_user, name="update_user"),
    path("delete/<int:user_id>/", views.delete_user, name="delete_user"),
    path("google/login/", views.google_login, name="google_login"),
    path("google/callback/", views.google_callback, name="google_callback"),
]