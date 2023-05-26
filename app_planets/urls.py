from django.urls import path
from . import views
from app_accounts import views as accounts_views
app_name = 'planets'

urlpatterns = [
    path('', views.main, name='main'),
    path('planets/', views.planet_list, name='planet_list'),
    path('planets/create/', views.planet_create, name='planet_create'),
    path('planets/<str:planet_name>/join/', views.planet_join, name='planet_join'),
    path('planets/<str:planet_name>/delete/', views.planet_delete, name='planet_delete'),
    path('planets/<str:planet_name>/', views.index, name='index'),
    path('planets/<str:planet_name>/<int:post_pk>/delete/', views.post_delete, name='post_delete'),
    path('planets/<str:planet_name>/admin/', views.planet_admin, name='planet_admin'),
    path('planets/<str:planet_name>/admin/tos/', views.planet_tos_admin, name='planet_tos_admin'),
    # 행성별 프로필
    path('planets/<str:planet_name>/profile/<int:user_pk>/', accounts_views.planet_profile, name='planet_profile'),
    path('planets/<str:planet_name>/profile/<int:user_pk>/update/', accounts_views.planet_profile_update, name='planet_profile_update'),
]
