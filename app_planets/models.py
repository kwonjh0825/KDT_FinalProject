import os
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta, datetime
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from taggit.managers import TaggableManager
from app_accounts.models import Accountsbyplanet


class Planet(models.Model):
    name             = models.CharField(max_length=20, unique=True)
    description      = models.TextField()
    category_choices = (('Tech','Tech'), ('Game','Game'), ('Music','Music'), ('Sprots','Sports'), ('Food','Food'), ('Hobby','Hobby'))
    category         = models.CharField(max_length=20, choices=category_choices)
    image            = ProcessedImageField(
        upload_to  = 'planet/',
        processors = [ResizeToFill(256,128)],
        format     = 'JPEG',
        options    = {'quality' : 100},
        blank      = True,
        null       = True,
    )
    plan_category    = (('Free', 'Free'), ('Premium', 'Primium'))
    plan             = models.CharField(max_length=10, choices=plan_category, default='Free')
    is_public_category = (('Private', 'Private'), ('Public', 'Public'))
    is_public        = models.CharField(max_length=10, choices=is_public_category, default='Private')
    maximum_capacity = models.DecimalField(default=50, max_digits=1000, decimal_places=0)
    created_by       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)


class TermsOfService(models.Model):
    Planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    order = models.IntegerField()
    content = models.CharField(max_length=100, null=False, blank=False)


class Post(models.Model):
    content = models.TextField()
    emotion = models.ManyToManyField(Accountsbyplanet, related_name='emotion_post', through='Emote')
    image   = ProcessedImageField(
        upload_to  = 'planets/posts/',
        processors = [ResizeToFill(400,400)],
        format     = 'JPEG',
        options    = {'quality' : 100},
        blank      = True,
        null       = True,
    )
    planet          = models.ForeignKey(Planet, on_delete=models.CASCADE)
    accountbyplanet = models.ForeignKey(Accountsbyplanet, on_delete=models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    tags            = TaggableManager()

    # post 시간 표시
    @property
    def created_time(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return self.created_at.strftime('%Y-%m-%d')
    
    # post 삭제시 image file 삭제
    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)


class Comment(models.Model):
    content    = models.TextField()
    emotion    = models.ManyToManyField(Accountsbyplanet, related_name='emotion_comment', through='Emote')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post       = models.ForeignKey(Post, on_delete=models.CASCADE)
    accountsbyplanet = models.ForeignKey(Accountsbyplanet, on_delete=models.CASCADE)

    @property
    def created_time(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return self.created_at.strftime('%Y-%m-%d')


# 게시글, 댓글 포함 감정표현
class Emote(models.Model):
    post             = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment          = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    accountsbyplanet = models.ForeignKey(Accountsbyplanet, on_delete=models.CASCADE)
    emotion          = models.CharField(max_length=10)
