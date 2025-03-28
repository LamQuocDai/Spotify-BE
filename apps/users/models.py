from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=10, unique=True)
    gender = models.IntegerField(choices=[(0, 'Female'), (1, 'Male'), (2, 'Other')], default=2)
    image = models.URLField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('banned', 'Banned')], default='active')
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')

    def __str__(self):
        return self.username