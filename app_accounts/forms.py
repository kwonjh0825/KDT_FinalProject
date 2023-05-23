from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from .models import Accountsbyplanet

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('username', 'first_name', 'email', )


class AccountsbyplanetForm(forms.ModelForm):
    class Meta:
        model = Accountsbyplanet
        fields = ('nickname', 'profile_image', 'backgounrd_image')