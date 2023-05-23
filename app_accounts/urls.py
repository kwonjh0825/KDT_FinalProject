from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    # 최상위 프로필
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/<str:username>/', views.profile, name='profile'),
    # 행성별 프로필
    path('planets/<str:planet_name>/profile/<int:user_pk>/', views.planet_profile, name='planet_profile'),
    path('planets/<str:planet_name>/profile/<int:user_pk>/update/', views.planet_profile_update, name='planet_profile_update'),
    path('find_id/', views.find_id.as_view(), name='find_id'),
    path('delete/', views.delete, name='delete'),
    path('logout/', views.logout, name='logout'),
]


