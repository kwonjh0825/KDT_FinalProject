from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import Accountsbyplanet
from django.contrib.auth.forms import SetPasswordForm

# 새 비밀번호 변경 form
class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['new_password1'].widget.attrs.update({
            'class': '',
            'style': 'border: 2px solid red;'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': '',
            'style': 'border: 2px solid red;'
        })


class CustomUserChangeForm(UserChangeForm):
    password = None

    last_name = forms.CharField(
        label = "성",
        widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "홍",
                "style": "height: 47px;",
            }),
    )

    first_name = forms.CharField(
        label = "이름",
        widget = forms.TextInput(
            attrs = {
                "class": "form-control",
                "placeholder": "길동",
                "style": "height: 47px;",
            }),
    )

    email = forms.CharField(
        label = "이메일",
        widget = forms.TextInput(
            attrs = {
                "class": "form-control",
                "placeholder": "gildong@google.com",
                "style": "height: 47px;",
            }),
    )
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', )


class AccountsbyplanetForm(forms.ModelForm):
    nickname = forms.CharField(
        label = "닉네임",
        widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "style": "height: 47px;",
            }),
    )
    class Meta:
        model = Accountsbyplanet
        fields = ('nickname', 'profile_image', 'backgounrd_image')

class CustomAutentication(AuthenticationForm):
    username = forms.CharField(
        label = False,
        widget= forms.TextInput(attrs = {
            'class':'form-control',
            "placeholder": "아이디",
            "style": "height: 47px;",
            "autocomplete": "username",
            }),
    )
    password = forms.CharField(
        label = False,
        widget = forms.PasswordInput(attrs = {
            'class':'form-control',
            "placeholder": "비밀번호",
            "style": "height: 47px;",
            "autocomplete": "current-password",
            }),
    )

    class Meta:
        model = get_user_model
        fields = ('username', 'password')

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="아이디",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "아이디",
                "style": "height: 47px;",
            }),
    )

    last_name = forms.CharField(
        label = "성",
        widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "홍",
                "style": "height: 47px;",
            }),
    )

    first_name = forms.CharField(
        label = "이름",
        widget = forms.TextInput(
            attrs = {
                "class": "form-control",
                "placeholder": "길동",
                "style": "height: 47px;",
            }),
    )

    email = forms.CharField(
        label = "이메일",
        widget = forms.TextInput(
            attrs = {
                "class": "form-control",
                "placeholder": "gildong@google.com",
                "style": "height: 47px;",
            }),
    )

    password1 = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "******",
                "style": "height: 47px;",
            }),
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "******",
                "style": "height: 47px;",
            }),
    )
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'last_name', 'first_name', 'email', 'password1', 'password2',)


