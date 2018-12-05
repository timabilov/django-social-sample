from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserProfile(AbstractUser):
    REQUIRED_FIELDS = ['email']

    email = models.EmailField(_('Email address'), blank=True)
    first_name = models.CharField(_('first name'), max_length=100, blank=True)
    last_name = models.CharField(_('first name'), max_length=100, blank=True)
    last_seen = models.DateTimeField(auto_now=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    facebook_id = models.CharField(null=True, blank=True, max_length=250)
    google_id = models.CharField(null=True, blank=True, max_length=250)

    # S3, digital ocean spaces
    img = models.ImageField(upload_to='profile_avatar', null=True, blank=True)
    banned = models.BooleanField(default=False)
    # Search count

    def __str__(self):
        return f'{self.username}'


class Post(models.Model):
    content = models.TextField(
        verbose_name=_('content'), null=False, blank=True
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # index
    likes = models.IntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content


class PostLike(models.Model):

    class Meta:
        unique_together = ('reacted', 'post')

    reacted = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='liked_posts', on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        'Post', related_name='liked_users', on_delete=models.CASCADE
    )
    created = models.DateTimeField(default=timezone.now)
