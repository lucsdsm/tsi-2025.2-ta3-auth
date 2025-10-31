"""
Views principais da aplicação

Este arquivo contém apenas a view home.
As funcionalidades de autenticação estão em:
- users/auth/local/ - Autenticação local (CRUD usuários)
- users/auth/google/ - Autenticação Google OAuth2
"""

from django.shortcuts import render

def home(request):
    """Página inicial da aplicação"""
    context = {}
    
    # Se o usuário está autenticado, buscar seus pets
    if request.user.is_authenticated:
        from pets.models import Animal
        user_pets = Animal.objects.filter(proprietario=request.user, ativo=True)[:6]  # Limitar a 6 pets
        context['user_pets'] = user_pets
    
    return render(request, 'home.html', context)
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
    
    access_token = token_json.get('access_token')
    
    if not access_token:
        print('Erro: access_token não encontrado')
        return render(request, 'account/login.html', {'error': 'Erro ao obter token do Google.'})

    user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

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