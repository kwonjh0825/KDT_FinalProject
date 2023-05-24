from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Planet, TermsOfService, Post, Emote
from .forms import PlanetForm, PostForm
from app_accounts.models import Accountsbyplanet
from app_accounts.forms import AccountsbyplanetForm

EMOTIONS = [
    {'label': '좋아요', 'value': 1},
    {'label': '재밌어요', 'value': 2},
    {'label': '싫어요', 'value': 3},
]

# 사이트 첫 페이지
def main(request):
    return render(request, 'planets/main.html')


# 행성 리스트 페이지
def planet_list(request):
    planets = Planet.objects.filter(is_public='Public')
    context = {
        'planets':planets
    }
    return render(request, 'planets/planet_list.html', context)


# 행성 생성 페이지
@login_required
def planet_create(request):
    if request.method == 'POST':
        form = PlanetForm(request.POST, request.FILES)
        if form.is_valid():
            planet = form.save(commit=False)
            planet.created_by = request.user
            planet.save()

            termsofservice_count = int(request.POST.get('termsofservice_count', 0))

            # 이용 약관 저장
            for i in range(1, termsofservice_count + 1):
                term_content = request.POST.get(f'term_content_{i}', '')

                # 이용 약관 DB Create
                TermsOfService.objects.create(Planet=planet, order=i, content=term_content)

            return redirect('planets:planet_join', planet.name)
    else:
        form = PlanetForm()
    context = {
        'form': form,
    }
    return render(request, 'planets/planet_create.html', context)


# 행성 가입
@login_required
def planet_join(request, planet_name):
    planet = Planet.objects.get(name=planet_name)

    # 이미 행성에 계정이 있는 경우
    if Accountsbyplanet.objects.filter(planet=planet, user=request.user).exists():
        return redirect('planets:index', planet_name)
    
    termsofservice = TermsOfService.objects.filter(Planet_id=planet.pk)

    if request.method == 'POST':
        form = AccountsbyplanetForm(request.POST, request.FILES)
        if form.is_valid():
            accountsbyplanet = form.save(commit=False)
            accountsbyplanet.planet = planet
            accountsbyplanet.user = request.user
            accountsbyplanet.save()
            return redirect('planets:index', planet_name)
    else:
        form = AccountsbyplanetForm()

    context = {
        'form': form,
        'termsofservice': termsofservice,
        'planet': planet,
    }
    return render(request, 'planets/planet_join.html', context)


# 행성 페이지
def index(request, planet_name):
    planet = Planet.objects.get(name=planet_name)

    # 행성에 계정이 없는 경우
    if not request.user.is_authenticated or not Accountsbyplanet.objects.filter(planet=planet, user=request.user).exists():
        return redirect('planets:main')
    
    posts = Post.objects.filter(planet=planet).order_by('-pk')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.accountbyplanet = Accountsbyplanet.objects.get(planet=planet, user=request.user)
            post.planet = planet
            post.save()
            return redirect('planets:index', planet_name)
    else:
        form = PostForm()

    context = {
        'form': form,
        'planet': planet,
        'posts': posts,
    }
    return render(request, 'planets/index.html', context)


# 행성 삭제
@login_required
def planet_delete(request, planet_name):
    planet = Planet.objects.get(name=planet_name)
    if planet.created_by == request.user:
        planet.delete()
    return redirect('planets:main')


# 게시글 삭제
@login_required
def post_delete(request, planet_name, post_pk):
    post = Post.objects.get(pk=post_pk)
    planet = Planet.objects.get(name=planet_name)
    if Accountsbyplanet.objects.get(user=request.user.pk, planet=planet) == post.accountbyplanet:
        post.delete()
    return redirect('planets:index', planet_name)

# 행성 관리 페이지
@login_required
def planet_admin(request, planet_name):
    planet = Planet.objects.get(name=planet_name)
    # tos = TermsOfServices.objects.filter(Planet_id=planet.pk)
    if request.method == 'POST':
        form_planet = PlanetForm(request.POST, instance=planet)
        
        if form_planet.is_valid():
            form_planet.save()
            
            return redirect('planets:main')
    else:
        form_planet = PlanetForm(instance=planet)
    
    context = {
        'form_planet': form_planet, 
        'planet': planet,
    }
    return render(request, 'planets/planet_admin.html', context)

# 행성 약관 관리 페이지
@login_required
def planet_tos_admin(request, planet_name):
    planet = Planet.objects.get(name=planet_name)
    TOSs = TermsOfService.objects.filter(Planet_id=planet.pk)
    length = TOSs.count()
    if request.method == 'POST':
        termsofservice_count = int(request.POST.get('termsofservice_count', 0))
        # 기존 약관 DB 삭제
        old_term = TermsOfService.objects.filter(Planet=planet)
        old_term.delete()
        
        # 이용 약관 저장
        for i in range(1, termsofservice_count + 1):
            term_content = request.POST.get(f'term_content_{i}', '')
            TermsOfService.objects.create(Planet=planet, order=i, content=term_content)

        return redirect('planets:main')
    
    else:
        context = {
            'planet': planet,
            'TOSs': TOSs,
            'length': length,
        }
        return render(request, 'planets/planet_tos_admin.html', context)