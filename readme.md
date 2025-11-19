# Sistema de Autenticação e Gerenciamento de animais

Sistema desenvolvido em Django para gerenciamento de usuários e pets, incluindo autenticação local e via Google OAuth2.

## 🚀 Funcionalidades

### 👥 Autenticação de Usuários

#### Autenticação Local
- ✅ **Cadastro de usuários** com validação de email e username
- ✅ **Login** com username ou email
- ✅ **Validações completas** (formato de email, username alfanumérico, etc.)
- ✅ **Mensagens de erro amigáveis** com ícones e feedback visual

#### Autenticação Google OAuth2
- ✅ **Login com Google** integrado
- ✅ **Verificação de email** do Google
- ✅ **Conexão com contas locais existentes** (mesmo email)
- ✅ **Setup de senha** para novos usuários do Google
- ✅ **Validação de emails descartáveis**

### 🐕 Gerenciamento de Pets

O sistema permite que usuários cadastrem e gerenciem seus pets com os seguintes recursos:

#### Funcionalidades Principais
- ✅ **CRUD completo de Animais** (Create, Read, Update, Delete)
- ✅ **Relacionamento user-pet**: cada pet pertence a um único usuário
- ✅ **Tipos de animais** personalizáveis com ícones (🐕 Cachorro, 🐈 Gato, 🐦 Pássaro, 🐰 Coelho, etc.)
- ✅ **Raças** vinculadas a cada tipo de animal
- ✅ **Carregamento dinâmico** de raças no formulário baseado no tipo selecionado
- ✅ **Cálculo automático de idade** baseado na data de nascimento
- ✅ **Interface responsiva** com cards visuais e ícones
- ✅ **Controle de acesso**: apenas o proprietário pode editar/excluir seus pets

#### Dados dos Pets
- Nome do pet
- Tipo de animal (Cachorro, Gato, Pássaro, Coelho, etc.)
- Raça (carregada dinamicamente)
- Sexo (♂️ Macho / ♀️ Fêmea)
- Data de nascimento (com cálculo de idade)
- Observações (alergias, medicamentos, comportamento, etc.)

#### Gerenciamento de Tipos e Raças (Admin/Staff)
- ✅ **CRUD de Tipos de Animais** (apenas staff)
- ✅ **CRUD de Raças** (apenas staff)
- ✅ **Ícones personalizados** para cada tipo
- ✅ **Interface administrativa** dedicada

## 🏗️ Arquitetura

### Estrutura de arquivos:

```
django/
├── app/                    # Configurações principais
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                  # Autenticação de usuários
│   ├── models.py          # Modelo User customizado
│   ├── views.py
│   ├── urls.py
│   ├── auth/
│   │   ├── local/        # Autenticação local
│   │   └── google/       # OAuth2 Google
│   └── templates/
├── pets/                   # Gerenciamento de pets
│   ├── models.py          # TipoAnimal, Raca, Animal
│   ├── views.py           # CRUD + API de raças
│   ├── urls.py
│   ├── admin.py
│   └── templates/         # Templates de pets
└── produtos/             
    ├── models.py          # Produto,categoria,carrinho_de_compras e ver_Carrinho_de_compras
    ├── views.py           # CRUD + API de produtos
    ├── urls.py
    ├── admin.py
    └── templates/         # Templates de Produtos

```

### Modelos de Dados:

#### User (users/models.py)
- Username (único)
- Email (único, validado)
- Password (opcional para usuários Google)
- First name, Last name

#### TipoAnimal (pets/models.py)
- Nome (ex: "Cachorro", "Gato")
- Ícone (emoji: 🐕, 🐈, etc.)

#### Raca (pets/models.py)
- Nome (ex: "Labrador", "Persa")
- TipoAnimal (ForeignKey)
- unique_together: [tipo_animal, nome]

#### Animal (pets/models.py)
- Nome
- Proprietário (ForeignKey → User)
- TipoAnimal (ForeignKey)
- Raca (ForeignKey)
- Sexo (choices: M/F)
- Data de nascimento
- Observações
- unique_together: [proprietario, nome]

#### Produto (produto/models.py)
- produto_id = models.AutoField(primary_key=True)
- nome = models.CharField(max_length=100)
- descricao = models.TextField()
- preco = models.DecimalField(max_digits=10, decimal_places=2)
- estoque = models.IntegerField()
- imagem = models.ImageField(upload_to=caminho_imagem, null=True, blank=True)
- categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, null=True, blank=True)

#### Categoria(produto/models.py)
- id_categoria = models.AutoField(primary_key=True)
- nome_categoria = models.CharField(max_length=100)

#### CarrinhoDeCompras(produto/models.py):
- usuario = models.ForeignKey(User, on_delete= models.CASCADE)

#### ItemDoCarrinho(produto/models.py):
- carrinho = models.ForeignKey(CarrinhoDeCompras, on_delete=models.CASCADE)
- produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
- quantidade = models.IntegerField(default=1)

## 📦 Instalação e Configuração

### 1. Iniciar os Containers (Setup Automático!)

Ao iniciar os containers pela primeira vez, o sistema executa automaticamente:
- ✅ **Criação do superusuário admin** (app users)
  - Username: `admin`
  - Email: `admin@petshop.com`
  - Password: `admin123`
- ✅ **Configuração do Site Django** para localhost (OAuth2)
- ✅ **Criação de 6 tipos de animais** (app pets)
  - 🐕 Cachorro, 🐈 Gato, 🐦 Pássaro, 🐰 Coelho, 🐹 Hamster, 🐠 Peixe
- ✅ **Criação de 42+ raças** distribuídas entre os tipos

```bash
docker-compose up --build -d
```

O setup automático é executado pelo script `entrypoint.sh` que:
1. Aguarda o PostgreSQL estar pronto
2. Aplica todas as migrations
3. Executa `python manage.py init_users` (cria admin e configura Site)
4. Executa `python manage.py init_data` (cria tipos e raças)
5. Inicia o servidor Django

**Credenciais do Admin:**
- **Username:** `admin`
- **Password:** `admin123`

### 2. Configurar Site (Apenas para GitHub Codespaces)

**Se estiver usando localhost**, o site já está configurado automaticamente!

**Para GitHub Codespaces**, atualize o domínio com o comando:

```bash
docker-compose exec web python manage.py shell -c "
from django.contrib.sites.models import Site
site = Site.objects.get(id=1)
site.domain = 'seu-codespace-xxx.app.github.dev'
site.save()
print(f'✓ Site configurado: {site.domain}')
"
```

### 3. Re-executar Inicialização (Se necessário)

Se você precisar recriar os dados, pode executar manualmente:

```bash
# Reinicializar usuários e configurações
docker-compose exec web python manage.py init_users

# Reinicializar dados de pets
docker-compose exec web python manage.py init_data
```

Estes comandos são **idempotentes**, ou seja, podem ser executados múltiplas vezes sem duplicar dados.

## 🌐 Acessar a Aplicação

### Localmente:
```
http://localhost:8000
```

### GitHub Codespaces:
```
https://<seu-codespace>.app.github.dev
```

## 🎯 Rotas Principais

### Autenticação
- `/` - Home page
- `/users/login/` - Login local
- `/users/signup/` - Cadastro
- `/users/google/login/` - Login com Google
- `/users/google/callback/` - Callback OAuth2
- `/users/google/setup-password/` - Setup de senha (novos usuários Google)
- `/users/logout/` - Logout

### Gerenciamento de Pets
- `/pets/animais/` - Lista de pets do usuário
- `/pets/animais/novo/` - Cadastrar novo pet
- `/pets/animais/<id>/editar/` - Editar pet
- `/pets/animais/<id>/excluir/` - Excluir pet

### Admin (Staff apenas)
- `/pets/tipos/` - Gerenciar tipos de animais
- `/pets/racas/` - Gerenciar raças
- `/admin/` - Django Admin

## 🔒 Segurança e Validações

### Usuários
- ✅ Validação de formato de email
- ✅ Bloqueio de emails descartáveis
- ✅ Username alfanumérico (sem espaços)
- ✅ Detecção de contas existentes
- ✅ Verificação de email pelo Google

### Pets
- ✅ Apenas proprietário pode editar/excluir
- ✅ LoginRequiredMixin em todas as views
- ✅ UserPassesTestMixin para verificação de propriedade
- ✅ Soft delete (campo `ativo`)
- ✅ Constraints únicos (user + nome do pet)

## 🛠️ Tecnologias

- **Django 5.1.2** - Framework web
- **PostgreSQL 16** - Banco de dados
- **Docker & Docker Compose** - Containerização
- **Google OAuth2** - Autenticação social
- **Class-Based Views** - ListView, CreateView, UpdateView, DeleteView
- **Template System** - HTML/CSS responsivo com gradientes