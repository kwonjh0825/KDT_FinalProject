from django.shortcuts import render, redirect
from .forms import CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Accountsbyplanet, User
from app_planets.models import Planet
from .forms import AccountsbyplanetForm, CustomAutentication, CustomUserCreationForm, CustomSetPasswordForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.urls import reverse_lazy

# 이메일
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
# 비밀번호 리셋
from django.contrib.auth.views import PasswordResetConfirmView

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
            return redirect('accounts:profile', username=request.user)
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

# 아이디 찾기 
class find_id(View):
    def get(self, request):
        return render(request, 'accounts/find_id.html')

    def post(self, request):
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        try:
            # 입력받은 정보로 유저 검색
            user_found = User.objects.get(email=email, first_name=first_name, last_name=last_name)
            context = {
                'user_found': user_found,
            }
            # 일치하는 정보의 유저가 있다면 결과 페이지로 이동
            return render(request, 'accounts/find_id_result.html', context)
        
        except:
            # 일치하는 정보의 유저가 없으면 메시지 출력 후 다시 아이디를 찾을 수 있도록 함
            context = {
                'message': '일치하는 정보가 없습니다. '
            }
            return render(request, 'accounts/find_id.html', context)

# 계정 삭제
@login_required
def delete(request):
    # 계정 정보 삭제 후 로그아웃
    request.user.delete()
    auth_logout(request)
    return redirect('planets:main')

# 로그아웃
@login_required
def logout(request):
    auth_logout(request)
    return redirect('planets:main')

# 비밀번호 초기화 이메일 전송
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email'] # 폼에서 이메일 추출
            associated_users = get_user_model().objects.filter(email=data) # 유저 검색

            # 유재 존재 여부
            if associated_users.exists():                
                for user in associated_users:
                    subject = '[캣츠모스] 비밀번호 초기화' # 이메일 제목
                    email_template_name = "accounts/password_reset_email.txt" #이메일 내용
                    c = {
                        "email": user.email,
                        # local: '127.0.0.1:8000', prod: 'givwang.herokuapp.com'
                        'domain': '127.0.0.1:8000', #settings.HOSTNAME
                        'site_name': '캣츠모스',
                        # MTE4
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        # Return a token that can be used once to do a password reset for the given user.
                        'token': default_token_generator.make_token(user),
                        # local: http, prod: https
                        'protocol': 'http', #settings.PROTOCOL,
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("accounts:password_reset_done")
        
            else: # 유저가 존재 하지 않음
                messages.error(request, "존재하지 않는 이메일 주소입니다.")
                
    else:
        password_reset_form = PasswordResetForm()

    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name='accounts/password_reset.html',
        context={'password_reset_form': password_reset_form}
    )


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('planets:main')