from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password = None, **extra_fields):
        """ create and save un nouvel user"""
        if not email:
            raise ValueError('User must have a valid email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,password):
        """creates a new su"""
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser,PermissionsMixin):
    """custom user model taht support using email instead of username"""
    email = models.EmailField(max_length = 255, unique=True)
    name = models.CharField(max_length = 255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """tag pour les recettes"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)

    def __str__(self):
        return self.name
