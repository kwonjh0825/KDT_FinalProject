from django.contrib import admin
from .models import Planet, TermsOfServices, Post, Comment

# Register your models here.

admin.site.register(Planet)
admin.site.register(TermsOfServices)
admin.site.register(Post)
admin.site.register(Comment)
