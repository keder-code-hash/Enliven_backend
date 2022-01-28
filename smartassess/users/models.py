from pyexpat import model
from tkinter.tix import Tree
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import jwt, datetime


##createing a custom user manager for managing the model.
class CustomAccountManager(BaseUserManager):
    def create_user(self, email, user_name, last_name, first_name, password, **other_fields):
        if not email:
            raise ValueError(_('provide an email'))
        email = BaseUserManager.normalize_email(email=email)
        user = Register(email=email, user_name=user_name, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    ##creating a super user or a admin for managing the whole things.
    def create_superuser(self, email, user_name, interests, first_name, password, **other_fields):
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_superuser', True)

        return self.create_user(email, user_name, interests, first_name, password, **other_fields)


##Actual register model for a user


class Register(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(_('email address'), blank=False, max_length=100, primary_key=True)
    # profile_pic=models.FileField(upload_to='uploads/profile/',null=True)
    profile_pic_url=models.CharField(null=True,max_length=300,default="https://res.cloudinary.com/dvcjj1k7a/image/upload/v1636390885/Blog/Profile/663328_ti7cnp.png")
    first_name = models.CharField(default='', blank=False, max_length=20)
    last_name = models.CharField(default='', blank=False, max_length=20)

    # department=models.CharField(null=True,max_length=50)
    date_of_birth = models.DateField(null=True, blank=False)
    bio = models.CharField( null=True,max_length=100)
    interests = models.TextField(null=True, max_length=200)
    ph_no = models.CharField( null=True,max_length=10)

    created_user = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # define a object of customUserManager
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'interests']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

# class Cources(models.Model):
# class Dept(models.Model):