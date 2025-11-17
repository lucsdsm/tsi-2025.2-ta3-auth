from django.db import models
from 

# Create your models here.

# depois podera ser removido o null e blank 

# coloca a imagem dinamicamente
def caminho_imagem(instance, filename):
    # Função para definir o caminho onde a imagem será salva
    return f'imagens/{instance.produto_id}/{filename}'

class Produto(models.Model):
    produto_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    imagem = models.ImageField(upload_to=caminho_imagem, null=True, blank=True)
    # o blank=True permite que o campo seja opcional no formulário
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nome_categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_categoria


class CarrinhoDeCompras(models.Model):

