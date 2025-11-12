from django.shortcuts import render
from .models import Produto

# Create your views here.

def produto_list(request):

    produtos = Produto.objects.all()
    return render(request, 'produto_list.html', {'produtos': produtos})


def add_produto(request):
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
        return render(request, 'produtos/add_produto.html', {'sucesso': True})
    return render(request, 'produtos/add_produto.html')

def update_produto(request, produto_id):
    try:
        produto = Produto.objects.get(id=produto_id)
    except Produto.DoesNotExist:
        return render(request, 'produtos/update_produto.html', {'erro': 'Produto não encontrado.'})
    
    if request.method == 'POST':
        produto.nome = request.POST.get('nome')
        produto.descricao = request.POST.get('descricao')
        produto.preco = request.POST.get('preco')
        produto.estoque = request.POST.get('estoque')
        produto.save()
        return render(request, 'produtos/update_produto.html', {'produto': produto, 'sucesso': True})
    
    return render(request, 'produtos/update_produto.html', {'produto': produto})

def delete_produto(request, produto_id):
    try:
        produto = Produto.objects.get(id=produto_id)
        produto.delete()
        return render(request, 'produtos/delete_produto.html', {'sucesso': True})
    except Produto.DoesNotExist:
        return render(request, 'produtos/delete_produto.html', {'erro': 'Produto não encontrado.'})

