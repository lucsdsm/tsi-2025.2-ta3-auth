# 🔑 Credenciais de Acesso - Sistema PetShop

## 🏢 Sistema de Matrícula

O sistema utiliza **matrícula + senha padrão** para funcionários. A senha padrão é gerada automaticamente no formato: `Pet@{matrícula}`

### **Prefixos de Matrícula por Tipo:**
- **10XXXX** → Veterinário
- **15XXXX** → Gerente
- **20XXXX** → Supervisor
- **25XXXX** → Funcionário

**Exemplo:** Matrícula `100001` tem senha `Pet@100001`

---

## 👨‍⚕️ Veterinário

**URL de Acesso:** http://localhost:8000/painel-veterinario/

**Credenciais de Teste:**
- **Matrícula:** 100001
- **Senha:** Pet@100001
- **Email:** vet1@petshop.com
- **Tipo:** VETERINARIO

**Permissões:**
- ✅ Dashboard com estatísticas de consultas
- ✅ Agendar, visualizar e gerenciar consultas
- ✅ Criar e editar prontuários médicos
- ✅ Emitir receitas veterinárias
- ✅ Iniciar e finalizar atendimentos
- ❌ Não pode acessar painéis administrativos
- ❌ Não pode gerenciar usuários

---

## 👔 Gerente

**URL de Acesso:** http://localhost:8000/painel-funcionario/

**Credenciais de Teste:**
- **Matrícula:** 150001
- **Senha:** Pet@150001
- **Email:** gerente@petshop.com
- **Tipo:** GERENTE

**Permissões:**
- ✅ Acesso ao painel de funcionário
- ✅ Cadastrar e gerenciar clientes
- ✅ Cadastrar pets para clientes
- ✅ Visualizar lista completa de clientes e pets
- ✅ Consultar produtos da loja
- ❌ Não pode acessar painel administrativo (staff)

---

## 🔍 Supervisor

**URL de Acesso:** http://localhost:8000/painel-funcionario/

**Credenciais de Teste:**
- **Matrícula:** 200001
- **Senha:** Pet@200001
- **Email:** supervisor@petshop.com
- **Tipo:** SUPERVISOR

**Permissões:** (Mesmas do Gerente)
- ✅ Acesso ao painel de funcionário
- ✅ Cadastrar e gerenciar clientes
- ✅ Cadastrar pets para clientes
- ✅ Visualizar lista completa de clientes e pets

---

## 👨‍💼 Funcionário

**URL de Acesso:** http://localhost:8000/painel-funcionario/

**Credenciais de Teste:**
- **Matrícula:** 250001
- **Senha:** Pet@250001
- **Email:** funcionario@petshop.com
- **Tipo:** FUNCIONARIO

**Permissões:**
- ✅ Acesso ao painel de funcionário
- ✅ Cadastrar clientes (CPF obrigatório)
- ✅ Cadastrar pets vinculados a clientes
- ✅ Editar dados de clientes existentes
- ✅ Adicionar novos pets a clientes
- ✅ Visualizar lista de todos os clientes
- ✅ Consultar produtos disponíveis
- ❌ Não pode acessar painéis administrativos
- ❌ Não pode gerenciar tipos de animais ou raças

---

## 👨‍💻 Administrador (Staff)

**URL de Acesso:** http://localhost:8000/painel-admin/

**Credenciais:**
- **Username:** admin
- **Senha:** admin123
- **Email:** admin@petshop.com
- **Tipo:** ADMIN (is_staff=True)

**Permissões:**
- ✅ Acesso total ao sistema
- ✅ Criar funcionários com matrícula
- ✅ Gerenciar todos os usuários
- ✅ Gerenciar tipos de animais e raças
- ✅ Visualizar todos os pets cadastrados
- ✅ Acesso ao Django Admin (/admin/)

---

## 👤 Cliente (Público)

**Credenciais de Teste:**
- **Username:** cliente1
- **Senha:** senha123
- **Email:** cliente@example.com
- **Tipo:** CLIENTE

**Como criar conta:**
1. Acesse: http://localhost:8000/users/signup/
2. Preencha: Nome de usuário, Email, Senha
3. Ou use "Continuar com Google"

**Após cadastro:**
- Aparece automaticamente no painel do funcionário
- Funcionário pode complementar dados (CPF, telefone)
- Funcionário pode adicionar pets ao cliente

---

## 🏠 URLs Principais

**Acesso Geral:**
- **Página Inicial:** http://localhost:8000/
- **Login:** http://localhost:8000/users/login/
- **Cadastro Público:** http://localhost:8000/users/signup/

**Painéis:**
- **Admin:** http://localhost:8000/painel-admin/
- **Funcionário:** http://localhost:8000/painel-funcionario/
- **Veterinário:** http://localhost:8000/painel-veterinario/

**Django Admin:**
- http://localhost:8000/admin/

---

## 🧪 Como Testar os Painéis

### **Painel Funcionário:**
1. Acesse: http://localhost:8000/users/login/
2. Digite **Matrícula:** 250001 e **Senha:** Pet@250001
3. Será redirecionado para: http://localhost:8000/painel-funcionario/
4. Teste: Cadastrar cliente, adicionar pets, visualizar lista

### **Painel Veterinário:**
1. Faça logout se estiver logado
2. Login com **Matrícula:** 100001 e **Senha:** Pet@100001
3. Será redirecionado para: http://localhost:8000/painel-veterinario/
4. Teste: Ver consultas, criar prontuários, emitir receitas

### **Painel Admin:**
1. Faça logout
2. Login com **Username:** admin e **Senha:** admin123
3. Será redirecionado para: http://localhost:8000/painel-admin/
4. Teste: Criar funcionário, gerenciar tipos de animais, ver todos os pets

---

## 📝 Criar Novo Funcionário (Via Admin)

**Pelo Painel Admin:**
1. Login como admin
2. Acesse: http://localhost:8000/painel-admin/usuarios/novo/
3. Preencha:
   - **Matrícula:** 6 dígitos (ex: 250002 para funcionário)
   - **Tipo:** Selecione o tipo desejado
   - **Nome/Sobrenome/Email/Telefone**
   - Para veterinário: preencha CRMV e Especialidade
4. A senha padrão será: `Pet@{matrícula}`
5. Informe ao funcionário: Matrícula e Senha gerada

**Via Django Shell:**
```bash
docker-compose exec web python manage.py shell
```

```python
from users.models import User

# Criar Veterinário
vet = User.objects.create_user(
    username='100002',  # Matrícula como username
    email='vet2@petshop.com',
    password='Pet@100002',
    user_type=User.VETERINARIO,
    matricula='100002',
    first_name='Dr. João',
    last_name='Silva',
    crmv='CRMV/SP 12345',
    especialidade='Clínica Geral'
)

# Criar Funcionário
func = User.objects.create_user(
    username='250002',
    email='func2@petshop.com',
    password='Pet@250002',
    user_type=User.FUNCIONARIO,
    matricula='250002',
    first_name='Maria',
    last_name='Santos'
)

print(f"Criados: {vet.username} e {func.username}")
```

---

## 🔐 Sistema de Autenticação

**Login aceita:**
- Username (ex: admin, cliente1)
- Email (ex: admin@petshop.com)
- Matrícula (ex: 250001) ← **Usado por funcionários**

**Redirecionamento automático após login:**
- Admin (is_staff) → `/painel-admin/`
- Veterinário → `/painel-veterinario/`
- Funcionário/Supervisor/Gerente → `/painel-funcionario/`
- Cliente → `/` (home)

---

**Última atualização:** 02/12/2025
