from django import forms
from .models import Planet, Post
from taggit.forms import TagField


class PlanetForm(forms.ModelForm):
    class Meta:
        model = Planet
        fields = ('name', 'description', 'category', 'is_public', 'image', 'maximum_capacity',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs['placeholder'] = " "
        self.fields['name'].label = '행성 이름'
        self.fields['name'].help_text = ''
        
        self.fields['description'].widget.attrs['placeholder'] = " "
        self.fields['description'].label = '행성 설명'
        self.fields['description'].help_text = ''
        
        self.fields['category'].widget.attrs['placeholder'] = " "
        self.fields['category'].label = '카테고리'
        self.fields['category'].help_text = ''
        
        self.fields['is_public'].label = '공개 여부'
        self.fields['is_public'].help_text = ''
        
        self.fields['image'].label = "행성 사진"
        self.fields['image'].help_text = ''
        
        self.fields['maximum_capacity'].label = "행성 최대 인원"
        self.fields['maximum_capacity'].help_text = ''
        
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
        
