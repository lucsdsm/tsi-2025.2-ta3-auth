from django.db import models

# Create your models here.


class Produto(models.Model):
    produto_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    # o blank=True permite que o campo seja opcional no formulário
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nome_categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_categoria
