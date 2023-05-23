from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import CustomAutentication, CustomUserCreationForm

# Create your views here.

def login(request):
    if request.method == 'POST':
        form = CustomAutentication(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('planets:main')
    else:
        form = CustomAutentication()

    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('planets:main')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('planets:main')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

