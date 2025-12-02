"""
Módulo de Autenticação Local
===========================

Este módulo fornece autenticação tradicional com username/email e senha,
incluindo CRUD completo de usuários.

É totalmente independente e pode ser usado em qualquer projeto Django.

Funcionalidades:
- Cadastro de usuários
- Login com username ou email
- Logout
- Atualização de usuários
- Exclusão de usuários
- Listagem de usuários

Para usar em outro projeto:
1. Copie esta pasta 'local' para seu projeto
2. Configure as URLs no seu urls.py principal
3. Certifique-se de ter um modelo User (pode usar o padrão do Django)
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import rotate_token
from users.forms import ClientePublicCreateForm

User = get_user_model()


@ensure_csrf_cookie
def create_user(request):
    """
    Cadastra um novo cliente no sistema.
    Apenas clientes podem se cadastrar publicamente.
    Funcionários devem ser cadastrados pelo administrador.
    """
    if request.method == "POST":
        form = ClientePublicCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Cadastro realizado com sucesso! Faça login para continuar.")
            return redirect('local_login')
        # Se houver erros, o formulário será renderizado com os erros
    else:
        form = ClientePublicCreateForm()
    
    return render(request, "account/signup.html", {
        "form": form
    })


@ensure_csrf_cookie
def user_login(request):
    """
    Autentica usuário usando username, email OU matrícula + senha.
    Permite login com qualquer um dos três identificadores.
    """
    if request.method == "POST":
        login_input = request.POST.get("login", "").strip()
        password = request.POST.get("password", "")

        error_message = None

        if not login_input or not password:
            error_message = "❌ Usuário/Email/Matrícula e senha são obrigatórios."
        
        elif len(login_input) < 3:
            error_message = "❌ Usuário/Email/Matrícula inválido."
        
        else:
            # Tenta autenticar com username primeiro
            user = authenticate(request, username=login_input, password=password)
            
            # Se falhar, tenta com email ou matrícula
            if not user:
                try:
                    # Tenta buscar por email
                    user_obj = User.objects.filter(email=login_input).first()
                    
                    # Se não encontrar por email, tenta por matrícula
                    if not user_obj:
                        user_obj = User.objects.filter(matricula=login_input).first()
                    
                    if user_obj:
                        # Verifica se o usuário tem senha definida
                        if not user_obj.has_usable_password():
                            error_message = (
                                "⚠️ Esta conta foi criada com o Google e ainda não tem senha definida. "
                                "Faça login com o Google e crie uma senha, ou redefina sua senha para usar login tradicional."
                            )
                        else:
                            user = authenticate(request, username=user_obj.username, password=password)
                            if not user:
                                error_message = "❌ Senha incorreta. Verifique e tente novamente."
                    else:
                        error_message = "❌ Usuário/Email/Matrícula não encontrado. Verifique ou crie uma nova conta."
                
                except Exception as e:
                    user = None
                    error_message = "❌ Erro ao processar login. Tente novamente."
            
            if user:
                login(request, user)
                
                # Redireciona baseado no tipo de usuário
                if user.is_staff:
                    return redirect('panel:dashboard')
                elif user.is_veterinario():
                    return redirect('consultas:dashboard')
                elif user.is_funcionario() or user.is_supervisor() or user.is_gerente():
                    return redirect('painel_funcionario')
                else:
                    return redirect('home')
            elif not error_message:
                error_message = "❌ Falha ao autenticar. Tente novamente."
        
        return render(request, "account/login.html", {"error": error_message})

    # GET request - garante que sempre há um token CSRF fresco
    from django.middleware.csrf import get_token
    response = render(request, "account/login.html")
    
    # Força geração e envio do token CSRF
    token = get_token(request)
    response.set_cookie(
        'csrftoken',
        token,
        max_age=31449600,
        path='/',
        secure=False,
        httponly=False,
        samesite='Lax'
    )
    
    return response


@ensure_csrf_cookie
def user_logout(request):
    """
    Encerra a sessão do usuário e redireciona para login.
    Garante que um novo token CSRF seja gerado.
    """
    # Salva resposta de redirect
    response = redirect('local_login')
    
    # Faz logout
    logout(request)
    
    # DELETA o cookie CSRF antigo forçando criação de um novo
    response.delete_cookie('csrftoken', path='/', domain=None)
    
    # Rotaciona o token CSRF para garantir um token fresco
    rotate_token(request)
    
    messages.success(request, "✅ Você foi desconectado com sucesso.")
    return response


def list_users(request):
    """
    Lista todos os usuários cadastrados.
    Útil para administração.
    """
    users = User.objects.all()
    return render(request, "users/list_users.html", {"users": users})


def update_user(request, user_id):
    """
    Atualiza dados de um usuário existente.
    Permite alterar username, email e senha.
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('list_users')
        
    error_message = None

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not username or not email:
            error_message = "Username e email são obrigatórios."
        elif password and len(password) < 8:
            error_message = "A senha deve ter pelo menos 8 caracteres."

        if error_message is None:
            user.username = username
            user.email = email
            if password:  # Só atualiza senha se fornecida
                user.set_password(password)
            user.save()
            return redirect('list_users')

    return render(request, "users/update_user.html", {"user": user, "error": error_message})


def delete_user(request, user_id):
    """
    Exclui um usuário do sistema.
    Requer confirmação via POST.
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('list_users')

    if request.method == "POST":
        user.delete()
        return redirect('list_users')

    return render(request, "users/delete_user.html", {"user": user})
