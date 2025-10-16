from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .models import User

# Create your views here.

def home(request):
    return render(request, 'home.html')

def create_user(request):
    error_message = None  # Inicializar antes do if
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not username or not email or not password:
            error_message = "Todos os campos são obrigatórios."
        elif len(password) < 8:
            error_message = "A senha deve ter pelo menos 8 caracteres."
        
        if error_message is None:
            user = User(username=username, email=email)
            user.set_password(password)  # Criptografa a senha corretamente
            user.save()
            return render(request, "account/login.html", {"user": user})
    return render(request, "account/signUp.html", {"error": error_message} if error_message else {})

def list_users(request):
    users = User.objects.all()
    return render(request, "users/list_users.html", {"users": users})

def update_user(request, user_id):
    user = User.objects.get(id=user_id)
    error_message = None  # Inicializar antes do if

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not username or not email or not password:
            error_message = "Todos os campos são obrigatórios."
        elif len(password) < 8:
            error_message = "A senha deve ter pelo menos 8 caracteres."

        if error_message is None:
            user.username = username
            user.email = email
            user.set_password(password)  # Criptografa a senha corretamente
            user.save()
            return render(request, "users/home.html", {"user": user})

    return render(request, "users/update_user.html", {"user": user, "error": error_message})

def delete_user(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == "POST":
        user.delete()
        users = User.objects.all()
        return render(request, "users/list_users.html", {"users": users})

    return render(request, "users/delete_user.html", {"user": user})

def user_login(request):
    if request.method == "POST":
        login_input = request.POST.get("login")
        password = request.POST.get("password")

        error_message = None

        if not login_input or not password:
            error_message = "Todos os campos são obrigatórios."
        else:
            # o authenticate serve para verificar se o usuário existe
            user = authenticate(request, username=login_input, password=password) 
            if not user:
                try:
                    user_obj = User.objects.get(email=login_input)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            if user:
                login(request, user) # cria a sessão do usuário
                return render(request, "home.html", {"user": user})
            else:
                error_message = "Credenciais inválidas."
            
        return render(request, "account/login.html", {"error": error_message} if error_message else {})

    return render(request, "account/login.html")