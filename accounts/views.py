from django.contrib.auth import get_user_model, login, logout, authenticate
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

def login_user(request):
    if request.method == "POST":
        #connect user
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password) #verifier si infos envoyées se trouvent dans la db
        if user:
            login(request, user)
            return redirect('index')

    return render(request, 'accounts/login.html')

def signout(request):
    logout(request)
    return redirect('index')

