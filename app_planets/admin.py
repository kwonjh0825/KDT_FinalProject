from django.contrib import admin
from .models import Planet, TermsOfService, Post, Comment

# Register your models here.

admin.site.register(Planet)
admin.site.register(TermsOfService)
admin.site.register(Post)
admin.site.register(Comment)
