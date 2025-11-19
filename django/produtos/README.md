# App: produtos

Resumo rápido  
Gerencia produtos, categorias e carrinho de compras. Contém CRUD de produtos, upload de imagens e carrinho por usuário.

## Estrutura principal
- modelos: produtos/models.py
- views: produtos/views.py
- urls: produtos/urls.py
- templates: produtos/templates/*.html
- mídia: /django/media (MEDIA_ROOT)

## Modelos (essenciais)
- Produto: id, nome, descrição, preço, estoque, imagem, categoria (FK)
- Categoria: id, nome
- CarrinhoDeCompras: usuário (FK → User)
- ItemDoCarrinho: carrinho (FK), produto (FK), quantidade

### Exemplo do modelo Produto
```python
// filepath: /workspaces/tsi-2025.2-ta3-auth/django/produtos/models.py
# ...existing code...
class Produto(models.Model):
    produto_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    imagem = models.ImageField(upload_to=caminho_imagem, null=True, blank=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, null=True, blank=True)
# ... code...
```

## Views úteis (exemplos)
- listar produtos, adicionar ao carrinho, ver carrinho.

```python
// filepath: /workspaces/tsi-2025.2-ta3-auth/django/produtos/views.py
# ...existing code...
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Produto, CarrinhoDeCompras, ItemDoCarrinho

def produto_list(request):
    products = Produto.objects.filter(estoque__gt=0).order_by('-produto_id')[:50]
    return render(request, "produtos/produto_list.html", {"products": products})

@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, produto_id=produto_id)
    carrinho, _ = CarrinhoDeCompras.objects.get_or_create(usuario=request.user)
    item, created = ItemDoCarrinho.objects.get_or_create(carrinho=carrinho, produto=produto)
    if not created:
        item.quantidade += 1
        item.save()
    return redirect('ver_carrinho', user_id=request.user.id)

@login_required
def ver_carrinho(request, user_id=None):
    # se user_id não for passado, usa request.user
    if user_id is None:
        user = request.user
    else:
        user = get_object_or_404(User, id=user_id)
    if request.user != user and not request.user.is_staff:
        return redirect('produto_list')
    cart = CarrinhoDeCompras.objects.filter(usuario=user).first()
    items = ItemDoCarrinho.objects.filter(carrinho=cart).select_related('produto') if cart else []
    total = sum(i.quantidade * i.produto.preco for i in items)
    return render(request, "produtos/carrinho_de_compras.html", {"cart": cart, "items": items, "total": total})
# ...existing code...
```

## URLs (já existentes)
```python
// filepath: /workspaces/tsi-2025.2-ta3-auth/django/produtos/urls.py
# ...existing code...
urlpatterns = [
    path("", views.produto_list, name="produto_list"),
    path("add/", views.add_produto, name="add_produto"),
    path("update/<int:produto_id>/", views.update_produto, name="update_produto"),
    path("delete/<int:produto_id>/", views.delete_produto, name="delete_produto"),
    path("adicionar_carrinho/<int:produto_id>/", views.adicionar_ao_carrinho, name="adicionar_ao_carrinho"),
    path("carrinho/", views.ver_carrinho, name="ver_carrinho"),
]
# ...existing code...
```
> Observação: aqui a rota de carrinho está definida sem user_id — a view aceita request.user. Se quiser usar `/carrinho/<user_id>/` ajuste tanto URL quanto view.

## Template: card de produto (exemplo)
```html
// filepath: /workspaces/tsi-2025.2-ta3-auth/django/produtos/templates/produto_list.html
{% extends 'loja.html' %}

{% block content %}
<div class="grid-produtos">
  {% for produto in products %}
  <div class="card-produto">
    {% if produto.imagem %}
      <img src="{{ produto.imagem.url }}" alt="{{ produto.nome }}">
    {% endif %}
    <h3>{{ produto.nome }}</h3>
    <p class="descricao">{{ produto.descricao|truncatechars:80 }}</p>
    <div class="preco">R$ {{ produto.preco|floatformat:2 }}</div>
    <form action="{% url 'adicionar_ao_carrinho' produto.produto_id %}" method="post">
      {% csrf_token %}
      <button type="submit" class="btn-primary">Adicionar ao carrinho</button>
    </form>
  </div>
  {% empty %}
  <p>Nenhum produto disponível.</p>
  {% endfor %}
</div>
{% endblock %}
```

## Como gerar migrations e aplicar (Docker Compose)
```bash
# build e subir containers
docker-compose up -d --build

# criar migrations do app produtos
docker-compose exec web python manage.py makemigrations produtos

# aplicar migrations
docker-compose exec web python manage.py migrate
```

## Mídia / Imagens
- Em desenvolvimento, imagens são armazenadas em `django/media/`.
- Template deve checar `if produto.imagem` antes de renderizar `produto.imagem.url`.

## Boas práticas e dicas rápidas
- Use `user.set_password()` ao criar/atualizar senhas (se houver relação com usuários).
- Valide estoque antes de confirmar adição ao carrinho.
- Proteja views de manipulação do carrinho com `@login_required`.
- Para APIs futuras, criar endpoints REST (Django REST Framework).

## Check rápido (debug)
- Logs do Django: `docker-compose logs -f web`
- Ver migrations aplicadas: `docker-compose exec web python manage.py showmigrations produtos`
- Entrar no DB: `docker-compose exec db psql -U postgres -d petshopdb`