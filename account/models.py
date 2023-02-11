from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from commons.models import StatusModel, TimeStampModel
from post.models import Post

# Create your models here.

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, **other_fields)
    
    def create_user(self, email, username, password, **other_fields):

        if not email:
            raise ValueError('You must provide an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email,username=username,**other_fields)

        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser,PermissionsMixin, TimeStampModel):
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos', default='default.png', blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.username


class Profile(TimeStampModel, StatusModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    bookmarks = models.ManyToManyField(Post, related_name='user_bookmarks', blank=True)
    favourites = models.ManyToManyField(Post, related_name='user_favourites', blank=True)
    followers = models.ManyToManyField(User, related_name='user_followers', blank=True)
    followings = models.ManyToManyField(User, related_name='user_followings', blank=True)

    def __str__(self):
        return f'{self.user} profile'