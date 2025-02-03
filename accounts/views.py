from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect

User = get_user_model()

def signup(request):
    if request.method == "POST":
        # Traiter formulaire
        username = request.POST.get("username")
        password = request.POST.get("password")
        # create the user with all given infos
        user = User.objects.create_user(username=username, password=password)
        # connect user
        login(request, user)
        # redirect to home after signup
        return redirect('index')

    return render(request, 'accounts/signup.html')