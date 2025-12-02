# 🔑 Credenciais de Acesso - Sistema PetShop

## 👨‍💼 Funcionário

**URL de Acesso:** http://localhost:8000/painel-funcionario/

**Credenciais:**
- **Username:** funcionario1
- **Email:** funcionario@petshop.com
- **Senha:** senha123

**Tipo de Usuário:** FUNCIONARIO

**Permissões:**
- ✅ Consultar produtos da loja
- ✅ Agendar consultas com veterinário
- ✅ Cadastrar clientes
- ✅ Cadastrar pets
- ✅ Visualizar lista de pets
- ✅ Visualizar e gerenciar consultas
- ❌ Não pode acessar configurações administrativas
- ❌ Não pode gerenciar usuários do sistema
- ❌ Não pode modificar tipos de animais ou raças

---

## 👨‍⚕️ Veterinário

**URL de Acesso:** http://localhost:8000/painel-veterinario/

**Credenciais:**
- **Username:** veterinario1
- **Email:** vet1@petshop.com
- **Senha:** senha123

**Tipo de Usuário:** VETERINARIO

---

## 👨‍💻 Administrador

**URL de Acesso:** http://localhost:8000/painel-admin/

**Credenciais:**
- **Username:** admin
- **Email:** admin@petshop.com
- **Senha:** admin

**Tipo de Usuário:** ADMIN (is_staff=True)

---

## 🏠 Acesso Geral

**Página Inicial:** http://localhost:8000/
**Login:** http://localhost:8000/users/local/login/
**Cadastro:** http://localhost:8000/users/local/signup/

---

## 🧪 Como Testar o Painel do Funcionário

1. Acesse: http://localhost:8000/users/local/login/
2. Digite:
   - **Login:** funcionario1
   - **Senha:** senha123
3. Clique em "Entrar"
4. Você será redirecionado automaticamente para: http://localhost:8000/painel-funcionario/

---

## 📝 Criar Novo Funcionário

Via Django Shell:

```bash
docker-compose exec web python manage.py shell
```

```python
from users.models import User

funcionario = User.objects.create_user(
    username='novo_funcionario',
    email='funcionario@example.com',
    password='senha123',
    user_type=User.FUNCIONARIO,
    first_name='Nome',
    last_name='Sobrenome'
)
print(f"Funcionário criado: {funcionario.username}")
```

---

**Última atualização:** 29/11/2025
