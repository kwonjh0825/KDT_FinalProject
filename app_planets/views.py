from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Planet, TermsOfServices
from .forms import PlanetForm

# 사이트 첫 페이지
def main(request):
    return render(request, 'planets/main.html')


# 행성 리스트 페이지
def planet_list(request):
    planets = Planet.objects.all()
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

            num_terms = int(request.POST.get('num_terms', 0))

            # 이용 약관 저장
            for i in range(1, num_terms + 1):
                term_content = request.POST.get(f'term_content_{i}', '')

                # 이용 약관 DB Create
                TermsOfServices.objects.create(Planet=planet, order=i, content=term_content)

            return redirect('planets:main')
    else:
        form = PlanetForm()
    context = {
        'form': form,
    }
    return render(request, 'planets/planet_create.html', context)


# 행성 가입 시 이용 약관 페이지
@login_required
def planet_join(request, planet_name):
    planet = Planet.objects.get(name=planet_name)
    termsofservices = TermsOfServices.objects.filter(Planet_id=planet.pk)
    context = {
        'termsofservices': termsofservices,
    }
    return render(request, 'planets/planet_join.html', context)

