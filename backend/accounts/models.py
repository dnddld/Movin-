from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class User(AbstractUser):
    username = models.EmailField(unique=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    nickname = models.CharField(max_length=100, blank=True, default='닉네임')
    birth = models.DateField(null=True, blank=True)

    profile_img = ProcessedImageField(
        upload_to='profile/',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 90},
        blank=True,
        null=True
    )

    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    def __str__(self):
        return self.username
