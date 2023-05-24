from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.CharField(max_length=255, unique=True)
    

class Accountsbyplanet(models.Model):
    nickname = models.CharField(max_length=15, blank=False, null=False)
    profile_image  = ProcessedImageField(
        upload_to  = 'accounts/',
        processors = [ResizeToFill(128, 128)],
        format     = 'JPEG',
        options    = {'quality': 100},
        blank      = True,
        null       = True,
    )
    backgounrd_image = ProcessedImageField(
        upload_to  = 'accounts/',
        processors = [ResizeToFill(500, 100)],
        format     = 'JPEG',
        options    = {'quality': 100},
        blank      = True,
        null       = True,
    )
    followings = models.ManyToManyField('self',
                                        symmetrical=False,
                                        blank=True,
                                        related_name='followers')
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accountsbyplanet')
    planet   = models.ForeignKey('app_planets.Planet', on_delete=models.CASCADE)

