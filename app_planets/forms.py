from django import forms
from .models import Planet
from taggit.forms import TagField


class PlanetForm(forms.ModelForm):
    class Meta:
        model = Planet
        fields = ('name', 'description', 'category', 'image', 'maximum_capacity',)
        labels = {
            'name': '행성 이름', 
            'description': '행성 설명', 
            'category': '카테고리', 
            'image': '행성 사진', 
            'maximum_capacity': '행성 최대 인원',
        }

