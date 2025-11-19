from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from .models import Produto, Categoria, CarrinhoDeCompras, ItemDoCarrinho
from django.contrib.auth.decorators import login_required

# Create your views here.

def produto_list(request):

    produtos = Produto.objects.all()
    return render(request, 'produto_list.html', {'produtos': produtos})


def add_produto(request):
# Olhar como add imagens depois
    
    categorias = Categoria.objects.all()
    produtos = Produto.objects.all()

    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco =  request.POST.get('preco')
        categoria = request.POST.get('categoria')
        estoque = request.POST.get('estoque')

        produto = Produto (
            nome = nome,
            descricao = descricao,
            preco = preco,
            estoque = estoque,
            categoria_id = categoria
        )
        produto.save()
        # return redirect(request, 'add_produto.html', {'sucesso': True, 'categorias' : categorias,'produtos' : produtos})
        return redirect('add_produto')
    return render(request, 'add_produto.html',{'categorias' : categorias, 'produtos' : produtos})

def update_produto(request, produto_id):
    try:
        produto = Produto.objects.get(produto_id=produto_id)
    except Produto.DoesNotExist:
        return render(request, 'update_produto.html', {'erro': 'Produto não encontrado.'})
    
    if request.method == 'POST':
        produto.nome = request.POST.get('nome')
        produto.descricao = request.POST.get('descricao')
        produto.preco = request.POST.get('preco')
        produto.estoque = request.POST.get('estoque')
        produto.save()
        return render(request, 'update_produto.html', {'produto': produto, 'sucesso': True})
    
    return render(request, 'update_produto.html', {'produto': produto})

def delete_produto(request, produto_id):
    try:
        produto = Produto.objects.get(produto_id=produto_id)
        produto.delete()
        return redirect('add_produto')
    except Produto.DoesNotExist:
        return redirect('add_produto')


@login_required
def adicionar_ao_carrinho(request, produto_id):

    if request.method == 'POST':
        # quantidade enviada no form (padrão 1)
        try:
            quantidade = int(request.POST.get('quantidade', 1))
        except (TypeError, ValueError):
            quantidade = 1

        # garante que o produto existe
        produto = get_object_or_404(Produto, produto_id=produto_id)

        # Verifica se o carrinho existe para o usuário autenticado, se não, cria um novo
        carrinho, criado_carrinho = CarrinhoDeCompras.objects.get_or_create(usuario=request.user)

        # verifica se o item já está no carrinho, se não, cria um novo com a quantidade
        item, criado_item = ItemDoCarrinho.objects.get_or_create(
            carrinho=carrinho,
            produto=produto,
            defaults={'quantidade': quantidade}
        )

        if not criado_item:
            # atualiza a quantidade existente
            item.quantidade = (item.quantidade or 0) + quantidade
            item.save()

        return redirect('produto_list')

    return redirect('produto_list')

@login_required
def ver_carrinho(request):
    # Obtém ou cria o carrinho do usuário autenticado
    carrinho, carrinho_criado = CarrinhoDeCompras.objects.get_or_create(usuario=request.user)

    # Busca itens relacionados ao carrinho, e o select_related para otimizar consultas
    itens = ItemDoCarrinho.objects.filter(carrinho=carrinho).select_related('produto')

    # Monta estrutura esperada pelo template
    produtos = []
    total = Decimal('0.00')
    for item in itens:
        preco = item.produto.preco or Decimal('0.00')
        subtotal = preco * item.quantidade
        produtos.append({
            'produto': item.produto,
            'quantidade': item.quantidade,
            'subtotal': f"{subtotal:.2f}"
        })
        total += subtotal

    return render(request, 'carrinho_de_compras.html', {'produtos': produtos, 'produto_total': f"{total:.2f}"})





    

