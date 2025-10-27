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

User = get_user_model()


def create_user(request):
    """
    Cadastra um novo usuário no sistema.
    Valida username único, email único e senha com mínimo de 8 caracteres.
    """
    error_message = None
    
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Validações
        if not username or not email or not password:
            error_message = "Todos os campos são obrigatórios."
        elif len(password) < 8:
            error_message = "A senha deve ter pelo menos 8 caracteres."
        elif User.objects.filter(username=username).exists():
            error_message = "Nome de usuário já existe."
        elif User.objects.filter(email=email).exists():
            error_message = "Email já cadastrado."

        if error_message is None:
            user = User(username=username, email=email)
            user.set_password(password)  # Criptografa a senha
            user.save()
            return redirect('local_login')  # Redireciona para login após cadastro
            
    return render(request, "account/signup.html", {"error": error_message})


def user_login(request):
    """
    Autentica usuário usando username OU email + senha.
    Permite login com qualquer um dos dois identificadores.
    """
    if request.method == "POST":
        login_input = request.POST.get("login")
        password = request.POST.get("password")

        error_message = None

        if not login_input or not password:
            error_message = "Todos os campos são obrigatórios."
        else:
            # Tenta autenticar com username primeiro
            user = authenticate(request, username=login_input, password=password)
            
            # Se falhar, tenta com email
            if not user:
                try:
                    user_obj = User.objects.get(email=login_input)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
                    
            if user:
                login(request, user)
                return redirect('home')
            else:
                error_message = "Credenciais inválidas."
        
        return render(request, "account/login.html", {"error": error_message})

    return render(request, "account/login.html")


def user_logout(request):
    """
    Encerra a sessão do usuário.
    """
    logout(request)
    return redirect('home')


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
