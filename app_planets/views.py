from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count
from .models import Planet, TermsOfService, Post, Comment, Recomment, Emote, Report
from .forms import PlanetForm, PostForm, CommentForm, RecommentForm
from app_accounts.models import Accountbyplanet, User
from app_accounts.forms import AccountbyplanetForm

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

            # guide accountbyplanet 생성
            accountbyplanet = Accountbyplanet.objects.create(nickname='Guide', user=User.objects.get(pk=1), planet=planet)

            # 게시글, 댓글, 대댓글 생성
            post = Post.objects.create(content='이곳은 게시글입니다. 꿈을 마음 껏 펼치세요!', planet=planet, accountbyplanet=accountbyplanet)
            comment = Comment.objects.create(content='이곳은 댓글입니다. 게시글에 대한 의견을 작성하세요!', post=post, accountbyplanet=accountbyplanet)
            Recomment.objects.create(content='이곳은 대댓글입니다. 댓글에 대한 생각을 알려주세요!', comment=comment, accountbyplanet=accountbyplanet)

            return redirect('planets:planet_join', planet.name)
    else:
        form = PlanetForm()
    context = {
        'form': form,
    }
    return render(request, 'planets/planet_create.html', context)

@login_required
def planet_contract(request,planet_name):
    planet = Planet.objects.get(name=planet_name)
    # 이미 행성에 계정이 있는 경우
    if Accountbyplanet.objects.filter(planet=planet, user=request.user).exists():
        return redirect('planets:index', planet_name)
    
    if Accountbyplanet.objects.filter(planet=planet).count() >= planet.maximum_capacity:
        messages.info(request, '서버 최대 인원을 초과하여 가입을 진행할 수 없습니다. ')
        return redirect('planets:main')
    
    termsofservice = TermsOfService.objects.filter(Planet_id=planet.pk)

    context = {
        'termsofservice': termsofservice,
        'planet': planet,

    }
    return render(request, 'planets/planet_contract.html', context )

# 행성 가입
@login_required
def planet_join(request, planet_name):
    planet = Planet.objects.get(name=planet_name)
    if request.method == 'POST':
        form = AccountbyplanetForm(request.POST, request.FILES)
        if form.is_valid():
            accountbyplanet = form.save(commit=False)
            accountbyplanet.planet = planet
            accountbyplanet.user = request.user
            
            # 관리자의 가입 승인이 필요 없는 경우
            if planet.need_confirm == False:
                accountbyplanet.is_confirmed = True
            
            accountbyplanet.save()
            return redirect('planets:index', planet_name)
    else:
        form = AccountbyplanetForm()

    context = {
        'form': form,
        'planet': planet,
    }
    return render(request, 'planets/planet_join.html', context)


# 행성 페이지
def index(request, planet_name):
    planet = Planet.objects.get(name=planet_name)

    # 행성에 계정이 없는 경우 또는 가입 승인 대기 중인 경우
    if not request.user.is_authenticated or not Accountbyplanet.objects.filter(planet=planet, user=request.user).exists() or Accountbyplanet.objects.get(planet=planet, user=request.user).is_confirmed == False: 
        return redirect('planets:main')
    
    postform = PostForm()
    commentform = CommentForm()
    recommentform = RecommentForm()

    context = {
        'postform': postform,
        'commentform': commentform,
        'recommentform': recommentform,
        'planet': planet,
        'first_post': Post.objects.filter(planet=planet).first(),
    }
    return render(request, 'planets/index.html', context)


# 행성 삭제
@login_required
def planet_delete(request, planet_name):
    planet = Planet.objects.get(name=planet_name)
    if planet.created_by == request.user:
        planet.delete()
    return redirect('planets:main')


# posts json
@login_required
def planet_posts(request, planet_name):
    posts = Post.objects.filter(planet=Planet.objects.get(name=planet_name)).order_by('-pk')
    per_page = 5
    page_number = request.GET.get('page')
    paginator = Paginator(posts, per_page)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    post_list = []
    for post in posts:
        post_list.append({
            'pk': post.pk,
            'content': post.content,
            'created_time': post.created_time,
            'nickname': post.accountbyplanet.nickname,
            'image_url': post.image.url if post.image else None,
            'user': post.accountbyplanet.user.username,
            'profile_image_url': post.accountbyplanet.profile_image.url if post.accountbyplanet.profile_image else None,
        })

    if posts.has_next():
        return JsonResponse(post_list, safe=False)
    else:
        post_list.append(None)
        return JsonResponse(post_list, safe=False)


# 게시글 생성
@require_POST
def post_create(request, planet_name):
    planet = Planet.objects.get(name=planet_name)
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.accountbyplanet = Accountbyplanet.objects.get(planet=planet, user=request.user)
        post.planet = planet
        post.save()
        form.save_m2m()
        response_data = {
            'success': True,
            'post_pk': post.pk,
            'content': post.content,
            'created_time': post.created_time,
            'nickname': post.accountbyplanet.nickname,
            'profile_image_url': post.accountbyplanet.profile_image.url,
            'image_url': post.image.url if post.image else None
        }
        return JsonResponse(response_data)
    else:
        errors = form.errors.as_json()
        return JsonResponse({'success': False, 'errors': errors})


# 게시글 삭제
@require_POST
def post_delete(request, planet_name, post_pk):
    post = Post.objects.get(pk=post_pk)
    planet = Planet.objects.get(name=planet_name)
    if Accountbyplanet.objects.get(user=request.user.pk, planet=planet) == post.accountbyplanet:
        post.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


# 댓글 생성
@require_POST
def comment_create(request, planet_name, post_pk):
    planet = Planet.objects.get(name=planet_name)
    post = Post.objects.get(pk=post_pk, planet=planet)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.accountbyplanet = Accountbyplanet.objects.get(planet=planet, user=request.user)
        comment.save()
        response_data = {
            'success': True,
            'comment_pk': comment.pk,
            'content': comment.content,
            'created_time': comment.created_time,
            'nickname': comment.accountbyplanet.nickname,
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'success': False, 'message': 'Form is invalid'})


# 댓글 삭제
@require_POST
def comment_delete(request, planet_name, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    planet = Planet.objects.get(name=planet_name)
    if Accountbyplanet.objects.get(user=request.user.pk, planet=planet) == comment.accountbyplanet:
        if Recomment.objects.filter(comment=comment).exists():
            comment.content = '이미 삭제된 댓글입니다.'
            comment.save()
            return JsonResponse({'success': 'Change', 'comment_content': comment.content})
        else:
            comment.delete()
            return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


# 대댓글 생성
@require_POST
def recomment_create(request, planet_name, post_pk, comment_pk):
    planet = Planet.objects.get(name=planet_name)
    post = Post.objects.get(pk=post_pk, planet=planet)
    comment = Comment.objects.get(pk=comment_pk, post=post)
    form = RecommentForm(request.POST)
    if form.is_valid():
        recomment = form.save(commit=False)
        recomment.comment = comment
        recomment.accountbyplanet = Accountbyplanet.objects.get(planet=planet, user=request.user)
        recomment.save()
        response_data = {
            'success': True,
            'recomment_pk': recomment.pk,
            'content': recomment.content,
            'created_time': recomment.created_time,
            'nickname': recomment.accountbyplanet.nickname,
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'success': False, 'message': 'Form is invalid'})


# 대댓글 삭제
@require_POST
def recomment_delete(request, planet_name, post_pk, comment_pk, recomment_pk):
    recomment = Recomment.objects.get(pk=recomment_pk)
    planet = Planet.objects.get(name=planet_name)
    if Accountbyplanet.objects.get(user=request.user.pk, planet=planet) == recomment.accountbyplanet:
        recomment.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


# 행성 관리 페이지
@login_required
def planet_admin(request, planet_name):
    planet = Planet.objects.get(name=planet_name)
    confirms = Accountbyplanet.objects.filter(planet=planet, is_confirmed=False)
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
        'confirms': confirms,
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

# 행성 가입 관리
@login_required
def planet_join_admin(request, planet_name):
    planet = Planet.objects.get(name=planet_name)
    confirms = Accountbyplanet.objects.filter(planet=planet, is_confirmed=False)

    context = {
        'planet': planet,
        'confirms': confirms,
    }
    return render(request, 'planets/planet_join_admin.html', context)

# 행성 가입 승인
@login_required
def planet_join_confirm(request, planet_name, user_pk):
    planet = Planet.objects.get(name=planet_name)
    user = User.objects.get(pk=user_pk)

    account = Accountbyplanet.objects.get(planet=planet, user=user)
    account.is_confirmed = True
    account.save()

    return JsonResponse({'success': True})

# 행성 가입 거절
@login_required
def planet_join_reject(request, planet_name, user_pk):
    planet = Planet.objects.get(name=planet_name)
    user = User.objects.get(pk=user_pk)
    
    account = Accountbyplanet.objects.get(planet=planet, user=user)
    account.delete()

    return JsonResponse({'success': True})    

# 게시글 신고 기능
def post_report(request, planet_name, post_pk):
    post = Post.objects.get(pk=post_pk)
    if not Report.objects.filter(user=request.user, post=post):
        Report.objects.create(user=request.user, post=post)
        messages.info(request, '신고가 완료되었습니다.')
    
    else:
        messages.info(request, '이미 신고한 게시글입니다. ')

    return redirect('planets:index', planet_name)

def admin_report(request, planet_name):
    planet = Planet.objects.get(name=planet_name)

    reports = Report.objects.values('post').annotate(Count('pk'))
    context = {
        'planet': planet,
        'reports': reports,
    }
    return render(request, 'planets/admin_report.html', context)