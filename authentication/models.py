from django.db import models
from django.contrib.auth.models import AbstractUser
import os
import random
from django.conf import settings

class CustomUser(AbstractUser):
    age = models.IntegerField(default=18)
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True)
    rating = models.FloatField(default=0)
    # Provide custom related_name attributes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        related_query_name='custom_user',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        related_query_name='custom_user',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def _str_(self):
        return self.username
    def save(self, *args, **kwargs):
        if not self.profile_photo:  # If profile photo is not already set
            if self.gender == 'Male':
                profile_photo_folder = os.path.join(settings.MEDIA_ROOT, 'male/')
                profile_photos = os.listdir(profile_photo_folder)
                if profile_photos:
                    profile_photo = random.choice(profile_photos)
                    self.profile_photo = os.path.join('male/', profile_photo)
            elif self.gender == 'Female':
                profile_photo_folder = os.path.join(settings.MEDIA_ROOT, 'female/')
                profile_photos = os.listdir(profile_photo_folder)
                if profile_photos:
                    profile_photo = random.choice(profile_photos)
                    self.profile_photo = os.path.join('female/', profile_photo)
        super().save(*args, **kwargs)