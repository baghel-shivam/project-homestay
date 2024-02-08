from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, UserManager
import os


def user_dp_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/username/dp_imgs/<filename>
    return os.path.join(instance.username, 'dp_imgs', filename)

class User(AbstractBaseUser, PermissionsMixin):
    display_img = models.FileField(blank=True, null=True, upload_to=user_dp_path)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    mobile_no = models.CharField(max_length=13,  blank=True, null=True)
    email = models.EmailField(blank=True, null=True, max_length=200)
    username = models.CharField(max_length=200,unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = "username"
    objects = UserManager()
    def __str__(self):
        return self.username