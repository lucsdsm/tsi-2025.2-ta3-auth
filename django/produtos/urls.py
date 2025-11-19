from django.urls import path
from . import views

urlpatterns = [
    path("", views.produto_list, name="produto_list"),
    path("add/", views.add_produto, name="add_produto"),
    path("update/<int:produto_id>/", views.update_produto, name="update_produto"),
    path("delete/<int:produto_id>/", views.delete_produto, name="delete_produto"),
    path("adicionar_carrinho/<int:produto_id>/", views.adicionar_ao_carrinho, name = "adicionar_ao_carrinho"),
    path("carrinho/", views.ver_carrinho, name = "ver_carrinho"),
]