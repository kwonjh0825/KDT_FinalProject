from django import forms
from .models import Planet, Post
from taggit.forms import TagField


class PlanetForm(forms.ModelForm):
    class Meta:
        model = Planet

        fields = ('name', 'description', 'category', 'is_public', 'image', 'maximum_capacity',)
        labels = {
            'name': '행성 이름', 
            'description': '행성 설명', 
            'category': '카테고리', 
            'is_public': '공개 여부',
            'image': '행성 사진', 
            'maximum_capacity': '행성 최대 인원',
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
        
