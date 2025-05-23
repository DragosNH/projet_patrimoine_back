from pyexpat import model
from tkinter import Widget
from turtle import mode
from unittest.util import _MAX_LENGTH
from xml.dom import ValidationErr
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Construction(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=250)
    zip_code = models.CharField(
        max_length=5,
        validators=[RegexValidator(r'^\d{5}$', message="The ZIP code you entered is not valid in France")]
    )
    city = models.CharField(max_length=50)
    demolished = models.BooleanField(default=False)

    CONSTRUCTION_TYPE = [
        ("HOUSE", "House"),
        ("CATHEDRAL", "Cathedral"),
        ("CASTLE", "Castle"),
    ]
    type = models.CharField(max_length=20, choices=CONSTRUCTION_TYPE)
    
    def __str__(self):
        return f"{self.get_type_display()} at {self.address}"
        
class CustomUserManager(BaseUserManager):
    def create_user(self, email,username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email adress")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username


class Model3D(models.Model):
    construction = models.ForeignKey(
        Construction,
        related_name='models',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    file = models.FileField(
        upload_to='bundles/',
        help_text="Upload your AssetBundle (.bundle) for this model"
    )
    latitude  = models.FloatField(
        help_text="GPS latitude (decimal degrees)"
    )
    longitude = models.FloatField(
        help_text="GPS longitude (decimal degrees)"
    )
    altitude  = models.FloatField(
        null=True,
        blank=True,
        help_text="Optional altitude (meters)"
    )
    uploaded  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} @ ({self.latitude}, {self.longitude})"