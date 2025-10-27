from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User
import requests, os

def home(request):
    return render(request, 'home.html')

# Views para login local e CRUD de usuários

def create_user(request):
    error_message = None  # inicializar antes do if
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

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
            user.set_password(password)  # criptografa a senha
            user.save()
            return render(request, "account/login.html", {"user": user})
    return render(request, "account/signup.html", {"error": error_message} if error_message else {})

def list_users(request):
    users = User.objects.all()
    return render(request, "users/list_users.html", {"users": users})

def update_user(request, user_id):
    user = User.objects.get(id=user_id)
    error_message = None  # inicializar antes do if

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
            user.set_password(password)  # criptografa a senha corretamente
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

def user_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')

# Views para login via Google OAuth2
def google_login(request):
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    redirect_uri = 'https://zany-goggles-94w6qq9v55g2w55-8000.app.github.dev/users/google/callback/'
    scope = 'openid email profile'
    state = 'random_state_string'
    url = (
        f'https://accounts.google.com/o/oauth2/v2/auth'
        f'?client_id={client_id}'
        f'&redirect_uri={redirect_uri}'
        f'&response_type=code'
        f'&scope={scope}'
        f'&state={state}'
    )
    return redirect(url)

def google_callback(request):
    code = request.GET.get('code')
    if not code:
        return render(request, 'account/login.html', {'error': 'Erro no login com Google.'})

    token_url = 'https://oauth2.googleapis.com/token'
    redirect_uri = 'https://zany-goggles-94w6qq9v55g2w55-8000.app.github.dev/users/google/callback/'
    data = {
        'code': code,
        'client_id': os.getenv('GOOGLE_CLIENT_ID'),
        'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
    }
    token_response = requests.post(token_url, data=data)
    token_json = token_response.json()
    
    # Debug: imprimir resposta do token
    print('Token response:', token_json)
    
    access_token = token_json.get('access_token')
    
    if not access_token:
        print('Erro: access_token não encontrado')
        return render(request, 'account/login.html', {'error': 'Erro ao obter token do Google.'})

    user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()
    
    # Debug: imprimir informações do usuário
    print('User info:', user_info)

    email = user_info.get('email')
    first_name = user_info.get('given_name')
    last_name = user_info.get('family_name')

    if not email:
        return render(request, 'account/login.html', {'error': 'Não foi possível obter o e-mail do Google. Verifique as permissões.'})

    user, created = User.objects.get_or_create(email=email, defaults={
        'username': email.split('@')[0],
        'first_name': first_name,
        'last_name': last_name,
    })
    
    print(f'Usuario {"criado" if created else "encontrado"}: {user.username} ({user.email})')

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    
    print(f'Usuario autenticado: {request.user.is_authenticated}')
    
    return redirect('home')