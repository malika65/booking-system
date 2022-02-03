import uuid

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from model_utils import Choices
from django.utils.crypto import get_random_string

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin): 

    ADMIN = 1
    MANAGER = 2
    EMPLOYEE = 3
    REGULAR_USER = 4
    BUSSINESS_USER = 5  

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (MANAGER, 'Managers'),
        (EMPLOYEE, 'Employee'),
        (REGULAR_USER, 'Regular User'),
        (BUSSINESS_USER, 'Bussiness User')
        )
    
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=REGULAR_USER)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.EmailField()
    modified_by = models.EmailField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def delete(self, *args, **kwargs):
        self.is_active = True
        super().delete(*args, **kwargs)

    
class ConfirmCode(models.Model):
    code = models.CharField(max_length=6)
    confirm = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name = 'codes' , on_delete=models.CASCADE)
    reset = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Код подтверждения'
        verbose_name_plural = 'Коды подтверждения'

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_random_string(length=6)
        super(ConfirmCode, self).save(*args, **kwargs)