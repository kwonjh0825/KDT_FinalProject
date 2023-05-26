from django.urls import path
from . import views

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
    path('planets/<str:planet_name>/admin/join', views.planet_join_admin, name='planet_join_admin'),
    path('planets/<str:planet_name>/admin/join/<int:user_pk>/confirm/', views.planet_join_confirm, name='planet_join_confirm'),
    path('planets/<str:planet_name>/admin/join/<int:user_pk>/reject/', views.planet_join_reject, name='planet_join_reject'),
]
