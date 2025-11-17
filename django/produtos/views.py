from django.shortcuts import render, redirect
from .models import Produto, Categoria

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

