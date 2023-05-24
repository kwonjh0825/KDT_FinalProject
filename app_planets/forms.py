from django import forms
from .models import Planet, Post
from taggit.forms import TagField


class PlanetForm(forms.ModelForm):
    class Meta:
        model = Planet
        fields = ('name', 'description', 'category', 'image', 'maximum_capacity', 'is_public')
        labels = {
            'name': '행성 이름', 
            'description': '행성 설명', 
            'category': '카테고리', 
            'image': '행성 사진', 
            'maximum_capacity': '행성 최대 인원',
            'is_private': '공개 범위 설정',
        }


class PostForm(forms.ModelForm):
    tags = TagField(required=False)
    class Meta:
        model = Post
        fields = ('content', 'image', 'tags',)
        labels = {
            'content': '내용',
            'image': '사진',
            'tags': '태그',
        }
        
