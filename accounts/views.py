from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.contrib import messages

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
    if request.method == "POST":
        is_valid = authenticate(email=request.POST.get("email"), password=request.POST.get("password")) # 
        if is_valid:
            user = request.user
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.email = request.POST.get("email")
            user.save()
            messages.add_message(request, messages.SUCCESS, "Profil mis à jour avec succès")
        else:
            messages.add_message(request, messages.ERROR, "Le mot de passe est incorrect")

        return redirect('profile')

    form = UserForm(initial=model_to_dict(request.user, exclude=["password"])) # Form with user's infos as a dictionary
    
    addresses = request.user.addresses.all() # Get all shipping adresses for the user
    
    return render(request, 'accounts/profile.html', context={"form": form,
                                                             "addresses": addresses})