from django.urls import path
from . import views

app_name = 'planets'

urlpatterns = [
    path("", views.main, name="main"),
]
