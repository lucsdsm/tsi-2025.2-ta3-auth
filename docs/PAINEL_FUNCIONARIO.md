# 👨‍💼 Painel do Funcionário - PetShop

## 📋 Descrição

O Painel do Funcionário é uma interface restrita criada especialmente para funcionários do PetShop, permitindo que realizem tarefas operacionais do dia a dia sem ter acesso às configurações administrativas do sistema.

## 🎯 Funcionalidades Disponíveis

### ✅ Permitido

1. **Consulta de Produtos da Loja**
   - Visualizar catálogo completo de produtos
   - Ver preços e disponibilidade em estoque
   - Acessar detalhes dos produtos

2. **Marcação de Consultas com Veterinário**
   - Agendar novas consultas
   - Visualizar consultas agendadas
   - Consultar disponibilidade dos veterinários

3. **Cadastro de Clientes**
   - Registrar novos clientes no sistema
   - Atualizar dados de clientes existentes

4. **Cadastro de Pets**
   - Adicionar novos pets
   - Vincular pets aos seus proprietários
   - Atualizar informações dos pets

### ❌ Não Permitido

- Gerenciar usuários do sistema (criar/editar funcionários, veterinários, etc.)
- Modificar tipos de animais ou raças
- Acessar configurações do sistema
- Ver relatórios administrativos completos
- Realizar vendas de produtos (apenas consulta)

## 🚀 Como Acessar

### Credenciais de Teste

**Usuário Funcionário Padrão:**
- **Username:** `funcionario1`
- **Email:** `funcionario@petshop.com`
- **Senha:** `senha123`

### Passo a Passo

1. Acesse a página de login: `http://localhost:8000/users/local/login/`
2. Entre com as credenciais de funcionário
3. Você será automaticamente redirecionado para: `http://localhost:8000/painel-funcionario/`

## 🎨 Interface do Painel

O painel do funcionário possui um design moderno com:

- **Cor Principal:** Verde (#1abc9c) - diferenciando do painel administrativo
- **Menu Lateral:** Acesso rápido às funcionalidades permitidas
- **Dashboard:** Visão geral com estatísticas relevantes
- **Cards de Ação Rápida:** Atalhos para as tarefas mais comuns

### Seções do Menu

```
📊 Dashboard
├── Estatísticas gerais
└── Ações rápidas

👥 Clientes e Pets
├── ➕ Cadastrar Cliente
├── 🐾 Cadastrar Pet
└── 📋 Listar Pets

📅 Consultas
├── 📅 Agendar Consulta
└── 📋 Listar Consultas

🛒 Produtos
└── 🛒 Consultar Loja

🔧 Sistema
├── 🏠 Voltar ao Site
└── 🚪 Sair
```

## 📊 Dashboard - Informações Exibidas

### Estatísticas em Cards

- **Total de Clientes:** Quantidade de clientes ativos no sistema
- **Pets Cadastrados:** Número total de pets registrados
- **Consultas Hoje:** Consultas agendadas para o dia atual
- **Produtos Disponíveis:** Produtos com estoque disponível

### Listas Rápidas

- **Clientes Recentes:** Últimos 5 clientes cadastrados
- **Pets Recentes:** Últimos 5 pets registrados
- **Próximas Consultas:** Consultas agendadas (próximos dias)
- **Produtos em Destaque:** Produtos mais recentes da loja

### Ações Rápidas

Botões de acesso direto para:
- 👤 Cadastrar Cliente
- 🐕 Cadastrar Pet
- 📅 Agendar Consulta
- 🛒 Consultar Loja

## 🔒 Segurança e Restrições

### Controle de Acesso

A view do dashboard do funcionário (`DashboardFuncView`) implementa:

```python
class DashboardFuncView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    def test_func(self):
        return self.request.user.is_funcionario()
```

Isso garante que:
- ✅ Apenas usuários autenticados podem acessar
- ✅ Apenas usuários com `user_type='FUNCIONARIO'` têm acesso
- ❌ Clientes, veterinários e administradores são redirecionados

### Redirecionamento Automático

Ao fazer login, o sistema automaticamente redireciona para o painel correto:

- **Administrador (is_staff=True)** → `/painel-admin/`
- **Veterinário** → `/painel-veterinario/`
- **Funcionário** → `/painel-funcionario/`
- **Cliente** → `/` (home)

## 🛠️ Estrutura Técnica

### Arquivos Criados/Modificados

```
django/
├── panel/
│   ├── views/
│   │   └── dashboard.py (+ DashboardFuncView)
│   ├── templates/
│   │   ├── base_func.html (novo template base)
│   │   └── dashboard_funcionario.html (novo dashboard)
│   └── urls.py (mantido sem alterações)
├── app/
│   └── urls.py (+ rota painel-funcionario)
└── users/
    └── auth/
        └── local/
            └── views.py (+ lógica de redirecionamento)
```

### Rota Principal

```python
# app/urls.py
path("painel-funcionario/", DashboardFuncView.as_view(), name='painel_funcionario')
```

### Template Base

O template `base_func.html` é personalizado para funcionários e contém:
- Menu lateral com links restritos
- Cor de destaque verde
- Indicador de cargo "Funcionário"

## 💡 Dicas de Uso

### Para Funcionários

1. **Sempre confirme os dados** do cliente antes de cadastrar
2. **Verifique a disponibilidade** do veterinário ao agendar consultas
3. **Mantenha os dados dos pets atualizados** (vacinas, peso, etc.)
4. **Consulte o estoque** de produtos antes de indicar ao cliente
5. **Em caso de dúvidas**, contate o administrador

### Para Desenvolvedores

1. **Adicionar novas funcionalidades:** Edite `base_func.html` para adicionar novos links no menu
2. **Modificar permissões:** Ajuste o método `test_func()` na view
3. **Customizar estatísticas:** Edite o método `get_context_data()` em `DashboardFuncView`
4. **Alterar design:** Modifique os estilos em `base_func.html` e `dashboard_funcionario.html`

## 🧪 Testando o Sistema

### Criar Novo Funcionário (via Django Shell)

```bash
docker-compose exec web python manage.py shell
```

```python
from users.models import User

# Criar funcionário
funcionario = User.objects.create_user(
    username='funcionario2',
    email='funcionario2@petshop.com',
    password='senha123',
    user_type=User.FUNCIONARIO,
    first_name='Maria',
    last_name='Silva'
)

print(f"Funcionário criado: {funcionario.username}")
```

### Verificar Funcionários Cadastrados

```bash
docker-compose exec web python manage.py shell -c "
from users.models import User
funcionarios = User.objects.filter(user_type='FUNCIONARIO')
print(f'Total: {funcionarios.count()} funcionários')
for f in funcionarios:
    print(f'- {f.username} ({f.email})')
"
```

## 📝 Notas Importantes

1. **Diferença dos outros painéis:**
   - O painel do funcionário tem menos permissões que o admin
   - Não pode acessar configurações avançadas
   - Focado em operações do dia a dia

2. **Integração com outros módulos:**
   - Usa as mesmas views de cadastro de clientes e pets
   - Compartilha as views de consulta com o veterinário
   - Acessa a loja em modo somente leitura

3. **Futuras melhorias:**
   - Adicionar relatório de consultas do dia
   - Implementar sistema de vendas (atualmente só consulta)
   - Adicionar histórico de atendimentos
   - Criar sistema de notificações

## 🐛 Troubleshooting

### Erro: "Você não tem permissão para acessar esta página"

**Causa:** O usuário não tem `user_type='FUNCIONARIO'`

**Solução:**
```python
# No Django Shell
from users.models import User
user = User.objects.get(username='seu_usuario')
user.user_type = User.FUNCIONARIO
user.save()
```

### Erro: "NoReverseMatch at /painel-funcionario/"

**Causa:** URL não configurada corretamente

**Solução:** Verifique se a rota está em `app/urls.py`:
```python
path("painel-funcionario/", DashboardFuncView.as_view(), name='painel_funcionario')
```

### Painel aparece vazio ou sem dados

**Causa:** Banco de dados sem informações

**Solução:** Execute os comandos de setup:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py loaddata initial_data
```

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique este README
2. Consulte os logs: `docker-compose logs web`
3. Entre em contato com a equipe de desenvolvimento

---

**Versão:** 1.0  
**Última atualização:** 29/11/2025  
**Desenvolvido por:** Equipe PetShop
