import json
import secrets
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
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist # 예외처리
from django.db.models import Q


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
            planet                 = form.save(commit=False)
            planet.created_by      = request.user
            planet.save()

            # "Private"인 경우에만 초대 코드와 유효기간 저장
            if planet.is_public == 'Private':
                invite_code = secrets.token_urlsafe(8)
                expiration_date = timezone.now() + timedelta(days=7)
                planet.invite_code = invite_code
                planet.expiration_date = expiration_date
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

# 행성 검색
def search(request):
    query = request.GET.get('q')
    planets = Planet.objects.filter(Q(name__icontains=query) | Q(description__icontains=query), is_public='Public')
    context = {
        'planets':planets,
    }
    return render(request, 'planets/search_result.html', context)

@login_required
def planet_contract(request,planet_name):
    planet = Planet.objects.get(name=planet_name)
    # 이미 행성에 계정이 있는 경우
    if Accountbyplanet.objects.filter(planet=planet, user=request.user).exists():
        return redirect('planets:index', planet_name)
    
    if Accountbyplanet.objects.filter(planet=planet).count() >= planet.maximum_capacity:
        messages.info(request, '서버 최대 인원을 초과하여 가입을 진행할 수 없습니다. ')
        return redirect('planets:main')
    
    #private 행성
    if planet.invite_code != request.GET.get('invite_code'):
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
            
            # 행성 주인일 경우
            if planet.created_by == request.user:
                accountbyplanet.admin_level = 3
                accountbyplanet.is_confirmed = True

            # 관리자의 가입 승인이 필요 없는 경우
            elif planet.need_confirm == False:
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

    context = {
        'postform': postform,
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
            'tags': list(post.tags.names()),
            'profile_image_url': post.accountbyplanet.profile_image.url if post.accountbyplanet.profile_image else None,
            'user': post.accountbyplanet.user.username,
        })

    if posts.has_next():
        return JsonResponse(post_list, safe=False)
    else:
        post_list.append(None)
        return JsonResponse(post_list, safe=False)


# 게시글 생성 및 수정
@require_POST
def post_create(request, planet_name, post_pk=None):
    planet = Planet.objects.get(name=planet_name)
    form = PostForm(request.POST, request.FILES)

    if post_pk:  # 기존 게시글 수정 처리
        try:
            post = Post.objects.get(pk=post_pk, planet=planet)
            if form.is_valid():
                form = PostForm(request.POST, request.FILES, instance=post)
                if form.has_changed():  # 폼 데이터가 변경되었는지 확인
                    post = form.save(commit=False)
                    post.save()
                    form.save_m2m()
            else:
                form = PostForm(instance=post)
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'errors': 'Post not found'})
    else:  # 새로운 게시글 생성
        if form.is_valid():
            post = form.save(commit=False)
            post.accountbyplanet = Accountbyplanet.objects.get(planet=planet, user=request.user)
            post.planet = planet
            post.content = form.cleaned_data['content']
            post.image = form.cleaned_data['image']
            post.save()
            form.save_m2m()
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})

    response_data = {
        'success': True,
        'post_pk': post.pk,
        'content': post.content,
        'created_time': post.created_time,
        'nickname': post.accountbyplanet.nickname,
        'image_url': post.image.url if post.image else None,
        'tags': list(post.tags.names()),
        'profile_image_url': post.accountbyplanet.profile_image.url if post.accountbyplanet.profile_image else None,
        'user': post.accountbyplanet.user.username,
        'form_html': form.as_p() if form.as_p() else None,
    }
    return JsonResponse(response_data)


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


# 게시글 상세
@login_required
def post_detail(request, planet_name, post_pk):
    post = Post.objects.get(pk=post_pk)
    planet = Planet.objects.get(name=planet_name)
    comments = Comment.objects.filter(post=post)
    commentform = CommentForm()
    recommentform = RecommentForm()
    
    # emote
    accountbyplanet = Accountbyplanet.objects.get(planet=planet, user=request.user)

    post_emotion_heart = Emote.objects.filter(post=post, emotion='heart')
    post_emotion_thumbsup = Emote.objects.filter(post=post, emotion='thumbsup')
    post_emotion_thumbsdown = Emote.objects.filter(post=post, emotion='thumbsdown')
    
    context = {
        'post': post,
        'comments': comments,
        'planet': planet,
        'commentform': commentform,
        'recommentform': recommentform,
        'post_emotion_heart': post_emotion_heart,
        'post_emotion_thumbsup': post_emotion_thumbsup,
        'post_emotion_thumbsdown': post_emotion_thumbsdown,
        'request_user_nickname': Accountbyplanet.objects.get(user=request.user.pk, planet=planet).nickname,
    }
    return render(request, 'planets/planet_detail.html', context)


# comments json
@login_required
def detail_comments(request, planet_name, post_pk):
    comments = Comment.objects.filter(post_id=post_pk)
    per_page = 5
    page_number = request.GET.get('page')
    paginator = Paginator(comments, per_page)

    try:
        comments = paginator.page(page_number)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    comments_list = []
    for comment in comments:
        recomments = Recomment.objects.filter(comment=comment.pk)
        recomments_data = []
        for recomment in recomments:
            recomments_data.append(
                {
                    'pk': recomment.pk,
                    'content': recomment.content,
                    'created_time': recomment.created_time,
                    'nickname': recomment.accountbyplanet.nickname,
                    'profile_image_url': recomment.accountbyplanet.profile_image.url if recomment.accountbyplanet.profile_image else None,
                }
            )
        comments_list.append({
            'pk': comment.pk,
            'content': comment.content,
            'created_time': comment.created_time,
            'nickname': comment.accountbyplanet.nickname,
            'profile_image_url': comment.accountbyplanet.profile_image.url if comment.accountbyplanet.profile_image else None,
            'user': comment.accountbyplanet.user.username,
            'recomments': recomments_data,
        })
    
    if comments.has_next():
        return JsonResponse(comments_list, safe=False)
    else:
        comments_list.append(None)
        return JsonResponse(comments_list, safe=False)


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
            'profile_image_url': comment.accountbyplanet.profile_image.url if comment.accountbyplanet.profile_image else None,
            'user': comment.accountbyplanet.user.username,
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
            'profile_image_url': recomment.accountbyplanet.profile_image.url if recomment.accountbyplanet.profile_image else None,
            'user': recomment.accountbyplanet.user.username,
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
    # 관리자인 경우 관리 페이지 접근 가능
    is_staff = True if Accountbyplanet.objects.get(planet=planet, user=request.user).admin_level == 2 else False
    is_manager = True if Accountbyplanet.objects.get(planet=planet, user=request.user).admin_level == 3 else False
    
    if is_staff or is_manager:
        confirms = Accountbyplanet.objects.filter(planet=planet, is_confirmed=False)
        if request.method == 'POST':
            form_planet = PlanetForm(request.POST, instance=planet)
            
            if form_planet.is_valid():
                form_planet.save()
                
                return redirect('planets:main')
        else:
            form_planet = PlanetForm(instance=planet)
        
        planet.generate_invite_code() #초대코드 갱신

        context = {
            'form_planet': form_planet,
            'planet': planet,
            'confirms': confirms,
            'is_manager': is_manager,
        }
        return render(request, 'planets/planet_admin.html', context)

    else:
        messages.warning(request, '관리자만 접근 가능합니다. ')
        return redirect('planets:main')


# 행성 약관 관리 페이지
@login_required
def planet_tos_admin(request, planet_name):
    planet = Planet.objects.get(name=planet_name)
    # 관리자만 접근 가능
    is_staff = True if Accountbyplanet.objects.get(planet=planet, user=request.user).admin_level > 1 else False
    if is_staff:
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
    else:
        messages.warning(request, '관리자만 접근 가능합니다. ')
        return redirect('planets:main')
    
# 행성 가입 관리
@login_required
def planet_join_admin(request, planet_name):
    planet = Planet.objects.get(name=planet_name)

    # 관리자만 접근 가능
    is_staff = True if Accountbyplanet.objects.get(planet=planet, user=request.user).admin_level > 1 else False
    if is_staff:
        confirms = Accountbyplanet.objects.filter(planet=planet, is_confirmed=False)

        context = {
            'planet': planet,
            'confirms': confirms,
        }
        return render(request, 'planets/planet_joinㅋㅁ_admin.html', context)
    else:
        messages.warning(request, '관리자만 접근 가능합니다. ')
        return redirect('planets:main')

# 행성 가입 승인
@login_required
def planet_join_confirm(request, planet_name, user_pk):
    planet = Planet.objects.get(name=planet_name)
    # 관리자만 접근 가능
    is_staff = True if Accountbyplanet.objects.get(planet=planet, user=request.user).admin_level > 1 else False
    if is_staff:
        user = User.objects.get(pk=user_pk)
        account = Accountbyplanet.objects.get(planet=planet, user=user)
        account.is_confirmed = True
        account.save()

        return JsonResponse({'success': True})
    else:
        messages.warning(request, '관리자만 접근 가능합니다.')
        return redirect('planets:main')

# 행성 가입 거절
@login_required
def planet_join_reject(request, planet_name, user_pk):
    planet = Planet.objects.get(name=planet_name)
    # 관리자만 접근 가능
    is_staff = True if Accountbyplanet.objects.get(planet=planet, user=request.user).admin_level > 1 else False
    if is_staff:
        user = User.objects.get(pk=user_pk)
        
        account = Accountbyplanet.objects.get(planet=planet, user=user)
        account.delete()

        return JsonResponse({'success': True})    
    else:
        messages.warning(request, '관리자만 접근 가능합니다.')
        return redirect('planets:main')

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

# 행성 회원 관리
def admin_member(request, planet_name):
    planet = Planet.objects.get(name=planet_name)
    is_manager = True if Accountbyplanet.objects.get(planet=planet, user=request.user).admin_level == 3 else False
    if is_manager:
        if request.method == 'POST':    
            accounts = request.POST.getlist('account_pk')
            admin_levels = request.POST.getlist('admin_level')
            for pk, level in zip(accounts, admin_levels):
                temp = Accountbyplanet.objects.get(planet=planet, pk=pk)
                temp.admin_level = level
                temp.save()
            
            return redirect('planets:admin_member', planet_name)

        else:
            accounts = Accountbyplanet.objects.filter(planet=planet)
        
        accounts = Accountbyplanet.objects.filter(planet=planet)
        context = {
            'accounts': accounts,
            'planet_name': planet_name,
        }
        return render(request, 'planets/admin_member.html', context)
    
    else:
        messages.warning(request, '매니저만 접근 가능합니다.')
        return redirect('planets:main')


# 조회 기능
def filter(request, category):
    planets = Planet.objects.filter(category=category).order_by('-created_at')
    context = {
        'planets': planets,
    }
    return render(request, 'planets/planet_list.html', context)

@login_required
def invite_create(request):
    invite_code = request.body.decode('utf-8')
    invite_code = json.loads(invite_code)
    invite_code = invite_code['user_input']
    planets     = Planet.objects.filter(is_public='Private')
    for planet in planets:
        planet.generate_invite_code() #초대코드 갱신

    try:
        planet = Planet.objects.get(invite_code=invite_code, is_public='Private')
        return JsonResponse({'result':True, 'invite_code':invite_code})
        
    except ObjectDoesNotExist:
        return JsonResponse({'result':False, 'invite_code':'실패'})
    

@login_required
def invite_check(request, invite_code):
    planet = Planet.objects.get(invite_code=invite_code, is_public='Private')
    return render(request, 'planets/invite_check.html', {'planet': planet, 'invite_code':invite_code})

def following(request, planet_name, user_pk):
    planet = Planet.objects.get(name=planet_name)

    to_user = Accountbyplanet.objects.get(planet=planet, pk=user_pk)
    from_user = Accountbyplanet.objects.get(planet=planet, user=request.user)
    # 자기 자신을 팔로우 할 수 없음
    if to_user != from_user:
        if to_user.followers.filter(pk=from_user.pk).exists():
            # 팔로우 중이면 팔로우 취소
            to_user.followers.remove(from_user)
            is_followed = False
        else:
            # 팔로우 중이지 않으면 팔로우 
            to_user.followers.add(from_user)
            is_followed = True
        context = {
            'is_followed': is_followed,
            'following_count': to_user.followings.count(),
            'follower_count': to_user.followers.count(),
            'from_user_name': from_user.nickname,
            'from_user_pk': from_user.pk,
        }
        return JsonResponse(context)
    return redirect('planets:index', planet_name)

# 비동기 post emote
@login_required
def post_emote(request, planet_name, post_pk, emotion):
    planet = Planet.objects.get(name=planet_name)
    post = Post.objects.get(pk=post_pk)
    user = Accountbyplanet.objects.get(planet=planet, user=request.user)

    emote = Emote.objects.filter(post=post, accountbyplanet=user, emotion=emotion)

    if emote.exists():
        emote.delete()
    else:
        Emote.objects.create(post=post, accountbyplanet=user, emotion=emotion)

    context = {
        'emotion_count': Emote.objects.filter(post=post, emotion=emotion).count()
    }
    return JsonResponse(context)

# 비동기 comment emote 
@login_required
def comment_emote(request, planet_name, post_pk, emotion):
    planet = Planet.objects.get(name=planet_name)
    comment = Comment.objects.get(pk=post_pk)
    user = Accountbyplanet.objects.get(planet=planet, user=request.user)

    emote = Emote.objects.filter(comment=comment, accountbyplanet=user, emotion=emotion)

    if emote.exists():
        emote.delete()
    else:
        Emote.objects.create(comment=comment, accountbyplanet=user, emotion=emotion)

    context = {
        'emotion_count': Emote.objects.filter(comment=comment, emotion=emotion).count()
    }
    return JsonResponse(context)