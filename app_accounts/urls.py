from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path("login/", views.login, name="login"),
    path('find_id/', views.find_id.as_view(), name='find_id'),
    path('delete/', views.delete, name='delete'),
    path('logout/', views.logout, name='logout'),
]
