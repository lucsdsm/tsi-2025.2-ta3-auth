# 🔐 Sistema de Matrícula para Funcionários - PetShop

## 📋 Visão Geral

O sistema agora utiliza um esquema de **matrícula** para identificação de funcionários, supervisores, gerentes e veterinários. Apenas o **administrador** pode criar e gerenciar esses acessos, garantindo controle total sobre a equipe.

## 🎯 Mudanças Implementadas

### ✅ O que mudou:

1. **Cadastro Público** → Apenas para CLIENTES
2. **Cadastro de Funcionários** → Apenas pelo ADMINISTRADOR
3. **Sistema de Matrícula** → Identificação única com prefixos
4. **Senha Padrão** → Gerada automaticamente pelo sistema
5. **Novos Tipos de Usuário** → GERENTE e SUPERVISOR

## 👥 Tipos de Usuário e Prefixos de Matrícula

### Hierarquia do Sistema:

| Tipo | Prefixo | Formato | Exemplo | Criado Por |
|------|---------|---------|---------|------------|
| 👑 **Administrador** | - | - | admin | Sistema |
| 🩺 **Veterinário** | `10` | 10XXXX | 100001 | Admin |
| 💼 **Gerente** | `15` | 15XXXX | 150001 | Admin |
| 📋 **Supervisor** | `20` | 20XXXX | 200001 | Admin |
| 👔 **Funcionário** | `25` | 25XXXX | 250001 | Admin |
| 👤 **Cliente** | - | username | cliente123 | Auto-cadastro |

### Regras de Matrícula:

- **6 dígitos** obrigatórios
- **2 primeiros dígitos** = Prefixo (tipo de funcionário)
- **4 últimos dígitos** = Sequencial definido pelo admin
- **Único** no sistema (não pode repetir)
- **Imutável** após criação

## 🔑 Sistema de Senhas

### Senha Padrão Gerada Automaticamente:

**Formato:** `Pet@{matrícula}`

**Exemplos:**
```
Matrícula 100001 → Senha: Pet@100001
Matrícula 150001 → Senha: Pet@150001
Matrícula 200001 → Senha: Pet@200001
Matrícula 250001 → Senha: Pet@250001
```

### ⚠️ Importante:
- O admin recebe a senha após criar o funcionário
- Deve informar ao funcionário para o primeiro acesso
- Funcionário pode trocar a senha posteriormente (recomendado)

## 🔐 Como o Administrador Cria Funcionários

### Passo a Passo:

1. **Acesse o Painel Administrativo**
   ```
   URL: http://localhost:8000/painel-admin/
   Login: admin / senha_admin
   ```

2. **Vá para "Usuários"**
   ```
   Menu lateral → Gerenciamento → Usuários
   Ou diretamente: http://localhost:8000/painel-admin/usuarios/
   ```

3. **Clique em "➕ Novo Usuário"**

4. **Preencha o Formulário:**

   #### Campos Obrigatórios:
   
   **Matrícula** (6 dígitos)
   ```
   Veterinário → Comece com 10 (ex: 100001, 100002)
   Gerente     → Comece com 15 (ex: 150001, 150002)
   Supervisor  → Comece com 20 (ex: 200001, 200002)
   Funcionário → Comece com 25 (ex: 250001, 250002)
   ```
   
   **Tipo de Funcionário**
   - Selecione o cargo apropriado
   
   **Nome e Sobrenome**
   - Nome completo do funcionário
   
   **E-mail**
   - E-mail corporativo ou pessoal
   
   #### Campos Opcionais:
   
   **Telefone**
   - Contato do funcionário
   
   **CRMV** (Obrigatório apenas para Veterinários)
   - Número do Conselho Regional de Medicina Veterinária
   
   **Especialidade** (Obrigatório apenas para Veterinários)
   - Ex: Clínica Geral, Cirurgia, Dermatologia

5. **Clique em "Salvar"**

6. **Anote as Credenciais Geradas:**
   ```
   ✅ Funcionário 'João Silva' criado com sucesso!
   Matrícula: 250001
   Senha padrão: Pet@250001
   Informe estes dados ao funcionário para o primeiro acesso.
   ```

7. **Repasse as Credenciais ao Funcionário**

## 🔓 Como Funcionários Fazem Login

### Primeira vez:

1. Acesse: `http://localhost:8000/users/local/login/`

2. Faça login com:
   - **Login:** Digite sua matrícula (ex: `250001`)
   - **Senha:** Senha padrão fornecida pelo admin (ex: `Pet@250001`)

3. Você será redirecionado automaticamente para seu painel:
   - **Veterinário** → Painel Veterinário
   - **Gerente/Supervisor/Funcionário** → Painel do Funcionário

### Opções de Login:

O sistema aceita login com:
- ✅ **Matrícula** (ex: 250001)
- ✅ **E-mail** (ex: funcionario@petshop.com)  
- ✅ **Username** (gerado automaticamente = matrícula)

## 🚫 Restrições de Segurança

### O que NÃO é mais permitido:

❌ **Funcionários não podem se cadastrar publicamente**
- O formulário público agora é exclusivo para CLIENTES
- Apenas o admin cria contas de funcionários

❌ **Clientes não podem escolher tipo de usuário**
- Cadastro público sempre cria usuário tipo CLIENTE
- Não há opção de selecionar FUNCIONARIO, VETERINARIO, etc.

❌ **Matrícula não pode ser alterada**
- Após criação, a matrícula é permanente
- Evita conflitos e mantém histórico

❌ **Username não é editável**
- Username = Matrícula (gerado automaticamente)
- Garante unicidade e facilita identificação

## 📝 Exemplos Práticos

### Exemplo 1: Criar Veterinário

```
Matrícula: 100001
Tipo: Veterinário
Nome: Dr. Carlos
Sobrenome: Mendes
E-mail: carlos.mendes@petshop.com
Telefone: (11) 98765-4321
CRMV: CRMV-SP 12345
Especialidade: Ortopedia

→ Resultado:
   Username: 100001
   Senha: Pet@100001
```

### Exemplo 2: Criar Gerente

```
Matrícula: 150001
Tipo: Gerente
Nome: Maria
Sobrenome: Santos
E-mail: maria.santos@petshop.com
Telefone: (11) 98765-1234

→ Resultado:
   Username: 150001
   Senha: Pet@150001
```

### Exemplo 3: Criar Supervisor

```
Matrícula: 200001
Tipo: Supervisor
Nome: João
Sobrenome: Oliveira
E-mail: joao.oliveira@petshop.com

→ Resultado:
   Username: 200001
   Senha: Pet@200001
```

### Exemplo 4: Criar Funcionário

```
Matrícula: 250001
Tipo: Funcionário
Nome: Ana
Sobrenome: Costa
E-mail: ana.costa@petshop.com

→ Resultado:
   Username: 250001
   Senha: Pet@250001
```

## 🔧 Gestão de Funcionários pelo Admin

### Visualizar Funcionários

Na listagem, agora você vê:
- **Nome completo** (ao invés de username)
- **Matrícula** (identificação única)
- **Tipo com badge colorido**:
  - 🩺 Veterinário (azul claro)
  - 💼 Gerente (amarelo)
  - 📋 Supervisor (azul)
  - 👔 Funcionário (laranja)
  - 👤 Cliente (ciano)

### Editar Funcionário

Permite alterar:
- ✅ Nome e sobrenome
- ✅ E-mail
- ✅ Telefone
- ✅ CRMV e especialidade (veterinários)
- ✅ Status (ativo/inativo)
- ❌ Matrícula (bloqueada)
- ❌ Username (bloqueado)

### Ativar/Desativar

- **Desativar:** Funcionário não consegue mais fazer login
- **Ativar:** Restaura acesso do funcionário
- **Proteção:** Admin não pode desativar a própria conta

### Filtros Disponíveis

- 🔍 **Busca:** Nome, email, matrícula, CRMV
- 📊 **Status:** Ativo / Inativo / Todos
- 👥 **Tipo:** Veterinário, Gerente, Supervisor, Funcionário, Cliente

## 🎓 Boas Práticas

### Para Administradores:

1. **Organize as Matrículas**
   ```
   Veterinários:  100001, 100002, 100003...
   Gerentes:      150001, 150002, 150003...
   Supervisores:  200001, 200002, 200003...
   Funcionários:  250001, 250002, 250003...
   ```

2. **Mantenha um Registro**
   - Anote as matrículas e senhas geradas
   - Use uma planilha de controle (Excel, Google Sheets)

3. **Oriente os Funcionários**
   - Informe sobre a senha padrão
   - Incentive a troca de senha no primeiro acesso
   - Explique o uso da matrícula para login

4. **Revise Periodicamente**
   - Desative funcionários que saíram da empresa
   - Verifique contas inativas
   - Atualize informações de contato

### Para Funcionários:

1. **Primeiro Acesso**
   - Use a matrícula fornecida pelo admin
   - Entre com a senha padrão (Pet@matrícula)
   - Considere trocar a senha imediatamente

2. **Login Diário**
   - Pode usar matrícula ou e-mail
   - Guarde suas credenciais em local seguro

3. **Esqueceu a Senha?**
   - Contate o administrador
   - Ele pode redefinir para a senha padrão

## 🔄 Migração de Usuários Antigos

### Funcionários Criados Antes do Sistema de Matrícula:

Os usuários antigos **não têm matrícula** e continuam funcionando normalmente:
- ✅ Podem fazer login com username
- ✅ Podem fazer login com email
- ⚠️ Não têm matrícula (campo vazio)
- ℹ️ Admin pode adicionar matrícula ao editar (se necessário)

### Como Adicionar Matrícula a Usuário Antigo:

1. Vá em Usuários → Editar o funcionário
2. Preencha o campo "Matrícula" seguindo as regras
3. Valide se o prefixo está correto para o tipo
4. Salve

## 🧪 Testando o Sistema

### Via Django Shell:

```bash
docker-compose exec web python manage.py shell
```

```python
from users.models import User

# Criar veterinário com matrícula
vet = User.objects.create_user(
    username='100001',
    matricula='100001',
    email='vet@test.com',
    password=User.gerar_senha_padrao('100001'),
    user_type=User.VETERINARIO,
    first_name='Dr. Teste',
    last_name='Silva',
    crmv='CRMV-SP 99999',
    especialidade='Clínica Geral'
)
print(f"Veterinário criado: {vet}")
print(f"Senha padrão: {User.gerar_senha_padrao('100001')}")

# Criar funcionário com matrícula
func = User.objects.create_user(
    username='250001',
    matricula='250001',
    email='func@test.com',
    password=User.gerar_senha_padrao('250001'),
    user_type=User.FUNCIONARIO,
    first_name='João',
    last_name='Santos'
)
print(f"Funcionário criado: {func}")
print(f"Senha padrão: {User.gerar_senha_padrao('250001')}")

# Validar matrícula
is_valid, msg = User.validar_matricula('100001', User.VETERINARIO)
print(f"Validação: {is_valid} - {msg}")

is_valid, msg = User.validar_matricula('250001', User.FUNCIONARIO)
print(f"Validação: {is_valid} - {msg}")
```

## 📊 Estrutura Técnica

### Modelo User Atualizado:

```python
class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('CLIENTE', 'Cliente'),
        ('FUNCIONARIO', 'Funcionário'),
        ('SUPERVISOR', 'Supervisor'),
        ('GERENTE', 'Gerente'),
        ('VETERINARIO', 'Veterinário'),
    ]
    
    MATRICULA_PREFIXES = {
        'VETERINARIO': '10',
        'GERENTE': '15',
        'SUPERVISOR': '20',
        'FUNCIONARIO': '25',
    }
    
    matricula = CharField(max_length=6, unique=True, blank=True, null=True)
    
    @staticmethod
    def gerar_senha_padrao(matricula):
        return f"Pet@{matricula}"
    
    @classmethod
    def validar_matricula(cls, matricula, user_type):
        # Valida formato e prefixo
        ...
```

### Formulários:

- **FuncionarioCreateForm** → Para admin criar funcionários
- **ClientePublicCreateForm** → Para cadastro público de clientes

## 🐛 Troubleshooting

### Erro: "Matrícula deve começar com XX"

**Causa:** Prefixo incorreto para o tipo selecionado

**Solução:** Verifique a tabela de prefixos:
- Veterinário: 10
- Gerente: 15
- Supervisor: 20
- Funcionário: 25

### Erro: "Esta matrícula já está em uso"

**Causa:** Matrícula duplicada

**Solução:** Escolha outro número sequencial (ex: 250002, 250003)

### Erro: "CRMV é obrigatório para Veterinários"

**Causa:** Campo CRMV vazio ao criar veterinário

**Solução:** Preencha os campos CRMV e Especialidade

### Login não funciona com matrícula

**Causa:** Usuário pode não ter matrícula (criado antes do sistema)

**Solução:** Use email ou username, ou peça ao admin para adicionar matrícula

## 📚 Documentação Adicional

- **CREDENCIAIS.md** → Credenciais de teste do sistema
- **PAINEL_FUNCIONARIO.md** → Documentação do painel do funcionário
- **README.md** → Documentação geral do projeto

---

**Versão:** 2.0  
**Última atualização:** 29/11/2025  
**Desenvolvido por:** Equipe PetShop  
**Sistema de Matrícula:** Implementado
