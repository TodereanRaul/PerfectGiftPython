from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.forms import UserForm

User = get_user_model()

def signup(request):
    if request.method == "POST":
        # Traiter formulaire
        email = request.POST.get("email")
        password = request.POST.get("password")
        # create the user with all given infos
        user = User.objects.create_user(email=email, password=password)
        # connect user
        login(request, user)
        # redirect to home after signup
        return redirect('index')

    return render(request, 'accounts/signup.html')

def login_user(request):
    if request.method == "POST":
        #connect user
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(email=email, password=password) #verifier si infos envoyées se trouvent dans la db
        if user:
            login(request, user)
            return redirect('index')

    return render(request, 'accounts/login.html')

def signout(request):
    logout(request)
    return redirect('index')

@login_required # Decorator to protect the view - user must be connected to access it
def profile(request):
    form = UserForm()
    return render(request, 'accounts/profile.html', context={"form": form})