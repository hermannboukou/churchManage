from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirige vers la page d'accueil si déjà connecté

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Remplacez 'home' par votre vue principale
        else:
            messages.error(request, "Identifiants incorrects. Veuillez réessayer.")

    return render(request, 'registration/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def configuration(request):
    return render(request, 'settings.html')
