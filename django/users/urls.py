from django.urls import path, include
from . import views

urlpatterns =[
    path("", views.list_users, name="list_users"),
    path("signUp/", views.create_user, name="create_user"),
    path("login/", views.user_login, name="user_login"),
    path("update/<int:user_id>/", views.update_user, name="update_user"),
    path("delete/<int:user_id>/", views.delete_user, name="delete_user"),
]