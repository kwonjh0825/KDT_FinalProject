import json
import secrets
import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count, Q, Sum, Case, When, IntegerField
from .models import Planet, TermsOfService, Post, Comment, Recomment, Emote, Report, Vote, VoteTopic
from .forms import PlanetForm, PostForm, CommentForm, RecommentForm, VoteTopicForm
from app_accounts.models import Accountbyplanet, User, Memobyplanet
from app_accounts.forms import AccountbyplanetForm, MemobyplanetForm
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist # 예외처리
from taggit.models import Tag



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
    user = request.user
    if user.is_authenticated:
        user_planets = Accountbyplanet.objects.filter(user=user, planet__in=planets)
        joined_planets = [user_planet.planet for user_planet in user_planets]
        joined_planet_list = [joined_planet.name for joined_planet in joined_planets]
    else:
        joined_planet_list = None
    
    for planet in planets:
        planet.current_capacity = Accountbyplanet.objects.filter(planet=planet).count()
    context = {
        'planets': planets,
        'joined_planet_list': joined_planet_list,
    }
    return render(request, 'planets/planet_list.html', context)


# 조회 기능
def filter(request, category):
    planets = Planet.objects.filter(category=category, is_public='Public').order_by('-created_at')
    user = request.user
    if user.is_authenticated:
        user_planets = Accountbyplanet.objects.filter(user=user, planet__in=planets)
        joined_planets = [user_planet.planet for user_planet in user_planets]
        joined_planet_list = [joined_planet.name for joined_planet in joined_planets]
    else:
        joined_planet_list = None
    
    for planet in planets:
        planet.current_capacity = Accountbyplanet.objects.filter(planet=planet).count()
        
    context = {
        'planets': planets,
        'joined_planet_list': joined_planet_list,
    }
    return render(request, 'planets/planet_list.html', context)


# 내가 가입한 행성
def my_planet_filter(request):
    user = request.user
    if user.is_authenticated:
        planets = Planet.objects.filter(is_public='Public')
        user_planets = Accountbyplanet.objects.filter(user=user, planet__in=planets)
        joined_planets = [user_planet.planet for user_planet in user_planets]
        joined_planet_list = [joined_planet.name for joined_planet in joined_planets]
        for planet in joined_planets:
            planet.current_capacity = Accountbyplanet.objects.filter(planet=planet).count()
    else:
        return redirect('accounts:login')
    
    context = {
        'planets': joined_planets,
        'joined_planet_list': joined_planet_list
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
    query = request.POST.get('q')
    planets = Planet.objects.filter(Q(name__icontains=query) | Q(description__icontains=query), is_public='Public')
    user = request.user
    if user.is_authenticated:
        user_planets = Accountbyplanet.objects.filter(user=user, planet__in=planets)
        joined_planets = [user_planet.planet for user_planet in user_planets]
        joined_planet_list = [joined_planet.name for joined_planet in joined_planets]
    else:
        joined_planet_list = None

    for planet in planets:
        planet.current_capacity = Accountbyplanet.objects.filter(planet=planet).count()
        
    context = {
        'planets':planets,
        'joined_planet_list': joined_planet_list,

    }
    return render(request, 'planets/planet_list.html', context)


# 행성 이용약관
@login_required
def planet_contract(request,planet_name):
    planet = Planet.objects.get(name=planet_name)
    # 이미 행성에 계정이 있는 경우
    if Accountbyplanet.objects.filter(planet=planet, user=request.user).exists():
        return redirect('planets:index', planet_name)
    
    if Accountbyplanet.objects.filter(planet=planet).count() >= planet.maximum_capacity:
        messages.warning(request, '서버 최대 인원을 초과하여 가입을 진행할 수 없습니다. ')
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
            
            # 신청 완료
            elif planet.need_confirm == True:
                messages.success(request, '신청이 완료되었습니다')

            accountbyplanet.save()
            return redirect('planets:index', planet_name)
    else:
        form = AccountbyplanetForm()

    context = {
        'form': form,
        'planet': planet,
    }
    return render(request, 'planets/planet_join.html', context)


# 행성 탈퇴
@login_required
def planet_withdraw(request, planet_name):
    planet = Planet.objects.get(name=planet_name)
    accountbyplanet = Accountbyplanet.objects.get(planet=planet, user=request.user)
    accountbyplanet.delete()
    return redirect('planets:planet_list')


# 행성 페이지
def index(request, planet_name):
    planet = Planet.objects.get(name=planet_name)

    # 행성에 계정이 없는 경우 또는 가입 승인 대기 중인 경우
    if not request.user.is_authenticated or not Accountbyplanet.objects.filter(planet=planet, user=request.user).exists() or Accountbyplanet.objects.get(planet=planet, user=request.user).is_confirmed == False: 
        return redirect('planets:main')
    
    postform = PostForm()
    votetopicform = VoteTopicForm()

    try:
        memo = Memobyplanet.objects.get(accountbyplanet=Accountbyplanet.objects.get(planet=planet, user=request.user))
    except:
        memo = None
    memoform = MemobyplanetForm()

    context = {
        'votetopicform': votetopicform,
        'postform': postform,
        'planet': planet,
        'memo': memo,
        'memoform': memoform,
        'first_post': Post.objects.filter(planet=planet).first(),
        'user': Accountbyplanet.objects.get(planet=planet, user=request.user),
        'user_id': request.user,

    }
    return render(request, 'planets/index.html', context)


# 행성 내부 이동 페이지
def index_list(request, planet_name):
    planet = Planet.objects.get(name=planet_name)
    user = request.user
    user_by_planets_star = Accountbyplanet.objects.filter(user=user, star=1)
    user_by_planets_not_star = Accountbyplanet.objects.filter(user=user, star=0)
    user_planets = Accountbyplanet.objects.filter(user=user)
    user_categories = user_planets.values_list('planet__category', flat=True).distinct()
    planet_recommends = Planet.objects.filter(category__in=user_categories, is_public='Public').exclude(accountbyplanet__in=user_planets).order_by('?')[:5]
    planet_not_recommends = Planet.objects.exclude(category__in=user_categories).exclude(accountbyplanet__in=user_planets).exclude(is_public='Private').order_by('?')[:5]
    num_not_recommended = max(0, 5 - len(planet_recommends))
    planet_not_recommends = planet_not_recommends[:num_not_recommended]
    
    try:
        memo = Memobyplanet.objects.get(accountbyplanet=Accountbyplanet.objects.get(planet=planet, user=request.user))
    except:
        memo = None
    memoform = MemobyplanetForm()
    
    # 행성에 계정이 없는 경우 또는 가입 승인 대기 중인 경우
    if not request.user.is_authenticated or not Accountbyplanet.objects.filter(planet=planet, user=request.user).exists() or Accountbyplanet.objects.get(planet=planet, user=request.user).is_confirmed == False: 
        return redirect('planets:main')
    
    postform = PostForm()
    votetopicform = VoteTopicForm()
        
    context = {
        'votetopicform': votetopicform,
        'postform': postform,
        'planet': planet,
        'memo': memo,
        'memoform': memoform,
        'user_by_planets_star' : user_by_planets_star,
        'user_by_planets_not_star':user_by_planets_not_star,
        'first_post': Post.objects.filter(planet=planet).first(),
        'user': Accountbyplanet.objects.get(planet=planet, user=request.user),
        'user_categories' : user_categories,
        'planet_recommends': planet_recommends,
        'planet_not_recommends': planet_not_recommends,
        'user_id': request.user,
    }
    return render(request, 'planets/index_list.html', context)


# 행성 소개 페이지
def planet_introduction(request, planet_name):
    planet = Planet.objects.get(name=planet_name)
    
    try:
        memo = Memobyplanet.objects.get(accountbyplanet=Accountbyplanet.objects.get(planet=planet, user=request.user))
    except:
        memo = None

    memoform = MemobyplanetForm()
    planet.current_capacity = Accountbyplanet.objects.filter(planet=planet).count()
    postform = PostForm()
    
    if request.method == 'POST':    
        accounts = request.POST.getlist('account_pk')
        admin_levels = request.POST.getlist('admin_level')
        for pk, level in zip(accounts, admin_levels):
            temp = Accountbyplanet.objects.get(planet=planet, pk=pk)
            temp.admin_level = level
            temp.save()
        
        return redirect('planets:planet_introduction', planet_name)

    else:
        accounts = Accountbyplanet.objects.filter(planet=planet)
        
    context = {
        'accounts': accounts,
        'planet': planet,
        'memo': memo,
        'memoform': memoform,
        'user': Accountbyplanet.objects.get(planet=planet, user=request.user),
        'postform':postform,
        'user_id': request.user,
    }

    return render(request, 'planets/planet_introduction.html', context)


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
    planet = Planet.objects.get(name=planet_name)
    posts = Post.objects.filter(planet=planet).order_by('-pk')
    per_page = 5
    page_number = request.POST.get('page')
    paginator = Paginator(posts, per_page)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    post_list = []
    user = Accountbyplanet.objects.get(user=request.user, planet=planet)
    for post in posts:
        # 해당 Post의 VoteTopic들을 가져옵니다.
        vote_topics = VoteTopic.objects.filter(post=post)

        voted_topics = list(
            Vote.objects.filter(voter=user, votetopic__in=vote_topics).values_list('votetopic_id', flat=True)
        )
        
        post_list.append({
            'pk': post.pk,
            'content': post.content,
            'created_time': post.created_time,
            'nickname': post.accountbyplanet.nickname,
            'image_url': post.image.url if post.image else None,
            'tags': list(post.tags.names()),
            'profile_image_url': post.accountbyplanet.profile_image.url if post.accountbyplanet.profile_image else None,
            'user': post.accountbyplanet.user.username,
            'votetopics': list(post.votetopic_set.values('title')),
            'post_emote_heart': Emote.objects.filter(post=post, emotion='heart').count(),
            'post_emote_thumbsup': Emote.objects.filter(post=post, emotion='thumbsup').count(),
            'post_emote_thumbsdown': Emote.objects.filter(post=post, emotion='thumbsdown').count(),
            'vote_count':[Vote.objects.filter(votetopic=vote_topic).count() for vote_topic in vote_topics],
            'voted': True if voted_topics else False,
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
    votetopicform = VoteTopicForm(request.POST)
    accountbyplanet = Accountbyplanet.objects.get(planet=planet, user=request.user)
    
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
            post.accountbyplanet = accountbyplanet
            post.planet = planet
            post.image = form.cleaned_data['image']
            post.save()
            form.save_m2m()
        #투표 주제
        if votetopicform.is_valid():
            titles = request.POST.getlist('title')
            for title in titles:
                if title == '':
                    continue
                votetopic = VoteTopic()
                votetopic.title = title
                votetopic.post = post
                votetopic.save()
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    
    vote_topics = VoteTopic.objects.filter(post=post)
    voted_topics = list(
            Vote.objects.filter(voter=accountbyplanet, votetopic__in=vote_topics).values_list('votetopic_id', flat=True)
        )
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
        'votetopics': list(post.votetopic_set.values('title')),
        'vote_count':[Vote.objects.filter(votetopic=vote_topic).count() for vote_topic in vote_topics],
        'voted': True if voted_topics else False,
    }
    try:
        response_data['votetopic'] = titles
    except:
        response_data['votetopic'] = None

    return JsonResponse(response_data)


# 게시글 삭제
@require_POST
def post_delete(request, planet_name, post_pk):
    post = Post.objects.get(pk=post_pk)
    planet = Planet.objects.get(name=planet_name)
    accountbyplanet = Accountbyplanet.objects.get(user=request.user.pk, planet=planet)
    
    if accountbyplanet == post.accountbyplanet or accountbyplanet.admin_level > 1:
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

    vote_topics = VoteTopic.objects.filter(post=post)
    voted_topics = list(
            Vote.objects.filter(voter=accountbyplanet, votetopic__in=vote_topics).values_list('votetopic_id', flat=True)
        )
    vote_count = [Vote.objects.filter(votetopic=vote_topic).count() for vote_topic in vote_topics]
    postform = PostForm()
    votetopicform = VoteTopicForm()

    try:
        memo = Memobyplanet.objects.get(accountbyplanet=accountbyplanet)
    except:
        memo = None
    memoform = MemobyplanetForm()

    context = {
        'votetopicform': votetopicform,
        'postform': postform,
        'post': post,
        'comments': comments,
        'planet': planet,
        'commentform': commentform,
        'recommentform': recommentform,
        'memo': memo,
        'memoform': memoform,
        'post_emotion_heart': post_emotion_heart,
        'post_emotion_thumbsup': post_emotion_thumbsup,
        'post_emotion_thumbsdown': post_emotion_thumbsdown,
        'user': Accountbyplanet.objects.get(user=request.user.pk, planet=planet),
        'votetopics_count': zip(vote_topics, vote_count),
        'total_vote_count': sum(vote_count),
        'voted': True if voted_topics else False,
        'vote_topics':vote_topics,
        'user_id': request.user,
    }
    
    return render(request, 'planets/planet_detail.html', context)


# comments json
@login_required
def detail_comments(request, planet_name, post_pk):
    comments = Comment.objects.filter(post_id=post_pk)
    comments_list = []
    for comment in comments:
        comment_emote_heart = Emote.objects.filter(comment=comment, emotion='heart').count()
        comment_emote_thumbsup = Emote.objects.filter(comment=comment, emotion='thumbsup').count()
        comment_emote_thumbsdown = Emote.objects.filter(comment=comment, emotion='thumbsdown').count()
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
            'comment_emote_heart': comment_emote_heart,
            'comment_emote_thumbsup': comment_emote_thumbsup,
            'comment_emote_thumbsdown': comment_emote_thumbsdown,
        })
    return JsonResponse(comments_list, safe=False)


# 댓글 생성 및 수정
@require_POST
def comment_create(request, planet_name, post_pk, comment_pk=None):
    planet = Planet.objects.get(name=planet_name)
    post = Post.objects.get(pk=post_pk, planet=planet)
    form = CommentForm(request.POST)

    if comment_pk:  # 기존 댓글 수정 처리
        try:
            comment = Comment.objects.get(pk=comment_pk)
            if form.is_valid():
                form = CommentForm(request.POST, instance=comment)
                if form.has_changed():  # 폼 데이터가 변경되었는지 확인
                    comment = form.save(commit=False)
                    comment.save()
            else:
                form = CommentForm(instance=comment)
        except Comment.DoesNotExist:
            return JsonResponse({'success': False, 'errors': 'Comment not found'})
    else:  # 새로운 댓글 생성
        if form.is_valid():
            comment = form.save(commit=False)
            comment.accountbyplanet = Accountbyplanet.objects.get(planet=planet, user=request.user)
            comment.planet = planet
            comment.content = form.cleaned_data['content']
            comment.post = post
            comment.save()
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
        
    response_data = {
        'success': True,
        'comment_pk': comment.pk,
        'content': comment.content,
        'created_time': comment.created_time,
        'nickname': comment.accountbyplanet.nickname,
        'profile_image_url': comment.accountbyplanet.profile_image.url if comment.accountbyplanet.profile_image else None,
        'user': comment.accountbyplanet.user.username,
        'form_html': form.as_p() if form.as_p() else None,
    }
    return JsonResponse(response_data)


# 댓글 삭제
@require_POST
def comment_delete(request, planet_name, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    planet = Planet.objects.get(name=planet_name)
    accountbyplanet = Accountbyplanet.objects.get(user=request.user.pk, planet=planet)

    if accountbyplanet == comment.accountbyplanet or accountbyplanet.admin_level > 1:
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
def recomment_create(request, planet_name, post_pk, comment_pk, recomment_pk=None):
    planet = Planet.objects.get(name=planet_name)
    post = Post.objects.get(pk=post_pk, planet=planet)
    comment = Comment.objects.get(pk=comment_pk, post=post)
    form = RecommentForm(request.POST)

    if recomment_pk:  # 기존 대댓글 수정 처리
        try:
            recomment = Recomment.objects.get(pk=recomment_pk)
            if form.is_valid():
                form = RecommentForm(request.POST, instance=recomment)
                if form.has_changed():  # 폼 데이터가 변경되었는지 확인
                    recomment = form.save(commit=False)
                    recomment.save()
            else:
                form = RecommentForm(instance=recomment)
        except Recomment.DoesNotExist:
            return JsonResponse({'success': False, 'errors': 'Recomment not found'})
    else:  # 새로운 대댓글 생성
        if form.is_valid():
            recomment = form.save(commit=False)
            recomment.accountbyplanet = Accountbyplanet.objects.get(planet=planet, user=request.user)
            recomment.planet = planet
            recomment.content = form.cleaned_data['content']
            recomment.post = post
            recomment.comment = comment
            recomment.save()
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
        
    response_data = {
        'success': True,
        'recomment_pk': recomment.pk,
        'content': recomment.content,
        'created_time': recomment.created_time,
        'nickname': recomment.accountbyplanet.nickname,
        'profile_image_url': recomment.accountbyplanet.profile_image.url if recomment.accountbyplanet.profile_image else None,
        'user': recomment.accountbyplanet.user.username,
        'form_html': form.as_p() if form.as_p() else None,
    }
    return JsonResponse(response_data)


# 대댓글 삭제
@require_POST
def recomment_delete(request, planet_name, recomment_pk):
    recomment = Recomment.objects.get(pk=recomment_pk)
    planet = Planet.objects.get(name=planet_name)
    accountbyplanet = Accountbyplanet.objects.get(user=request.user.pk, planet=planet)

    if accountbyplanet == recomment.accountbyplanet or accountbyplanet.admin_level > 1:
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
            form_planet = PlanetForm(request.POST,request.FILES, instance=planet)
            if form_planet.is_valid():
                form_planet.save()
                return redirect('planets:index', planet.name)
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

            return redirect('planets:planet_admin',planet_name)
        
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
        return render(request, 'planets/planet_join_admin.html', context)
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
@login_required
def report(request, planet_name, report_category, pk):
    planet = Planet.objects.get(name=planet_name)
    user = request.user
    accountbyplanet = Accountbyplanet.objects.get(planet=planet, user=user)
    # method GET
    if request.method == 'POST':
        content = request.POST.get('report_content')
        if report_category == 'post':
            post = Post.objects.get(pk=pk)
            if not Report.objects.filter(post=post, user=user):
                Report.objects.create(post=post, content=content, user=user)
                messages.info(request, '신고가 완료되었습니다.') 
            else:
                messages.warning(request, '이미 신고한 게시글입니다.')
        elif report_category == 'comment':
            comment = Comment.objects.get(pk=pk)
            if not Report.objects.filter(comment=comment, user=user):
                Report.objects.create(comment=comment, content=content, user=user)
                messages.info(request, '신고가 완료되었습니다.') 
            else:
                messages.warning(request, '이미 신고한 댓글입니다.')
        else:
            recomment = Recomment.objects.get(pk=pk)
            if not Report.objects.filter(recomment=recomment, user=user):
                Report.objects.create(recomment=recomment, content=content, user=user)
                messages.info(request, '신고가 완료되었습니다.') 
            else:
                messages.warning(request, '이미 신고한 댓글입니다.')

        return redirect('planets:index', planet.name)
    
    else:
        if report_category == 'post':
            post = Post.objects.get(pk=pk)
            if accountbyplanet == post.accountbyplanet:
                messages.warning(request, '본인의 게시물은 신고할 수 없습니다. ')
                return redirect('planets:index', planet.name)
            else:
                context = {
                    'reported': post,
                }
        elif report_category == 'comment':
            comment = Comment.objects.get(pk=pk)
            if accountbyplanet == comment.accountbyplanet:
                messages.warning(request, '본인의 댓글은 신고할 수 없습니다. ')
                return redirect('planets:index', planet.name)
            else:
                context = {
                    'reported': comment,
                }
        else:
            recomment = Recomment.objects.get(pk=pk)
            if accountbyplanet == recomment.accountbyplanet:
                messages.warning(request, '본인의 대댓글은 신고할 수 없습니다. ')
                return redirect('planets:index', planet.name)
            else:
                context = {
                    'reported': recomment,
                }

        context['category'] = report_category
        context['planet'] = planet
        context['pk'] = pk
        context['user'] = Accountbyplanet.objects.get(planet=planet, user=request.user)
        context['user_id'] = request.user

        return render(request, 'planets/report.html', context)
    

# 신고 관리 페이지
def admin_report(request, planet_name):
    planet = Planet.objects.get(name=planet_name)
    is_manager = True if Accountbyplanet.objects.get(planet=planet, user=request.user).admin_level == 3 else False
    if is_manager:
        post_reports = Report.objects.exclude(post__isnull=True)
        comment_reports = Report.objects.exclude(comment__isnull=True)
        recomment_reports = Report.objects.exclude(recomment__isnull=True)
        post_reports_count = Report.objects.exclude(post__isnull=True).values('post').annotate(Count('pk'))
        comment_reports_count = Report.objects.exclude(comment__isnull=True).values('comment').annotate(Count('pk'))
        recomment_reports_count = Report.objects.exclude(recomment__isnull=True).values('recomment').annotate(Count('pk'))
        context = {
            'planet': planet,
            'post_reports': post_reports,
            'post_reports_count': post_reports_count,
            'comment_reports': comment_reports,
            'comment_reports_count': comment_reports_count,
            'recomment_reports': recomment_reports,
            'recomment_reports_count': recomment_reports_count,
        }
        return render(request, 'planets/admin_report.html', context)
    else:
        messages.warning(request, '매니저만 접근 가능합니다.')
        return redirect('planets:main')


# 행성 회원 관리
def admin_member(request, planet_name):
    planet = Planet.objects.get(name=planet_name)
    is_manager = True if Accountbyplanet.objects.get(planet=planet, user=request.user).admin_level == 3 else False
    if is_manager:
        if request.method == 'POST':    
            accounts = request.POST.getlist('account_pk')
            for pk in accounts:
                admin_levels = request.POST.get('admin_level_' + pk)
                temp = Accountbyplanet.objects.get(planet=planet, pk=pk)
                temp.admin_level = admin_levels
                temp.save()
            return redirect('planets:planet_admin', planet_name)
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


# 초대 코드 생성
@login_required
def invite_create(request):
    invite_code = request.body.decode('utf-8')
    invite_code = json.loads(invite_code)
    invite_code = invite_code['user_input']
    planets     = Planet.objects.filter(is_public='Private')
    for planet in planets:
        planet.generate_invite_code() #초대코드 갱신

    try:
        planet = Planet.objects.get(invite_code=invite_code)
        return JsonResponse({'result':True, 'invite_code':invite_code})
    except ObjectDoesNotExist:
        return JsonResponse({'result':False, 'invite_code':'실패'})
    

# 초대 확인
@login_required
def invite_check(request, invite_code):
    planet = Planet.objects.get(invite_code=invite_code)
    return render(request, 'planets/invite_check.html', {'planet': planet, 'invite_code':invite_code})


# 팔로우
@login_required
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


# 투표
@login_required
def vote(request, post_pk, vote_title):
    post = Post.objects.get(pk=post_pk)
    user = Accountbyplanet.objects.get(user=request.user, planet=post.planet)
    vote_topic = VoteTopic.objects.get(title=vote_title, post=post)
    if request.method == 'POST':

        # 중복 투표 x
        if Vote.objects.filter(voter=user, votetopic__post=post).exists():
            return redirect('planets:index', post.planet.name)
            # return redirect('planets:planet_posts', post.planet.name)
            
        # 새로운 투표 생성
        vote = Vote(votetopic=vote_topic, voter=user)
        vote.save()
        context = {
            'result':'success',
            'planet_name':post.planet.name,
        }
        return JsonResponse(context)
        

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
def comment_emote(request, planet_name, post_pk, comment_pk, emotion):
    planet = Planet.objects.get(name=planet_name)
    comment = Comment.objects.get(pk=comment_pk)
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


# tags 리스트 페이지
@login_required
def tags_list(request, planet_name):
    planet = Planet.objects.get(name=planet_name)
    posts = Post.objects.filter(planet=planet, created_at__gte=timezone.now() - datetime.timedelta(weeks=2))
    tags = Tag.objects.filter(post__in=posts).annotate(tag_count=Count('post')).order_by('-tag_count')[:5]
    accountbyplanet = Accountbyplanet.objects.get(planet=planet, user=request.user)
    total_posts = sum([tag.tag_count for tag in tags])
    postform = PostForm()
    try:
        memo = Memobyplanet.objects.get(accountbyplanet=accountbyplanet)
    except:
        memo = None
    memoform = MemobyplanetForm()
    context = {
        'postform': postform,
        'memo': memo,
        'memoform': memoform,
        'tags': tags,
        'total_posts': total_posts,
        'planet': planet,
        'user': accountbyplanet,
        'user_id': request.user,
    }
    return render(request, 'planets/planet_tags.html', context)


# tag 페이지
@login_required
def post_tag(request, planet_name, tag_name):
    planet = Planet.objects.get(name=planet_name)
    tag = Tag.objects.get(name=tag_name)
    accountbyplanet = Accountbyplanet.objects.get(planet=planet, user=request.user)
    posts = Post.objects.filter(planet=planet, tags=tag).order_by('-pk').annotate(
        heart_count=Count('emote', filter=Q(emote__emotion='heart')),
        thumbsup_count=Count('emote', filter=Q(emote__emotion='thumbsup')),
        thumbsdown_count=Count('emote', filter=Q(emote__emotion='thumbsdown'))
    )
    for post in posts:
        post.vote_topics = VoteTopic.objects.filter(post=post)
        post.vote_counts = []
        for vote_topic in post.vote_topics:
            vote_count = Vote.objects.filter(votetopic=vote_topic).count()
            post.vote_counts.append({
                'vote_topic': vote_topic,
                'vote_count': vote_count
            })
        post.voted = Vote.objects.filter(votetopic__in=post.vote_topics, voter=accountbyplanet).exists()
        post.total_vote_count = Vote.objects.filter(votetopic__in=post.vote_topics).aggregate(
            total=Sum(
                Case(
                    When(voter__isnull=False, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )['total']

    postform = PostForm()
    try:
        memo = Memobyplanet.objects.get(accountbyplanet=accountbyplanet)
    except:
        memo = None
    memoform = MemobyplanetForm()
    context = {
        'postform': postform,
        'posts': posts,
        'memo': memo,
        'memoform': memoform,
        'planet': planet,
        'user': accountbyplanet,
        'user_id': request.user,
    }
    return render(request, 'planets/planet_posts_filter.html', context)


# 메모
@login_required
def planet_memo(request, planet_name):
    planet = Planet.objects.get(name=planet_name)
    accountbyplanet = Accountbyplanet.objects.get(planet=planet, user=request.user)
    memoform = MemobyplanetForm(request.POST)
    try:
        memo = Memobyplanet.objects.get(accountbyplanet=accountbyplanet)
    except:
        memo = None
    
    if memo:  # 기존 메모 수정 처리
        try:
            if memoform.is_valid() and request.POST:
                memoform = MemobyplanetForm(request.POST, instance=memo)
                if memoform.has_changed():  # 폼 데이터가 변경되었는지 확인
                    memoform = MemobyplanetForm(request.POST, instance=memo)
                    memo = memoform.save(commit=False)
                    memo.save()
                else:
                    memo.delete()
                    memo = None
            else:
                memoform = MemobyplanetForm(instance=memo)
        except Memobyplanet.DoesNotExist:
            return JsonResponse({'success': False, 'errors': 'Memo not found'})
    else:   # 새로운 메모 생성
        if memoform.is_valid():
            memo = memoform.save(commit=False)
            memo.accountbyplanet = accountbyplanet
            memo.save()
        else:
            errors = memoform.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    
    response_data = {
        'success': True,
        'memo': memo.memo if memo else memo,
        'memoform': memoform.as_p() if memoform.as_p() else None,
    }
    
    return JsonResponse(response_data)


# 행성 즐겨찾기
@login_required
def planet_star(request, planet_name):
    planet = Planet.objects.get(name=planet_name)
    accountbyplanet = Accountbyplanet.objects.get(planet=planet, user=request.user)
    if accountbyplanet.star == False:
        accountbyplanet.star = True
    else:
        accountbyplanet.star = False
    accountbyplanet.save()
    response_data = {
        'success': True,
        'star': accountbyplanet.star,
    }
    return JsonResponse(response_data)


# 행성 내 post 검색
def post_search(request, planet_name):
    planet = Planet.objects.get(name=planet_name)
    keyword = request.GET.get('keyword', False)
    search_results = Post.objects.filter(Q(planet=planet, content__icontains=keyword) | Q(planet=planet, tags__name__icontains=keyword)).order_by('-pk')
    user = Accountbyplanet.objects.get(planet=planet, user=request.user)

    for post in search_results:
        post.heart_count = Emote.objects.filter(post=post, emotion='heart').count()
        post.thumbsup_count = Emote.objects.filter(post=post, emotion='thumbsup').count()
        post.thumbsdown_count = Emote.objects.filter(post=post, emotion='thumbsdown').count()
        post.vote_topics = VoteTopic.objects.filter(post=post)
        post.vote_counts = []
        for vote_topic in post.vote_topics:
            vote_count = Vote.objects.filter(votetopic=vote_topic).count()
            post.vote_counts.append({
                'vote_topic': vote_topic,
                'vote_count': vote_count
            })
        post.voted = Vote.objects.filter(votetopic__in=post.vote_topics, voter=user).exists()
        post.total_vote_count = Vote.objects.filter(votetopic__in=post.vote_topics).aggregate(
            total=Sum(
                Case(
                    When(voter__isnull=False, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )['total']

    postform = PostForm()
    try:
        memo = Memobyplanet.objects.get(accountbyplanet=user)
    except:
        memo = None
    memoform = MemobyplanetForm()

    context = {
        'posts': search_results,
        'planet': planet,
        'user': user,
        'postform': postform,
        'memo': memo,
        'memoform': memoform,
        'user_id': request.user,
    }
    return render(request, 'planets/planet_posts_filter.html', context)
