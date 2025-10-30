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
    
    Validação extra: Detecta se o email já está sendo usado por uma
    conta Google e sugere definir senha nessa conta existente.
    """
    error_message = None
    
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        # Validações
        if not username or not email or not password:
            error_message = "❌ Todos os campos são obrigatórios."
        
        elif len(username) < 3:
            error_message = "❌ Nome de usuário deve ter pelo menos 3 caracteres."
        
        elif len(username) > 30:
            error_message = "❌ Nome de usuário não pode ter mais de 30 caracteres."
        
        elif not username.replace('_', '').replace('-', '').isalnum():
            error_message = "❌ Nome de usuário pode conter apenas letras, números, hífen e underscore."
        
        elif '@' not in email:
            error_message = "❌ Email inválido. Verifique o formato."
        
        elif len(password) < 8:
            error_message = "❌ A senha deve ter pelo menos 8 caracteres."
        
        elif len(password) > 128:
            error_message = "❌ A senha não pode ter mais de 128 caracteres."
        
        elif User.objects.filter(username=username).exists():
            error_message = "❌ Este nome de usuário já está em uso. Tente outro."
        
        elif User.objects.filter(email=email).exists():
            # Verifica se é uma conta do Google sem senha
            existing_user = User.objects.get(email=email)
            if not existing_user.has_usable_password():
                error_message = (
                    "⚠️ Este email já está cadastrado via Google. "
                    "Faça login com o Google e defina uma senha na sua conta para poder usar também o login tradicional."
                )
            else:
                error_message = "❌ Este email já está cadastrado. Use outro email ou tente fazer login."

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
    
    Validação extra: Detecta usuários criados pelo Google que ainda
    não definiram senha e exibe mensagem informativa.
    """
    if request.method == "POST":
        login_input = request.POST.get("login", "").strip()
        password = request.POST.get("password", "")

        error_message = None

        if not login_input or not password:
            error_message = "❌ Usuário/Email e senha são obrigatórios."
        
        elif len(login_input) < 3:
            error_message = "❌ Usuário/Email inválido."
        
        else:
            # Tenta autenticar com username primeiro
            user = authenticate(request, username=login_input, password=password)
            
            # Se falhar, tenta com email
            if not user:
                try:
                    user_obj = User.objects.get(email=login_input)
                    
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
                
                except User.DoesNotExist:
                    user = None
                    error_message = "❌ Usuário/Email não encontrado. Verifique ou crie uma nova conta."
            
            elif not user:
                error_message = "❌ Senha incorreta. Verifique e tente novamente."
                    
            if user:
                login(request, user)
                return redirect('home')
            elif not error_message:
                error_message = "❌ Falha ao autenticar. Tente novamente."
        
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
