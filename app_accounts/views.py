from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .models import User
# Create your views here.

def login(request):
    return render(request, 'accounts/login.html')


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

@login_required
class delete(View):
    def post(self, request):
        # 계정 정보 삭제 후 로그아웃
        request.user.delete()
        auth_logout(request)
        return redirect('planet:main')
    
@login_required
class logout(View):
    def post(self, request):
        auth_logout(request)
        return redirect('planet:main')