from django.shortcuts import render
from .models import User

# Create your views here.


def create_user(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        error_message = None

        if not username or not email or not password:
            error_message = "Todos os campos são obrigatórios."
        elif len(password) < 8:
            error_message = "A senha deve ter pelo menos 8 caracteres."
        
        if error_message is None:
            user = User(username = username, email = email, password = password)
            user.save()
            return render(request, "users/home.html", {"user": user})
    return render(request, "users/create_user.html", {"error": error_message} if error_message else {})

def list_users(request):
    
    users = User.objects.all()
    return render(request, "users/list_users.html", {"users": users})

def update_user(request, user_id):

      user = User.objects.get(id = user_id)

      if request.method == "POST":

            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            error_message = None

            if not username or not email or not password:
                error_message = "Todos os campos são obrigatórios."
            elif len(password) < 8:
                error_message = "A senha deve ter pelo menos 8 caracteres."

            if error_message is None:
                user.username = username
                user.email = email
                user.password = password
                user.save()
                return render(request, "users/home.html", {"user": user})

    return render(request, "users/update_user.html", {"user": user, "error": error_message})

def delete_user(request, user_id):

        user = User.objects.get(id = user_id)
    
        if request.method == "POST":
                user.delete()
                users = User.objects.all()
                return render(request, "users/list_users.html", {"users": users})
    
        return render(request, "users/delete_user.html", {"user": user})