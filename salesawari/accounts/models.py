from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid


def id_gen() -> str:
    return str(uuid.uuid4()) + str(uuid.uuid4())


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class CustomUserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email can't be blank")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email=self.normalize_email(email), password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save(using=self._db)
        return user
    

class Account(AbstractBaseUser):
    full_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    username = models.CharField(max_length=30, unique=True, blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_buyer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length=100, unique=True, default=id_gen, editable=True)
    otp = models.CharField(max_length=16, blank=True, null=True, default="")

    objects = CustomUserAccountManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.full_name if self.full_name else self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
