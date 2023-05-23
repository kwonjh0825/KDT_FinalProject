from django.shortcuts import render, redirect
from .forms import CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Accountsbyplanet
from app_planets.models import Planet
from .forms import AccountsbyplanetForm

def login(request):
    return render(request, 'accounts/login.html')

# 최상위 프로필
def profile(request, username):
    User = get_user_model()
    user = User.objects.get(username=username)
    user_by_planets = Accountsbyplanet.objects.filter(user=user)

    context = {
        'user': user,
        # 유저가 속한 행성
        'user_by_planets':user_by_planets,
    }
    return render(request, 'accounts/profile.html', context)

# 최상위 프로필 업데이트
@login_required
def profile_update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile_update')
    else:
        form = CustomUserChangeForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)



# 행성별 프로필
def planet_profile(request, planet_name, user_pk):
    planet = Planet.objects.get(name=planet_name)
    user_by_planet = Accountsbyplanet.objects.filter(planet=planet, user=user_pk)

    context = {
        'user_by_planet':user_by_planet,
    }
    return render(request, 'accounts/planet_profile.html', context)

# 행성별 프로필 업데이트
@login_required
def planet_profile_update(request, planet_name, user_pk):
    planet = Planet.objects.get(name=planet_name)
    user_by_planet = Accountsbyplanet.objects.filter(planet=planet, user=user_pk)

    if user_by_planet.user == request.user:
        if request.method == 'POST':
            planet_user_update_form = AccountsbyplanetForm(request.POST, instance=user_by_planet)
            if planet_user_update_form.is_valid():
                planet_user_update_form.save()
                return redirect('accounts:planet_profile', planet_name, user_pk)
        else:
            planet_user_update_form = AccountsbyplanetForm(instance=user_by_planet)

    context = {
        'planet_user_update_form': planet_user_update_form,
    }
    return render(request, 'accounts/planet_update.html', context)